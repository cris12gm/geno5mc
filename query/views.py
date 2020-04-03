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
from .forms import QuerySNP,QueryGene

from sqlalchemy import inspect

class Errors(Enum):
    NO_ERROR = 0
    NOT_VALID = 1
    NOT_ASSOCIATED = 2

class SNPAssociatedQuery(TemplateView):
    template = 'query.html'

    def get(self, request):  
        formSNP = QuerySNP()
        formGene = QueryGene()
        return render(request, self.template, {
            'formSNP':formSNP,
            'formGene':formGene
        })
    