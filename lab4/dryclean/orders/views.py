from django.http import Http404
from django.shortcuts import render
from .models import Branch, Contract


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
