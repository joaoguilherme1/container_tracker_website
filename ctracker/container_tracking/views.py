from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import ProcurarForm
from .carries import is_valid_carrier, request_container_info


def index(request):
    form = ProcurarForm()
    return render(request, "index.html", {"form": form})


def resultados(request, container_number):

    data = request_container_info(container_number)

    return render(
        request,
        "results.html",
        {"containers": data, "container_number": container_number},
    )


def procura(request):

    if request.method == "POST":
        form = ProcurarForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            container_number = cd.get("container_number")

            if is_valid_carrier(container_number):
                return HttpResponseRedirect(container_number)

            else:
                return render(request, "carrier_nao_suportado.html", {"form": form})

        else:
            erros = form.errors
            for error in erros.keys():
                messages.error(request, erros[error][0])

    return render(request, "index.html", {"form": form})
