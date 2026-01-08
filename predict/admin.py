# predict/admin.py
from django.contrib import admin
from .models import DiabetesPrediction

@admin.register(DiabetesPrediction)
class DiabetesPredictionAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'Result', 'Age', 'Glucose', 'BMI') # 一覧で表示する項目
    list_filter = ('Result', 'created_at') # フィルタ機能
