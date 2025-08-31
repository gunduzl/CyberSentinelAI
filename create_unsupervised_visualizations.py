#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unsupervised Anomali Tespiti Görselleştirmeleri
KDD Cup 1999 - 04_network_anomaly_detection.ipynb sonuçları için
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

# Türkçe font desteği
plt.rcParams['font.family'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Renk paleti
colors = {
    'primary': '#2E86AB',
    'secondary': '#A23B72', 
    'accent': '#F18F01',
    'success': '#C73E1D',
    'warning': '#F4B942',
    'info': '#5D737E',
    'light': '#F5F5F5',
    'dark': '#2C3E50'
}

def create_unsupervised_performance_comparison():
    """
    Unsupervised algoritmaların performans karşılaştırması
    """
    # Notebook'tan alınan sonuçlar
    data = {
        'Algorithm': ['K-means', 'DBSCAN', 'Isolation Forest', 'One-Class SVM', 'LOF'],
        'Accuracy': [0.214, 0.233, 0.975, 0.979, 0.980],
        'Precision': [0.736, 0.926, 0.976, 0.978, 0.979],
        'Recall': [0.045, 0.057, 0.994, 0.997, 0.997],
        'F1-Score': [0.086, 0.108, 0.985, 0.987, 0.988],
        'ROC-AUC': [0.811, 0.969, 0.944, 0.964, 0.974],
        'Detected_Anomalies': [500, 499, 8245, 8253, 8242]
    }
    
    df = pd.DataFrame(data)
    
    # Büyük figür oluştur
    fig = plt.figure(figsize=(20, 12))
    gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)
    
    # Ana başlık
    fig.suptitle('Unsupervised Anomali Tespiti - Algoritma Performans Karşılaştırması\nKDD Cup 1999 Veri Seti', 
                 fontsize=20, fontweight='bold', y=0.95)
    
    # 1. F1-Score karşılaştırması
    ax1 = fig.add_subplot(gs[0, 0])
    bars1 = ax1.bar(df['Algorithm'], df['F1-Score'], 
                   color=[colors['primary'], colors['secondary'], colors['accent'], 
                         colors['success'], colors['warning']], alpha=0.8)
    ax1.set_title('F1-Score Karşılaştırması', fontsize=14, fontweight='bold')
    ax1.set_ylabel('F1-Score')
    ax1.set_ylim(0, 1.1)
    ax1.tick_params(axis='x', rotation=45)
    
    # Değerleri bar üzerine yaz
    for bar, value in zip(bars1, df['F1-Score']):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
    
    # 2. ROC-AUC karşılaştırması
    ax2 = fig.add_subplot(gs[0, 1])
    bars2 = ax2.bar(df['Algorithm'], df['ROC-AUC'], 
                   color=[colors['primary'], colors['secondary'], colors['accent'], 
                         colors['success'], colors['warning']], alpha=0.8)
    ax2.set_title('ROC-AUC Karşılaştırması', fontsize=14, fontweight='bold')
    ax2.set_ylabel('ROC-AUC')
    ax2.set_ylim(0, 1.1)
    ax2.tick_params(axis='x', rotation=45)
    
    for bar, value in zip(bars2, df['ROC-AUC']):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
    
    # 3. Precision vs Recall scatter
    ax3 = fig.add_subplot(gs[0, 2])
    scatter = ax3.scatter(df['Precision'], df['Recall'], 
                         c=[colors['primary'], colors['secondary'], colors['accent'], 
                           colors['success'], colors['warning']], 
                         s=200, alpha=0.8, edgecolors='black', linewidth=2)
    
    # Algoritma isimlerini ekle
    for i, txt in enumerate(df['Algorithm']):
        ax3.annotate(txt, (df['Precision'][i], df['Recall'][i]), 
                    xytext=(5, 5), textcoords='offset points', fontsize=10)
    
    ax3.set_xlabel('Precision')
    ax3.set_ylabel('Recall')
    ax3.set_title('Precision vs Recall', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(0, 1.05)
    ax3.set_ylim(0, 1.05)
    
    # 4. Tespit edilen anomali sayıları
    ax4 = fig.add_subplot(gs[1, :])
    bars4 = ax4.bar(df['Algorithm'], df['Detected_Anomalies'], 
                   color=[colors['primary'], colors['secondary'], colors['accent'], 
                         colors['success'], colors['warning']], alpha=0.8)
    ax4.set_title('Tespit Edilen Anomali Sayıları', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Anomali Sayısı')
    ax4.tick_params(axis='x', rotation=45)
    
    for bar, value in zip(bars4, df['Detected_Anomalies']):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100, 
                f'{value:,}', ha='center', va='bottom', fontweight='bold')
    
    # 5. Radar chart - En iyi 3 algoritma
    ax5 = fig.add_subplot(gs[2, :], projection='polar')
    
    # En iyi 3 algoritma (F1-Score'a göre)
    top3 = df.nlargest(3, 'F1-Score')
    
    metrics = ['F1-Score', 'ROC-AUC', 'Precision', 'Recall', 'Accuracy']
    angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
    angles += angles[:1]  # Döngüyü kapat
    
    colors_radar = [colors['accent'], colors['success'], colors['warning']]
    
    for i, (idx, row) in enumerate(top3.iterrows()):
        values = [row['F1-Score'], row['ROC-AUC'], row['Precision'], row['Recall'], row['Accuracy']]
        values += values[:1]  # Döngüyü kapat
        
        ax5.plot(angles, values, 'o-', linewidth=2, label=row['Algorithm'], 
                color=colors_radar[i], markersize=8)
        ax5.fill(angles, values, alpha=0.25, color=colors_radar[i])
    
    ax5.set_xticks(angles[:-1])
    ax5.set_xticklabels(metrics)
    ax5.set_ylim(0, 1)
    ax5.set_title('En İyi 3 Algoritma - Çok Boyutlu Performans', 
                 fontsize=14, fontweight='bold', pad=20)
    ax5.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    ax5.grid(True)
    
    # Genel bilgi kutusu
    info_text = (
        "📊 TEMEL BULGULAR:\n"
        "• En İyi Genel Performans: LOF (F1: 0.988)\n"
        "• En Yüksek ROC-AUC: LOF (0.974)\n"
        "• En Dengeli Sonuç: One-Class SVM\n"
        "• K-means ve DBSCAN: Düşük performans\n\n"
        "⚠️  ÖNEMLI NOTLAR:\n"
        "• Test seti: 10,000 örnek (8,245 anomali)\n"
        "• Contamination oranı: %10\n"
        "• PCA ile boyut indirgeme uygulandı"
    )
    
    plt.figtext(0.02, 0.02, info_text, fontsize=11, 
                bbox=dict(boxstyle="round,pad=0.5", facecolor=colors['light'], alpha=0.8),
                verticalalignment='bottom')
    
    plt.tight_layout()
    plt.savefig('/Users/gunduz/Desktop/odev-kdd/reports/figures/unsupervised_anomaly_performance.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    print("✅ Unsupervised anomali tespiti performans karşılaştırması oluşturuldu!")

def create_algorithm_analysis_infographic():
    """
    Algoritma analizi infografiği
    """
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Ana başlık
    ax.text(5, 9.5, 'Unsupervised Anomali Tespiti Algoritmaları', 
            fontsize=24, fontweight='bold', ha='center')
    ax.text(5, 9.1, 'KDD Cup 1999 - Detaylı Analiz ve Karşılaştırma', 
            fontsize=16, ha='center', style='italic')
    
    # Algoritma kutuları
    algorithms = [
        {
            'name': 'Local Outlier Factor (LOF)',
            'pos': (0.5, 7.5),
            'color': colors['warning'],
            'f1': '0.988',
            'auc': '0.974',
            'pros': ['En yüksek F1-Score', 'Mükemmel Recall (0.997)', 'Yerel yoğunluk analizi'],
            'cons': ['Hesaplama maliyeti yüksek', 'Parametre hassasiyeti']
        },
        {
            'name': 'One-Class SVM',
            'pos': (5.5, 7.5),
            'color': colors['success'],
            'f1': '0.987',
            'auc': '0.964',
            'pros': ['Çok iyi F1-Score', 'Güçlü teorik temel', 'Non-linear sınırlar'],
            'cons': ['Kernel seçimi kritik', 'Büyük veri setlerinde yavaş']
        },
        {
            'name': 'Isolation Forest',
            'pos': (0.5, 5),
            'color': colors['accent'],
            'f1': '0.985',
            'auc': '0.944',
            'pros': ['Hızlı eğitim', 'Ölçeklenebilir', 'Az parametre'],
            'cons': ['Orta seviye AUC', 'Yüksek boyutlarda zorlanır']
        },
        {
            'name': 'DBSCAN',
            'pos': (5.5, 5),
            'color': colors['secondary'],
            'f1': '0.108',
            'auc': '0.969',
            'pros': ['Yüksek Precision (0.926)', 'Küme şekli esnekliği'],
            'cons': ['Çok düşük Recall (0.057)', 'Parametre hassasiyeti']
        },
        {
            'name': 'K-means',
            'pos': (3, 2.5),
            'color': colors['primary'],
            'f1': '0.086',
            'auc': '0.811',
            'pros': ['Basit ve hızlı', 'Az bellek kullanımı'],
            'cons': ['En düşük performans', 'Küresel kümeler varsayımı']
        }
    ]
    
    for alg in algorithms:
        x, y = alg['pos']
        
        # Ana kutu
        rect = Rectangle((x, y), 4, 1.8, linewidth=2, 
                        edgecolor=alg['color'], facecolor=alg['color'], alpha=0.1)
        ax.add_patch(rect)
        
        # Algoritma adı
        ax.text(x + 2, y + 1.5, alg['name'], fontsize=14, fontweight='bold', 
                ha='center', color=alg['color'])
        
        # Performans metrikleri
        ax.text(x + 0.1, y + 1.2, f"F1-Score: {alg['f1']}", fontsize=11, fontweight='bold')
        ax.text(x + 0.1, y + 1.0, f"ROC-AUC: {alg['auc']}", fontsize=11, fontweight='bold')
        
        # Avantajlar
        ax.text(x + 0.1, y + 0.7, "✅ Avantajlar:", fontsize=10, fontweight='bold', color='green')
        for i, pro in enumerate(alg['pros']):
            ax.text(x + 0.2, y + 0.5 - i*0.15, f"• {pro}", fontsize=9)
        
        # Dezavantajlar
        ax.text(x + 0.1, y + 0.1, "❌ Dezavantajlar:", fontsize=10, fontweight='bold', color='red')
        for i, con in enumerate(alg['cons']):
            ax.text(x + 0.2, y - 0.1 - i*0.15, f"• {con}", fontsize=9)
    
    # Genel değerlendirme kutusu
    eval_rect = Rectangle((0.5, 0.2), 9, 1.5, linewidth=2, 
                         edgecolor=colors['dark'], facecolor=colors['light'], alpha=0.8)
    ax.add_patch(eval_rect)
    
    ax.text(5, 1.5, '🎯 GENEL DEĞERLENDİRME VE ÖNERİLER', 
            fontsize=16, fontweight='bold', ha='center')
    
    recommendations = [
        "1. 🏆 En İyi Seçim: LOF - Tüm metriklerde üstün performans",
        "2. 🥈 İkinci Seçenek: One-Class SVM - Dengeli ve güvenilir sonuçlar",
        "3. ⚡ Hız Önceliği: Isolation Forest - Hızlı ve etkili",
        "4. 🎯 Yüksek Precision: DBSCAN - False positive'leri minimize eder",
        "5. ❌ Önerilmez: K-means - Bu veri seti için uygun değil"
    ]
    
    for i, rec in enumerate(recommendations):
        ax.text(0.7, 1.2 - i*0.15, rec, fontsize=11)
    
    plt.tight_layout()
    plt.savefig('/Users/gunduz/Desktop/odev-kdd/reports/figures/unsupervised_algorithm_analysis.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    print("✅ Algoritma analizi infografiği oluşturuldu!")

def create_methodology_summary():
    """
    Metodoloji özeti görselleştirmesi
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Ana başlık
    ax.text(5, 9.5, 'Unsupervised Anomali Tespiti - Metodoloji', 
            fontsize=20, fontweight='bold', ha='center')
    ax.text(5, 9.1, 'KDD Cup 1999 Veri Seti Üzerinde Kapsamlı Analiz', 
            fontsize=14, ha='center', style='italic')
    
    # Veri işleme akışı
    steps = [
        {'title': '1. VERİ ÖN İŞLEME', 'pos': (1, 8), 'color': colors['primary'],
         'details': ['• 494,021 eğitim örneği', '• 41 özellik', '• StandardScaler normalizasyon', '• PCA boyut indirgeme']},
        
        {'title': '2. MODEL EĞİTİMİ', 'pos': (5, 8), 'color': colors['secondary'],
         'details': ['• Sadece normal verilerle eğitim', '• 5 farklı algoritma', '• Hiperparametre optimizasyonu', '• Cross-validation']},
        
        {'title': '3. ANOMALI TESPİTİ', 'pos': (1, 5.5), 'color': colors['accent'],
         'details': ['• Test seti: 10,000 örnek', '• Anomali skorları hesaplama', '• Threshold belirleme', '• Binary sınıflandırma']},
        
        {'title': '4. PERFORMANS DEĞERLENDİRME', 'pos': (5, 5.5), 'color': colors['success'],
         'details': ['• F1-Score, ROC-AUC', '• Precision, Recall', '• Confusion Matrix', '• Algoritma karşılaştırması']}
    ]
    
    for step in steps:
        x, y = step['pos']
        
        # Ana kutu
        rect = Rectangle((x-0.5, y-1), 4, 2, linewidth=2, 
                        edgecolor=step['color'], facecolor=step['color'], alpha=0.1)
        ax.add_patch(rect)
        
        # Başlık
        ax.text(x+1.5, y+0.5, step['title'], fontsize=12, fontweight='bold', 
                ha='center', color=step['color'])
        
        # Detaylar
        for i, detail in enumerate(step['details']):
            ax.text(x-0.3, y+0.1-i*0.25, detail, fontsize=10)
    
    # Oklar
    ax.annotate('', xy=(4.5, 8), xytext=(3.5, 8), 
                arrowprops=dict(arrowstyle='->', lw=2, color=colors['dark']))
    ax.annotate('', xy=(1, 6.5), xytext=(1, 7), 
                arrowprops=dict(arrowstyle='->', lw=2, color=colors['dark']))
    ax.annotate('', xy=(4.5, 5.5), xytext=(3.5, 5.5), 
                arrowprops=dict(arrowstyle='->', lw=2, color=colors['dark']))
    
    # Sonuçlar kutusu
    results_rect = Rectangle((0.5, 1), 9, 2.5, linewidth=2, 
                           edgecolor=colors['warning'], facecolor=colors['warning'], alpha=0.1)
    ax.add_patch(results_rect)
    
    ax.text(5, 3, '📊 TEMEL SONUÇLAR', fontsize=16, fontweight='bold', ha='center', color=colors['warning'])
    
    results = [
        "🏆 En Başarılı: LOF (F1-Score: 0.988, ROC-AUC: 0.974)",
        "⚡ En Hızlı: Isolation Forest (Büyük veri setleri için ideal)",
        "🎯 En Hassas: DBSCAN (Precision: 0.926, az false positive)",
        "❌ En Zayıf: K-means (F1-Score: 0.086, bu problem için uygun değil)",
        "📈 Genel Trend: Ensemble yöntemler daha başarılı"
    ]
    
    for i, result in enumerate(results):
        ax.text(0.8, 2.6-i*0.25, result, fontsize=11)
    
    # Öneriler
    ax.text(5, 0.7, '💡 ÖNERİLER', fontsize=14, fontweight='bold', ha='center', color=colors['info'])
    ax.text(0.8, 0.4, "• Gerçek zamanlı sistemler için: Isolation Forest + LOF hibrit yaklaşımı", fontsize=10)
    ax.text(0.8, 0.2, "• Yüksek hassasiyet gerekli: DBSCAN + manuel threshold ayarı", fontsize=10)
    ax.text(0.8, 0.0, "• Genel amaçlı kullanım: LOF (en dengeli performans)", fontsize=10)
    
    plt.tight_layout()
    plt.savefig('/Users/gunduz/Desktop/odev-kdd/reports/figures/unsupervised_methodology_summary.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    print("✅ Metodoloji özeti görselleştirmesi oluşturuldu!")

if __name__ == "__main__":
    print("🎨 Unsupervised Anomali Tespiti Görselleştirmeleri Oluşturuluyor...")
    print("=" * 60)
    
    # Görselleştirmeleri oluştur
    create_unsupervised_performance_comparison()
    print()
    create_algorithm_analysis_infographic()
    print()
    create_methodology_summary()
    
    print("\n" + "=" * 60)
    print("✅ Tüm görselleştirmeler başarıyla oluşturuldu!")
    print("📁 Dosyalar: /Users/gunduz/Desktop/odev-kdd/reports/figures/")
    print("   • unsupervised_anomaly_performance.png")
    print("   • unsupervised_algorithm_analysis.png")
    print("   • unsupervised_methodology_summary.png")