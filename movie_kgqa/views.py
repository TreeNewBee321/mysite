from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Actor,Movie,Genre
from django.views.decorators import csrf
from django.http import HttpResponse
from . import query_main
# Create your views here.
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

def index(request):
    context = {}
    context['title'] = '电影知识图谱检索系统'
    return render(request, 'index.html', context)

@csrf_exempt
def search(request):
    result = {}
    if request.POST:
        content = request.POST['keyword']
        result['ans'] = list()
        result['ans'] = query_main.kb_query(content)
    return render(request,"index.html",result)