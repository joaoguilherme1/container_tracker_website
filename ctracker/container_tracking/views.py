from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import ProcurarForm
from .carries import is_valid_carrier, request_container_info
from .models import Container
from datetime import datetime


def _update_container_data(container_number, data):
    if not data:
        return

    Container.objects.update_or_create(
        number=container_number,
        carrier=data["carrier"],
        defaults={
            "status": data["status"],
            "date": data["date"],
            "location": data["location"],
            "last_import": datetime.now(),
        },
    )

    return Container.objects.filter(number=container_number)


def index(request):
    form = ProcurarForm()
    return render(request, "index.html", {"form": form})


def _need_update(containers):
    if not containers:
        return True

    for container in containers:
        diff = abs(
            (
                container.last_import.replace(tzinfo=None)
                - datetime.now().replace(tzinfo=None)
            ).days
        )

        return diff > 1


def resultados(request, container_number):

    container = Container.objects.filter(number=container_number)

    need_request_new_data = _need_update(container)

    new_data = None
    if need_request_new_data:
        new_data = request_container_info(container_number)
        container = _update_container_data(container_number, new_data)

    if not container:
        messages.error(
            request, f"O container {container_number} não foi encontrado."
        )

    form = ProcurarForm()

    return render(
        request,
        "results.html",
        {
            "containers": container,
            "container_number": container_number,
            "form": form,
        },
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
                return render(
                    request, "carrier_nao_suportado.html", {"form": form}
                )

        else:
            erros = form.errors
            for error in erros.keys():
                messages.error(request, erros[error][0])

    return render(request, "index.html", {"form": form})
