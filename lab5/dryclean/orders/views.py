from django.http import Http404
from django.shortcuts import render, redirect
from .models import Branch, Client, Contract, Item, Service


def archive(request):
    return render(request, 'archive.html', {"contracts": Contract.objects.all()})


def get_contract(request, contract_id):
    try:
        contract = Contract.objects.get(id=contract_id)
        return render(request, 'contract.html', {"contract": contract})
    except Contract.DoesNotExist:
        raise Http404


def branch_stats(request, branch_id): #статистика
    try:
        branch = Branch.objects.get(id=branch_id)
    except Branch.DoesNotExist:
        raise Http404
    contracts = Contract.objects.filter(branch=branch)
    items = [item for c in contracts for item in c.item_set.all()]
    stats = {
        "contracts": contracts.count(),
        "items": len(items),
        "returned": len([i for i in items if i.date_returned]),
        "revenue": sum(i.price() for i in items),
    }
    return render(request, 'branch.html', {"branch": branch, "stats": stats,
                                           "contracts": contracts})


def create_contract(request): #создание договора
    if request.user.is_anonymous:
        raise Http404
    context = {
        "clients": Client.objects.all(),
        "branches": Branch.objects.all(),
        "services": Service.objects.all(),
        "complexity": Item.COMPLEXITY,
    }
    if request.method == "POST": #обработать данные формы
        form = {
            "number": request.POST.get("number", "").strip(),
            "client": request.POST.get("client", ""),
            "branch": request.POST.get("branch", ""),
            "service": request.POST.get("service", ""),
            "description": request.POST.get("description", "").strip(),
            "complexity": request.POST.get("complexity", "1.0"),
            "urgent": request.POST.get("urgent") == "on",
            "comment": request.POST.get("comment", "").strip(),
        }
        context["form"] = form
        required = ["number", "client", "branch", "service", "description"]
        if not all(form[field] for field in required):
            form["errors"] = "Не все поля заполнены"
        elif Contract.objects.filter(number=form["number"]).exists():
            form["errors"] = "Договор с номером %s уже существует" % form["number"]
        else: #сохраняем если нет ошибок
            contract = Contract.objects.create(
                number=form["number"], receiver=request.user,
                client_id=form["client"], branch_id=form["branch"],
                comment=form["comment"])
            Item.objects.create(
                contract=contract, service_id=form["service"],
                description=form["description"],
                complexity=form["complexity"], urgent=form["urgent"])
            return redirect('get_contract', contract_id=contract.id)
        #если введённые данные неправильные, возвращаем форму с ошибкой
        return render(request, 'create_contract.html', context)
    return render(request, 'create_contract.html', context)
