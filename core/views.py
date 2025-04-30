from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
import uuid
import os
import markdown2
import bleach
from bs4 import BeautifulSoup

from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_http_methods
from django.http import HttpResponse, JsonResponse
import uuid
import os
import bleach

from django.views.generic import TemplateView
from django.views import View
from django.views.decorators.http import require_POST, require_http_methods
from django.utils.decorators import method_decorator

from django.http import FileResponse, Http404
import logging

logger = logging.getLogger(__name__)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import User
from django.template.loader import render_to_string
from django.views.decorators.http import require_GET

from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserProfileForm


import json
from django.db import transaction
from django.db.models import Sum, Count
from django.contrib.auth import get_user_model


# CBV for Index View
class HomeView(TemplateView):
    template_name = "core/home.html"
