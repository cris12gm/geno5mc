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

from .models import samples

# Create your views here.

class primaryData(TemplateView):
    template = "primaryData.html"

    def post(self,request):
        tableSamples = samples.get_all_samples()

        return render(request, self.template, {
            'tableSamples':tableSamples
        })
    def get(self,request):

        tableSamples = samples.get_all_samples()
        
        return render(request, self.template, {
            'tableSamples':tableSamples
            })

