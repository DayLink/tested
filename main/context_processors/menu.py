#-*- coding: utf-8 -*-
from main.models import MenuItem

def get_menu(request):
    all_menu = MenuItem.objects.all()
    return locals()

