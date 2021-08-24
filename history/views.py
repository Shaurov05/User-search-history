from django.shortcuts import render
from . models import *
import json
from django.db.models import Count


# Create your views here.


def showHistory(request):

    if request.method == 'GET':
        users = CustomUser.objects.all()[:10]
        keywords_with_count = History.objects.values("keyword").\
            order_by("keyword").annotate(key_count=Count("keyword")).order_by('-key_count')[:10]
        # keywords_count_by_user = History.objects.values("keyword", "custom_user").order_by("keyword", "custom_user").\
        #     annotate(kwy_count=Count("keyword"))
        keywords = History.objects.all()

        return render(request, template_name="history.html", context={"keywords": keywords,
                                                                      "keywords_with_count":keywords_with_count,
                                                                      "users": users})

    elif request.method == "POST":
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']


