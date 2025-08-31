#!/usr/bin/env python3
"""
KDD Cup 1999 Proje Özet Görselleştirmeleri
Bu script, proje sonuçlarını özetleyen görselleştirmeler oluşturur.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path

# Stil ayarları
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# Çıktı dizini
output_dir = Path('reports/figures')
output_dir.mkdir(exist_ok=True)

def create_class_distribution_plot():
    """Sınıf dağılımı görselleştirmesi"""
    # Veri
    classes = ['DoS', 'Normal', 'Probe', 'R2L', 'U2R']
    counts = [391458, 97278, 4107, 1126, 52]
    percentages = [79.24, 19.69, 0.83, 0.23, 0.01]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Bar plot
    bars = ax1.bar(classes, counts, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
    ax1.set_title('Sınıf Dağılımı (Eğitim Seti)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Örnek Sayısı')
    ax1.set_yscale('log')
    
    # Değerleri bar'ların üzerine yaz
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{count:,}',
                ha='center', va='bottom')
    
    # Pie chart
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    wedges, texts, autotexts = ax2.pie(percentages, labels=classes, autopct='%1.2f%%',
                                      colors=colors, startangle=90)
    ax2.set_title('Sınıf Dağılımı (Yüzde)', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'class_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Sınıf dağılımı grafiği oluşturuldu")

def create_model_performance_comparison():
    """Model performans karşılaştırması"""
    # Binary sınıflandırma sonuçları
    binary_data = {
        'Model': ['Logistic Regression', 'Random Forest'],
        'F1 Score': [0.9498, 0.9524],
        'ROC AUC': [0.9706, 0.9795],
        'Precision': [0.9216, 0.9264],
        'Recall': [0.9806, 0.9806]
    }
    
    # Multiclass sınıflandırma sonuçları
    multiclass_data = {
        'Model': ['Logistic Regression', 'Random Forest'],
        'Macro F1': [0.5754, 0.5581],
        'Weighted F1': [0.9137, 0.9209],
        'Accuracy': [0.9357, 0.9406]
    }
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Binary Classification Metrics
    binary_df = pd.DataFrame(binary_data)
    metrics = ['F1 Score', 'ROC AUC', 'Precision', 'Recall']
    x = np.arange(len(metrics))
    width = 0.35
    
    lr_values = [binary_df.loc[0, metric] for metric in metrics]
    rf_values = [binary_df.loc[1, metric] for metric in metrics]
    
    ax1.bar(x - width/2, lr_values, width, label='Logistic Regression', color='#FF6B6B', alpha=0.8)
    ax1.bar(x + width/2, rf_values, width, label='Random Forest', color='#4ECDC4', alpha=0.8)
    
    ax1.set_title('Binary Sınıflandırma Performansı', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Skor')
    ax1.set_xticks(x)
    ax1.set_xticklabels(metrics)
    ax1.legend()
    ax1.set_ylim(0.9, 1.0)
    
    # Değerleri bar'ların üzerine yaz
    for i, (lr_val, rf_val) in enumerate(zip(lr_values, rf_values)):
        ax1.text(i - width/2, lr_val + 0.002, f'{lr_val:.4f}', ha='center', va='bottom', fontsize=10)
        ax1.text(i + width/2, rf_val + 0.002, f'{rf_val:.4f}', ha='center', va='bottom', fontsize=10)
    
    # Multiclass Classification Metrics
    multiclass_df = pd.DataFrame(multiclass_data)
    mc_metrics = ['Macro F1', 'Weighted F1', 'Accuracy']
    x_mc = np.arange(len(mc_metrics))
    
    lr_mc_values = [multiclass_df.loc[0, metric] for metric in mc_metrics]
    rf_mc_values = [multiclass_df.loc[1, metric] for metric in mc_metrics]
    
    ax2.bar(x_mc - width/2, lr_mc_values, width, label='Logistic Regression', color='#FF6B6B', alpha=0.8)
    ax2.bar(x_mc + width/2, rf_mc_values, width, label='Random Forest', color='#4ECDC4', alpha=0.8)
    
    ax2.set_title('Multi-class Sınıflandırma Performansı', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Skor')
    ax2.set_xticks(x_mc)
    ax2.set_xticklabels(mc_metrics)
    ax2.legend()
    ax2.set_ylim(0, 1.0)
    
    # Değerleri bar'ların üzerine yaz
    for i, (lr_val, rf_val) in enumerate(zip(lr_mc_values, rf_mc_values)):
        ax2.text(i - width/2, lr_val + 0.02, f'{lr_val:.4f}', ha='center', va='bottom', fontsize=10)
        ax2.text(i + width/2, rf_val + 0.02, f'{rf_val:.4f}', ha='center', va='bottom', fontsize=10)
    
    # Sınıf bazında F1 skorları (Multiclass)
    class_f1_data = {
        'Sınıf': ['DoS', 'Normal', 'Probe', 'R2L', 'U2R'],
        'F1 Score': [0.9949, 0.8596, 0.8248, 0.0298, 0.1681],
        'Support': [112426, 30296, 2036, 8192, 105]
    }
    
    class_df = pd.DataFrame(class_f1_data)
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    bars = ax3.bar(class_df['Sınıf'], class_df['F1 Score'], color=colors, alpha=0.8)
    ax3.set_title('Sınıf Bazında F1 Skorları (Multi-class)', fontsize=14, fontweight='bold')
    ax3.set_ylabel('F1 Score')
    ax3.set_ylim(0, 1.0)
    
    # Değerleri bar'ların üzerine yaz
    for bar, f1_score in zip(bars, class_df['F1 Score']):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{f1_score:.4f}',
                ha='center', va='bottom', fontsize=10)
    
    # Support sayıları (log scale)
    bars2 = ax4.bar(class_df['Sınıf'], class_df['Support'], color=colors, alpha=0.8)
    ax4.set_title('Sınıf Bazında Örnek Sayıları (Test Seti)', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Örnek Sayısı (log scale)')
    ax4.set_yscale('log')
    
    # Değerleri bar'ların üzerine yaz
    for bar, support in zip(bars2, class_df['Support']):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height * 1.1,
                f'{support:,}',
                ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'model_performance_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Model performans karşılaştırması grafiği oluşturuldu")

def create_data_quality_summary():
    """Veri kalitesi özeti"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Duplikasyon oranı
    labels = ['Tekrar Eden', 'Benzersiz']
    sizes = [70.53, 29.47]
    colors = ['#FF6B6B', '#4ECDC4']
    
    wedges, texts, autotexts = ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                                      colors=colors, startangle=90)
    ax1.set_title('Veri Duplikasyon Oranı', fontsize=14, fontweight='bold')
    
    # Sınıf dengesizliği (log scale)
    classes = ['DoS', 'Normal', 'Probe', 'R2L', 'U2R']
    counts = [391458, 97278, 4107, 1126, 52]
    colors_class = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    bars = ax2.bar(classes, counts, color=colors_class, alpha=0.8)
    ax2.set_title('Sınıf Dengesizliği (Log Scale)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Örnek Sayısı (log scale)')
    ax2.set_yscale('log')
    ax2.tick_params(axis='x', rotation=45)
    
    # Kategorik değişken çeşitliliği
    categorical_vars = ['protocol_type', 'service', 'flag']
    unique_counts = [3, 70, 11]
    
    bars3 = ax3.bar(categorical_vars, unique_counts, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.8)
    ax3.set_title('Kategorik Değişken Çeşitliliği', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Benzersiz Değer Sayısı')
    
    for bar, count in zip(bars3, unique_counts):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{count}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Veri seti boyutları
    datasets = ['Eğitim Seti', 'Test Seti']
    sizes_data = [494021, 311029]
    
    bars4 = ax4.bar(datasets, sizes_data, color=['#FF6B6B', '#4ECDC4'], alpha=0.8)
    ax4.set_title('Veri Seti Boyutları', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Kayıt Sayısı')
    
    for bar, size in zip(bars4, sizes_data):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 5000,
                f'{size:,}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'data_quality_summary.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Veri kalitesi özeti grafiği oluşturuldu")

def create_project_summary_infographic():
    """Proje özeti infografiği"""
    fig = plt.figure(figsize=(16, 20))
    
    # Ana başlık
    fig.suptitle('KDD Cup 1999 IDS Projesi - Özet Sonuçlar', 
                fontsize=24, fontweight='bold', y=0.98)
    
    # Grid layout
    gs = fig.add_gridspec(6, 2, height_ratios=[1, 1, 1, 1, 1, 0.5], hspace=0.3, wspace=0.2)
    
    # 1. Veri Seti Bilgileri
    ax1 = fig.add_subplot(gs[0, :])
    ax1.text(0.5, 0.8, 'VERI SETİ BİLGİLERİ', ha='center', va='center', 
            fontsize=18, fontweight='bold', transform=ax1.transAxes)
    
    info_text = (
        "• Eğitim Seti: 494,021 kayıt × 42 özellik\n"
        "• Test Seti: 311,029 kayıt × 42 özellik\n"
        "• 5 sınıf: Normal, DoS, Probe, R2L, U2R\n"
        "• Duplikasyon Oranı: %70.53\n"
        "• Ciddi sınıf dengesizliği mevcut"
    )
    
    ax1.text(0.5, 0.3, info_text, ha='center', va='center', 
            fontsize=14, transform=ax1.transAxes,
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.7))
    ax1.axis('off')
    
    # 2. Binary Sınıflandırma Sonuçları
    ax2 = fig.add_subplot(gs[1, 0])
    binary_metrics = ['F1 Score', 'ROC AUC', 'Precision', 'Recall']
    binary_values = [0.9524, 0.9795, 0.9264, 0.9806]
    
    bars = ax2.barh(binary_metrics, binary_values, color='#4ECDC4', alpha=0.8)
    ax2.set_title('Binary Sınıflandırma\n(Random Forest)', fontsize=14, fontweight='bold')
    ax2.set_xlim(0.9, 1.0)
    
    for i, (bar, value) in enumerate(zip(bars, binary_values)):
        ax2.text(value + 0.002, i, f'{value:.4f}', va='center', fontweight='bold')
    
    # 3. Multi-class Sınıflandırma Sonuçları
    ax3 = fig.add_subplot(gs[1, 1])
    mc_metrics = ['Macro F1', 'Weighted F1', 'Accuracy']
    mc_values = [0.5754, 0.9137, 0.9357]
    
    bars = ax3.barh(mc_metrics, mc_values, color='#FF6B6B', alpha=0.8)
    ax3.set_title('Multi-class Sınıflandırma\n(Logistic Regression)', fontsize=14, fontweight='bold')
    ax3.set_xlim(0, 1.0)
    
    for i, (bar, value) in enumerate(zip(bars, mc_values)):
        ax3.text(value + 0.02, i, f'{value:.4f}', va='center', fontweight='bold')
    
    # 4. Sınıf Bazında Performans
    ax4 = fig.add_subplot(gs[2, :])
    classes = ['DoS', 'Normal', 'Probe', 'R2L', 'U2R']
    f1_scores = [0.9949, 0.8596, 0.8248, 0.0298, 0.1681]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    bars = ax4.bar(classes, f1_scores, color=colors, alpha=0.8)
    ax4.set_title('Sınıf Bazında F1 Skorları (Multi-class)', fontsize=14, fontweight='bold')
    ax4.set_ylabel('F1 Score')
    ax4.set_ylim(0, 1.0)
    
    for bar, f1_score in zip(bars, f1_scores):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{f1_score:.4f}',
                ha='center', va='bottom', fontweight='bold')
    
    # 5. Temel Bulgular
    ax5 = fig.add_subplot(gs[3, :])
    ax5.text(0.5, 0.9, 'TEMEL BULGULAR', ha='center', va='center', 
            fontsize=18, fontweight='bold', transform=ax5.transAxes)
    
    findings_text = (
        "✓ Binary sınıflandırma için yüksek performans (F1: 0.9524)\n"
        "✓ DoS saldırıları mükemmel tespit edildi (F1: 0.9949)\n"
        "✗ R2L ve U2R sınıfları için düşük performans\n"
        "✗ Ciddi sınıf dengesizliği problemi\n"
        "✗ Yüksek duplikasyon oranı (%70.53)"
    )
    
    ax5.text(0.5, 0.4, findings_text, ha='center', va='center', 
            fontsize=14, transform=ax5.transAxes,
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.7))
    ax5.axis('off')
    
    # 6. Öneriler
    ax6 = fig.add_subplot(gs[4, :])
    ax6.text(0.5, 0.9, 'ÖNERİLER', ha='center', va='center', 
            fontsize=18, fontweight='bold', transform=ax6.transAxes)
    
    recommendations_text = (
        "• Gelişmiş sınıf dengeleme teknikleri (ADASYN, BorderlineSMOTE)\n"
        "• Cost-sensitive learning parametrelerinin optimizasyonu\n"
        "• XGBoost, LightGBM gibi gradient boosting yöntemleri\n"
        "• Modern veri setleri ile test (NSL-KDD, CICIDS-2017)\n"
        "• Deep learning yaklaşımlarının denenmesi"
    )
    
    ax6.text(0.5, 0.4, recommendations_text, ha='center', va='center', 
            fontsize=14, transform=ax6.transAxes,
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgreen', alpha=0.7))
    ax6.axis('off')
    
    # 7. Footer
    ax7 = fig.add_subplot(gs[5, :])
    ax7.text(0.5, 0.5, 'KDD Cup 1999 IDS Projesi - Siber Saldırı Tespit Sistemi', 
            ha='center', va='center', fontsize=12, style='italic', 
            transform=ax7.transAxes)
    ax7.axis('off')
    
    plt.savefig(output_dir / 'project_summary_infographic.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("✓ Proje özeti infografiği oluşturuldu")

def main():
    """Ana fonksiyon"""
    print("KDD Cup 1999 Proje Görselleştirmeleri Oluşturuluyor...\n")
    
    try:
        create_class_distribution_plot()
        print()
        
        create_model_performance_comparison()
        print()
        
        create_data_quality_summary()
        print()
        
        create_project_summary_infographic()
        print()
        
        print("🎉 Tüm görselleştirmeler başarıyla oluşturuldu!")
        print(f"📁 Dosyalar şu dizinde: {output_dir.absolute()}")
        
        # Oluşturulan dosyaları listele
        created_files = list(output_dir.glob('*.png'))
        if created_files:
            print("\n📊 Oluşturulan görselleştirmeler:")
            for file in created_files:
                print(f"   • {file.name}")
        
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")
        raise

if __name__ == "__main__":
    main()