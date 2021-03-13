from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return render(request, "pages/index.html")


def frekans(request):
    return render(request, "pages/frekans.html")


def frekansResult(request):
    url = request.POST.get("quantity")
    context = {"url": url}
    print(url)
    return render(request, "pages/frekansResult.html", context)


"""
formdan input alma işlemleri tamam, beautiful soup indirilip birinci isterden yola çıkılacak
"""
