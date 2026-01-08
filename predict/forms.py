from django import forms
from .models import DiabetesPrediction

class DiabetesPredictionForm(forms.ModelForm):
    class Meta:
        model = DiabetesPrediction
        fields = [
            'Pregnancies', 'Glucose', 'Blood_Pressure', 'Skin_Thickness', 
            'Insulin', 'BMI', 'Diabetes_Pedigree_Function', 'Age'
        ]
        
        labels = {
            'Pregnancies': '妊娠回数',
            'Glucose': 'グルコース (空腹時血糖)',
            'Blood_Pressure': '血圧 (拡張期血圧)',
            'Skin_Thickness': '皮膚の厚み (上腕三頭筋)',
            'Insulin': 'インシュリン (2時間後の血清)',
            'BMI': 'BMI (肥満度)',
            'Diabetes_Pedigree_Function': '家系係数',
            'Age': '年齢',
        }

        # ヘルプテキストを追加してユーザーをガイド
        help_texts = {
            'Diabetes_Pedigree_Function': '親族の病歴に基づいた数値（例: 0.5）を入力してください。',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 個別の入力制限（バリデーション）の設定
        # min_value を設定するとブラウザ側でも「0以上を入力してください」と警告が出ます
        self.fields['Pregnancies'].widget.attrs.update({'min': '0', 'max': '20'})
        self.fields['Glucose'].widget.attrs.update({'min': '0'})
        self.fields['Blood_Pressure'].widget.attrs.update({'min': '0'})
        self.fields['BMI'].widget.attrs.update({'min': '10', 'max': '60'})
        self.fields['Age'].widget.attrs.update({'min': '0', 'max': '120'})

        # 全フィールド共通の処理
        for name, field in self.fields.items():
            # 既存の attrs を維持しつつ更新
            current_class = field.widget.attrs.get('class', '')
            field.widget.attrs.update({
                'class': f'form-control {current_class}'.strip(),
                'placeholder': f'{field.label}を入力してください'
            })

    def clean_BMI(self):
        """ BMIに対するカスタムバリデーション例 """
        bmi = self.cleaned_data.get('BMI')
        if bmi and (bmi < 10 or bmi > 70):
            raise forms.ValidationError("BMIの数値が範囲外です。正しい数値を入力してください。")
        return bmi