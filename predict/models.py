from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class DiabetesPrediction(models.Model):
    # 既存のバリデーションは非常に良い設定です
    Pregnancies = models.IntegerField(
        verbose_name='妊娠回数',
        validators=[MinValueValidator(0)]
    )
    Glucose = models.FloatField(
        verbose_name='グルコース',
        validators=[MinValueValidator(0)]
    )
    Blood_Pressure = models.FloatField(
        verbose_name='血圧',
        validators=[MinValueValidator(0)]
    )
    Skin_Thickness = models.FloatField(
        verbose_name='皮膚の厚み',
        validators=[MinValueValidator(0)]
    )
    Insulin = models.FloatField(
        verbose_name='インシュリン',
        validators=[MinValueValidator(0)]
    )
    BMI = models.FloatField(
        verbose_name='BMI',
        validators=[MinValueValidator(0)]
    )
    Diabetes_Pedigree_Function = models.FloatField(
        verbose_name='家系係数',
        validators=[MinValueValidator(0)]
    )
    Age = models.IntegerField(
        verbose_name='年齢',
        validators=[MinValueValidator(0), MaxValueValidator(120)]
    )
    Result = models.CharField(
        max_length=10, # 陽性・陰性なら10文字で十分です
        verbose_name='判定結果'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='判定日時',
        db_index=True  # ソートに使用するためインデックスを追加
    )

    class Meta:
        verbose_name = '糖尿病判定履歴'
        verbose_name_plural = '糖尿病判定履歴一覧'
        ordering = ['-created_at'] # デフォルトで新しい順に並ぶよう設定

    def __str__(self):
        return f"{self.created_at.strftime('%Y-%m-%d %H:%M')} - {self.Result}"
