from paa.models import KeyWordOfPaa, KeyWordAnswer, KeyWordRelated, KeyWordImages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from GooglePAA.scrap import mainScraper
from .serializers import KeyWordOfPaaSerializer, KeyWordAnswerSerializer, KeyWordImagesSerializer, KeyWordRelatedSerializer


@api_view(['GET'])
def searchUsingKeyWord(request):
    keyWord = request.GET.get('q', None)
    if keyWord:
        searchData = KeyWordOfPaa.objects.filter(Q(keyword__icontains=keyWord.upper()) | Q(keyword__icontains=keyWord.title()) | Q(keyword__icontains=keyWord.lower()))
        if searchData:
            serializer = KeyWordOfPaaSerializer(searchData, many=True)
            return Response({'msg': 'success', 'data': serializer.data})
        else:
            return Response({'msg': 'data not found!'})
    else:
        return Response({'msg': 'q is required!'})


@api_view(['POST'])
def scrappingApi(request):
    keyWord = request.GET.get('q', None)
    numOfTimes = request.GET.get('quantity', None)
    relatedKeyWord = request.GET.get('related', None)
    pixaBayKeyWord = request.GET.get('pixabay', None)
    pexelKeyWord = request.GET.get('pexels', None)
    unSplashKeyWord = request.GET.get('unsplash', None)
    googleKeyWord = request.GET.get('gmedia', None)
    youTubeKeyWord = request.GET.get('youtube', None)
    if keyWord and numOfTimes and relatedKeyWord and pixaBayKeyWord and pexelKeyWord and unSplashKeyWord and googleKeyWord and youTubeKeyWord:
        keyWordList = list(keyWord.split(","))
        relatedKeyWord = relatedKeyWord == 'on'
        pixaBayKeyWord = pixaBayKeyWord == 'on'
        pexelKeyWord = pexelKeyWord == 'on'
        unSplashKeyWord = unSplashKeyWord == 'on'
        googleKeyWord = googleKeyWord == 'on'
        youTubeKeyWord = youTubeKeyWord == 'on'
        scrapData = mainScraper(keyWordList, int(numOfTimes), relatedKeyWord, pixaBayKeyWord, pexelKeyWord, unSplashKeyWord, googleKeyWord, youTubeKeyWord)
        return Response(scrapData)
    else:
        if keyWord is None:
            return Response({'msg': 'q is required!'})
        if numOfTimes is None:
            return Response({'msg': 'quantity is required!'})
        if relatedKeyWord is None:
            return Response({'msg': 'related is required!'})
        if pixaBayKeyWord is None:
            return Response({'msg': 'pixabay is required!'})
        if pexelKeyWord is None:
            return Response({'msg': 'pexels is required!'})
        if unSplashKeyWord is None:
            return Response({'msg': 'unsplash is required!'})
        if googleKeyWord is None:
            return Response({'msg': 'gmedia is required!'})
        if youTubeKeyWord is None:
            return Response({'msg': 'youtube is required!'})
