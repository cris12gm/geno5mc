import itertools
from django.conf import settings
import datetime
import os
from enum import Enum
from functools import reduce
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic import FormView, DetailView, TemplateView
from django.http import JsonResponse
from django.urls import reverse_lazy

# Create your views here.

class plotEnhancers(TemplateView):
    template = "plotElement.html"

    def post(self,request):
        pass
        return render(request, self.template, {})
    def get(self,request):
        return render(request, self.template, {})

class plotEnhancers2(TemplateView):
    template = "plotElement2.html"

    def post(self,request):
        pass
        return render(request, self.template, {})
    def get(self,request):
        return render(request, self.template, {})