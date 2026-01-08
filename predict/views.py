from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages  # 通知機能を追加
from .models import DiabetesPrediction
from .forms import DiabetesPredictionForm
import csv
import joblib
import os
import logging
from django.conf import settings

# ロガーの設定
logger = logging.getLogger(__name__)

# モデルのロード（サーバー起動時に1回実行）
MODEL_PATH = os.path.join(settings.BASE_DIR, 'diabetes_prediction_joblib.pkl')
try:
    classifier_model = joblib.load(MODEL_PATH)
except Exception as e:
    logger.error(f"モデルの読み込みに失敗しました: {e}")
    classifier_model = None

def home(request):
    return render(request, 'home.html')

def predict(request):
    """ 推論・保存・結果表示を統合したメインビュー """
    if request.method == 'POST':
        form = DiabetesPredictionForm(request.POST)
        if form.is_valid():
            # モデルがロードされていない場合のガード
            if not classifier_model:
                messages.error(request, "予測モデルが準備できていません。管理者にお問い合わせください。")
                return redirect('predict:predict')

            # 1. データの抽出（辞書から直接リスト化）
            data = form.cleaned_data
            input_features = [
                data['Pregnancies'], data['Glucose'], data['Blood_Pressure'],
                data['Skin_Thickness'], data['Insulin'], data['BMI'],
                data['Diabetes_Pedigree_Function'], data['Age']
            ]
            
            # 2. 推論実行
            input_data = [input_features]
            pred = classifier_model.predict(input_data)[0]
            
            # 確率の計算（対応していない場合は None）
            probability = None
            if hasattr(classifier_model, "predict_proba"):
                try:
                    prob_val = classifier_model.predict_proba(input_data)[0][1] * 100
                    probability = f"{prob_val:.1f}%"
                except Exception:
                    pass

            result_text = '陽性' if pred == 1 else '陰性'

            # 3. DB保存
            instance = form.save(commit=False)
            instance.Result = result_text
            instance.save()
            
            # 成功メッセージ（必要に応じて表示）
            messages.success(request, "判定が正常に完了し、保存されました。")

            # 4. 結果表示
            context = {
                'result': result_text,
                'probability': probability,
                'data': data,
            }
            return render(request, 'result.html', context)
    else:
        form = DiabetesPredictionForm()

    return render(request, 'predict.html', {'form': form})

def view_data(request):
    """ 履歴一覧を表示（ページネーションなどの拡張も可能） """
    predictions = DiabetesPrediction.objects.all().order_by('-created_at')
    return render(request, "data_base.html", {"dataset": predictions})

def exportcsv(request):
    """ 判定履歴をCSVとしてダウンロード（Excel対応） """
    response = HttpResponse(content_type='text/csv; charset=cp932')
    response['Content-Disposition'] = 'attachment; filename=diabetes_results.csv'
    
    writer = csv.writer(response)
    writer.writerow(['ID', '判定日時', '妊娠回数', 'グルコース', '血圧', '皮膚の厚み', 'インシュリン', 'BMI', '家系係数', '年齢', '判定結果'])
    
    # 効率的な一括取得
    predictions = DiabetesPrediction.objects.all().order_by('-created_at')
    
    for p in predictions:
        writer.writerow([
            p.id,
            p.created_at.strftime('%Y-%m-%d %H:%M'),
            p.Pregnancies, p.Glucose, p.Blood_Pressure,
            p.Skin_Thickness, p.Insulin, p.BMI,
            p.Diabetes_Pedigree_Function, p.Age, p.Result
        ])
        
    return response

def view_pima_indian(request):
    return render(request, 'pima_indian.html')
