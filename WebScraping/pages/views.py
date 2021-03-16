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
    frequency = calculateFrequency(url)
    context = {"words": frequency.keys(), "frequency": frequency.values()}
    return render(request, "pages/frekansResult.html", context)


def keyword(request):
    return render(request, "pages/keyword.html")


def keywordResult(request):
    url = request.POST.get("quantity")
    top10 = exportTop10(url)
    context = {"words": top10.keys(), "frequency": top10.values()}
    return render(request, "pages/keywordResult.html", context)

def similarityScore(request):
    return render(request, "pages/similarityScore.html")

def similarityScoreResult(request):
    url_1 = request.POST.get("url_1")
    url_2 = request.POST.get("url_2")
    top10_1= exportTop10(url_1)
    top10_2 = exportTop10(url_2)
    similarity = calculateSimilarity(top10_1, top10_2, url_2)
    context = {
        "words_1": top10_1.keys(), 
        "frequency_1": top10_1.values(),
        "words_2": top10_2.keys(), 
        "frequency_2": top10_2.values(),
        "similarity": similarity,
    }

    return render(request, "pages/similarityScoreResult.html", context)


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


def calculateFrequency(url):
    allContent = scrapeUrl(url)
    wordList = splitWords(allContent)
    frequency = {}
    for word in wordList:
        if word not in frequency.keys():
            frequency[word] = 1
        else:
            num = frequency[word] + 1
            frequency.update({word: num})
    return frequency


def exportTop10(url):
    frequency = calculateFrequency(url)
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
        if i == 10:
            break
        else:
            if key in baglacList:
                continue
            else:
                top10[key] = value
                i = i + 1

    return top10

def calculateSimilarity(top10_1, top10_2, url_2):
    frequency = calculateFrequency(url_2)
    keyWordCarpim = 1
    totalWordCount = 0

    for keys_1 in top10_1.keys():
        if keys_1 in top10_2.keys():
            keyWordCarpim = keyWordCarpim * top10_2[keys_1]
    
    if keyWordCarpim == 1:
        return totalWordCount

    for value in frequency.values():
        totalWordCount = totalWordCount + value

    print(totalWordCount)
    print(keyWordCarpim)
    result = (keyWordCarpim / totalWordCount)*100
    return  f'{result:.4f}'
    



