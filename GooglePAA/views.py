from .scrap import mainScraper
from django.shortcuts import render, HttpResponse
import json
from paa.models import KeyWordOfPaa, KeyWordAnswer, KeyWordRelated, KeyWordImages, KeyWordVideos, KeyWordGoogleImages


def scraperFront(request):
    if request.method == "POST":
        try:
            keyWord = request.POST.get('keyWord')
            numOfTimes = request.POST.get('numOfTimes')
            relatedKeyWord = request.POST.get('relatedKeyWord')
            pixaBayKeyWord = request.POST.get('pixaBayKeyWord')
            pexelKeyWord = request.POST.get('pexelKeyWord')
            unSplashKeyWord = request.POST.get('unSplashKeyWord')
            googleKeyWord = request.POST.get('googleKeyWord')
            youTubeKeyWord = request.POST.get('youTubeKeyWord')
            relatedKeyWord = relatedKeyWord == 'true'
            pixaBayKeyWord = pixaBayKeyWord == 'true'
            pexelKeyWord = pexelKeyWord == 'true'
            unSplashKeyWord = unSplashKeyWord == 'true'
            googleKeyWord = googleKeyWord == 'true'
            youTubeKeyWord = youTubeKeyWord == 'true'
            keyWordList = list(keyWord.split(","))
            scrapData = mainScraper(keyWordList, int(numOfTimes), relatedKeyWord, pixaBayKeyWord, pexelKeyWord, unSplashKeyWord, googleKeyWord, youTubeKeyWord)
            for data in scrapData:
                keyWordInsert = KeyWordOfPaa(keyword=data['keyword'], numoftimes=str(numOfTimes))
                keyWordInsert.save()
                keysList = list(data.keys())
                for paa in data['paa']:
                    passInsert = KeyWordAnswer(keywordofpaa=keyWordInsert, question=paa['question'], answer=paa['answer'])
                    passInsert.save()
                if 'related' in keysList:
                    for related in data['related']:
                        relatedInsert = KeyWordRelated(keywordofpaa=keyWordInsert, related_search=related)
                        relatedInsert.save()
                if 'pixabaycom' in keysList:
                    for images in data['pixabaycom']:
                        imagesInsert = KeyWordImages(keywordofpaa=keyWordInsert, image=images)
                        imagesInsert.save()
                if 'pexelscom' in keysList:
                    for images in data['pexelscom']:
                        imagesInsert = KeyWordImages(keywordofpaa=keyWordInsert, image=images)
                        imagesInsert.save()
                if 'unsplashcom' in keysList:
                    for images in data['unsplashcom']:
                        imagesInsert = KeyWordImages(keywordofpaa=keyWordInsert, image=images)
                        imagesInsert.save()
                if 'googleImages' in keysList:
                    for images in data['googleImages']:
                        imagesInsert = KeyWordGoogleImages(keywordofpaa=keyWordInsert, image=images)
                        imagesInsert.save()
                if 'video' in keysList:
                    for videos in data['video']:
                        videosInsert = KeyWordVideos(keywordofpaa=keyWordInsert, video=videos)
                        videosInsert.save()
            context = {'data': scrapData}
        except Exception as e:
            print(e)
            context = {'msg': 'Some Exception Accrued!'}
        return HttpResponse(json.dumps(context))
    else:
        return render(request, 'scraper.html')
