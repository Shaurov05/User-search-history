import datetime
from datetime import date

from django.shortcuts import render
from .models import *
from accounts.models import *
import json
from django.db.models import Count
from django.core.paginator import Paginator
from django.http import JsonResponse


# Create your views here.


def showHistory(request):
    users = CustomUser.objects.all()
    keywords_with_count = History.objects.values("keyword"). \
        order_by("keyword").annotate(key_count=Count("keyword")).order_by('-key_count')
    # keywords_count_by_user = History.objects.values("keyword", "custom_user").order_by("keyword", "custom_user").\
    #     annotate(kwy_count=Count("keyword"))
    keywords = History.objects.all()

    if request.method == 'GET':
        if keywords:
            paginator = Paginator(keywords, 12)
            page_number = request.GET.get('page')
            keywords = paginator.get_page(page_number)
        else:
            keywords = ""

        return render(request, template_name="history.html", context={"keywords": keywords,
                                                                      "keywords_with_count": keywords_with_count,
                                                                      "users": users})
    elif request.method == "POST":
        data = json.loads(request.body)
        print("data = ", data['page_n'][-1])
        page_number = data['page_n'][-1]

        if keywords:
            paginator = Paginator(keywords, 12)
            keywords = paginator.get_page(page_number)
        else:
            keywords = ""

        data = []
        page = {}

        if keywords != "":
            for keyword in keywords:
                data.append({"keyword": keyword.keyword,
                             "search_time": keyword.search_time.strftime(
                                 '%b %d,%Y, %H:%M %p') if keyword.search_time else None,
                             "custom_user": keyword.custom_user.username,
                             "search_result": keyword.search_result})

            page.update({
                "has_previous": keywords.has_previous(),
                "previous_page_number": keywords.previous_page_number() if keywords.has_previous() else None,
                "has_next": keywords.has_next(),
                "next_page_number": keywords.next_page_number() if keywords.has_next() else None,
                "number": keywords.number,
            })
            print(page)
            print(keywords.number)

        return JsonResponse({"data": data, "page": page})


def filterHistory(request):
    histories = History.objects.all()

    if request.method == 'POST':
        minimun_time = datetime.time.min
        maximum_time = datetime.time.max
        data = json.loads(request.body)
        print("data = ", data)

        page_number = data["data"]['page_n'][-1] if 'page_n' in data["data"].keys() else 1

        if "checked_keywords" in data["data"].keys() and data["data"]["checked_keywords"] != []:
            selectedKeywords = data["data"]["checked_keywords"]
            print("before selectedKeywords: ", len(histories))
            histories = histories.filter(keyword__in=selectedKeywords)
            print(len(histories))

        if "selected_users" in data["data"].keys() and data["data"]["selected_users"] != []:
            selectedUsers = data["data"]["selected_users"]
            print("before selected_users: ", len(histories))
            histories = histories.filter(custom_user__username__in=selectedUsers)
            print(len(histories))

        if "timeRange" in data["data"].keys() and data["data"]["timeRange"] != []:
            timeRange = data["data"]["timeRange"]

            print("before timeRange: ", len(histories))
            if "last month" in timeRange:
                print("month")
                syear, smonth, sday = str(timezone.now().date()).split('-')
                start_date = date(int(syear), int(smonth) - 1, int(sday))
                histories = histories.filter(search_time__gte=start_date)
            elif "last week" in timeRange:
                print("week")
                syear, smonth, sday = str(timezone.now().date()).split('-')
                start_date = date(int(syear), int(smonth), int(sday) - 7)
                histories = histories.filter(search_time__gte=start_date)
            elif "yesterday" in timeRange:
                print("yesterday")
                syear, smonth, sday = str(timezone.now().date()).split('-')
                start_date = date(int(syear), int(smonth), int(sday) - 1)
                histories = histories.filter(search_time__gte=start_date)

            print(len(histories))

        if data["data"]["start_date_input"] != "" and data["data"]["end_date_input"] != "":
            syear, smonth, sday = data["data"]["start_date_input"].split('-')
            start_date = date(int(syear), int(smonth), int(sday))
            eyear, emonth, eday = data["data"]["end_date_input"].split('-')
            end_date = date(int(eyear), int(emonth), int(eday))

            date_range = (datetime.datetime.combine(start_date, minimun_time).strftime("%Y-%m-%d %H:%M:%S"),
                          datetime.datetime.combine(end_date, maximum_time).strftime("%Y-%m-%d %H:%M:%S"))
            # print(date_range)
            histories = histories.filter(search_time__range=date_range)
        elif data["data"]["start_date_input"] != "":
            syear, smonth, sday = data["data"]["start_date_input"].split('-')
            start_date = date(int(syear), int(smonth), int(sday)).strftime("%Y-%m-%d %H:%M:%S")
            histories = histories.filter(search_time__gte=start_date)
        elif data["data"]["end_date_input"] != "":
            eyear, emonth, eday = data["data"]["end_date_input"].split('-')
            end_date = date(int(eyear), int(emonth), int(eday)).strftime("%Y-%m-%d %H:%M:%S")
            histories = histories.filter(search_time__lte=end_date)

        if histories:
            paginator = Paginator(histories, 12)
            histories = paginator.get_page(page_number)
        else:
            histories = ""

        data = []
        page = {}

        if histories != "":
            for keyword in histories:
                data.append({"keyword": keyword.keyword,
                             "search_time": keyword.search_time.strftime(
                                 '%b %d,%Y, %H:%M %p') if keyword.search_time else None,
                             "custom_user": keyword.custom_user.username,
                             "search_result": keyword.search_result})

            page.update({
                "has_previous": histories.has_previous(),
                "previous_page_number": histories.previous_page_number() if histories.has_previous() else None,
                "has_next": histories.has_next(),
                "next_page_number": histories.next_page_number() if histories.has_next() else None,
                "number": histories.number,
            })
            print(page)
            print(histories.number)

        return JsonResponse({"data": data, "page": page})
