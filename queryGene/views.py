import itertools
from django.conf import settings
import datetime
import os
from functools import reduce
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic import FormView, DetailView
from django.http import JsonResponse
from django.urls import reverse_lazy
import pymysql
from .forms import QueryGene