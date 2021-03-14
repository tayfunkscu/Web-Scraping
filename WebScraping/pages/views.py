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
+ p etiketlerinin içeriklerini kelimelere ayırkan bir fonksiyon yaz
+ kelimelerin frekansını hesaplayan bir fonksiyon yaz
"""


def index(request):
    return render(request, "pages/index.html")


def frekans(request):
    return render(request, "pages/frekans.html")


def frekansResult(request):
    url = request.POST.get("quantity")
    allContent = scrapeUrl(url)
    wordList = splitWords(allContent)
    frequency = calculateFrequency(wordList)
    context = {"words": frequency.keys(), "frequency": frequency.values()}
    return render(request, "pages/frekansResult.html", context)


def keyword(request):
    return render(request, "pages/keyword.html")


def keywordResult(request):
    url = request.POST.get("quantity")
    allContent = scrapeUrl(url)
    wordList = splitWords(allContent)
    frequency = calculateFrequency(wordList)
    top10 = sortFrequency(frequency)
    context = {"words": top10.keys(), "frequency": top10.values()}
    return render(request, "pages/keywordResult.html", context)


"""
Verilen url'deki p etiketlerinin içeriklerine sahip bir string listesi döndürür
///////////////////////////////////////////////////////////////////////////////
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
    wordList = ""
    for tag in allContentList:
        tag = tag.lower()
        tag_no_punctuation = re.sub("[^\w\s]", "", tag)
        wordList = wordList + tag_no_punctuation
    wordList = wordList.split()
    return wordList


def calculateFrequency(wordlist):
    frequency = {}
    for word in wordlist:
        if word not in frequency.keys():
            frequency[word] = 1
        else:
            num = frequency[word] + 1
            frequency.update({word: num})
    return frequency


def sortFrequency(frequency):

    baglacList = [
        "zira",
        "yoksa",
        "yine",
        "yeter",
        "ki",
        "yalnız",
        "yahut",
        "da",
        "ya",
        "veyahut",
        "veya",
        "ve",
        "üstelik",
        "öyleyse",
        "öyle",
        "oysaki",
        "oysa",
        "nitekim",
        "ne",
        "de",
        "ne",
        "yazık",
        "var",
        "nasıl",
        "mademki",
        "lâkin",
        "kısacası",
        "ise",
        "ile",
        "hem",
        "hele",
        "hatta",
        "hâlbuki",
        "gerek",
        "gerekse",
        "gene",
        "fakat",
        "demek",
        "dahi",
        "çünkü",
        "bile",
        "ancak",
        "ama",
        "açıkçası",
    ]

    frequency = dict(reversed(sorted(frequency.items(), key=lambda item: item[1])))

    i = 0
    top10 = {}
    for key, value in frequency.items():
        if i is 10:
            break
        else:
            if key in baglacList:
                continue
            else:
                top10[key] = value
                i = i + 1

    return top10