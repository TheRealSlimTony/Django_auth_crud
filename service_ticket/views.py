from django.shortcuts import get_object_or_404, render
from .models import Ticket, User


# Create your views here.
def home(request):
    if request.method == "POST":
        id_search = request.POST["ID_search"]
        id_search = id_search.replace(" ", "")

        if not id_search.isnumeric():
            return render(request, "ticket_view.html", {"error": "ID is not valid"})

        tickets = Ticket.objects.filter(id=request.POST["ID_search"])

        return render(request, "ticket_view.html", {"tickets": tickets})

    else:
        tickets = Ticket.objects.all()
    return render(request, "ticket_view.html", {"tickets": tickets})


def create(request):
    if request.method == "POST":
        username = request.POST["user"]
        sign_off = request.POST.get("sign_off", False)
        code_review = request.POST["code_review"]

        if sign_off == "on":
            sign_off = True
        elif sign_off == "":
            sign_off = False

        user = User.objects.get(username=username)

        ticket = Ticket.objects.create(
            user=user, sign_off=sign_off, code_review=code_review
        )

        return render(request, "create.html")

    else:
        return render(request, "create.html")


def detail(request,ticket_id):

  
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    print(ticket)

    return render(request, "detail.html",{
        'ticket':ticket
    })
