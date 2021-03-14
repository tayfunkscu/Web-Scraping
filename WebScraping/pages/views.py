from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
import re
import string

# Create your views here.
"""
checklist
+ url'yi al ve sonuç sayfasına yazdır
+ url'nin içeriğini ayıkla ve sonuç sayfasına yazdır
- p etiketlerinin içeriklerini kelimelere ayırkan bir fonksiyon yaz
- kelimelerin frekansını hesaplayan bir fonksiyon yaz
"""


def index(request):
    return render(request, "pages/index.html")


def frekans(request):
    return render(request, "pages/frekans.html")


def frekansResult(request):
    url = request.POST.get("quantity")
    allContent = scrapeUrl(url)
    wordList = splitWords(allContent)
    context = {"allContent": wordList}
    return render(request, "pages/frekansResult.html", context)


"""
Verilen url'deki p etiketlerinin içeriklerine sahip bir string listesi döndürür
"""


def scrapeUrl(url):
    r = requests.get(url)
    source = BeautifulSoup(r.content, "lxml")
    allContent = source.find_all("p")
    allContentList = list()
    for tag in allContent:
        allContentList.append(tag.text)
    return allContentList


def splitWords(allContentList):
    wordList = []
    for tag in allContentList:
        tag = tag.lower()
        tag_no_punctuation = re.sub("[^\w\s]", "", tag)
        tag_no_punctuation = tag_no_punctuation.split()
        wordList.append(tag_no_punctuation)
    return wordList
