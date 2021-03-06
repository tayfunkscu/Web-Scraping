from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("frekans", views.frekans, name="frekans"),
    path("frekansResult", views.frekansResult, name="frekansResult"),
    path("keyword", views.keyword, name="keyword"),
    path("keywordResult", views.keywordResult, name="keywordResult"),
    path("similarityScore", views.similarityScore, name="similarityScore"),
    path(
        "similarityScoreResult",
        views.similarityScoreResult,
        name="similarityScoreResult",
    ),
    path("indexingAndSort", views.indexingAndSort, name="indexingAndSort"),
    path(
        "indexingAndSortResult",
        views.indexingAndSortResult,
        name="indexingAndSortResult",
    ),
    path("semantic", views.semantic, name="semantic"),
    path("semanticResult", views.semanticResult, name="semanticResult"),
]