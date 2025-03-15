from django.contrib import admin

# Register your models here.

# admin.py
from django.contrib import admin
from .models import House,Job

@admin.register(House)
class HousetAdmin(admin.ModelAdmin):
    list_display = ('house_id', 'created_at')  # 在後台列表顯示的欄位
    search_fields = ('created_at',)          # 搜尋功能
    list_filter = ('created_at',)           # 篩選功能
    
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'created_at')  # 在後台列表顯示的欄位
    search_fields = ('created_at',)          # 搜尋功能
    list_filter = ('created_at',)           # 篩選功能
