from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from news.models import New


@login_required
def news_list_view(request):
    news = New.objects.all()

    search_query = request.GET.get('search')  # Obtener el parámetro por el que busca

    if search_query:
        events = news.filter(
            Q(name__icontains=search_query))

    return render(request, "news/news.html", {'news': news})
