# Review/admin.py
from django.contrib import admin
from .models import Review

# Review 모델을 관리자 페이지에 등록합니다.
admin.site.register(Review)