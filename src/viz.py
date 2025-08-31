# src/viz.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def zscore_outliers(df: pd.DataFrame, cols, threshold=3.0):
    """Z-score ile aykırı değerleri tespit eder.
    
    Args:
        df: Veri seti
        cols: İncelenecek kolonlar
        threshold: Z-score eşiği
        
    Returns:
        tuple: (aykırı_değerler, z_skorları)
    """
    Z = (df[cols] - df[cols].mean())/df[cols].std(ddof=0)
    mask = (np.abs(Z) > threshold).any(axis=1)
    return df[mask], Z


def boxplots(df: pd.DataFrame, cols, max_cols=6):
    """Seçilen kolonlar için boxplot çizer.
    
    Args:
        df: Veri seti
        cols: Çizilecek kolonlar
        max_cols: Maksimum kolon sayısı
    """
    cols = cols[:max_cols]
    for c in cols:
        plt.figure(figsize=(8, 6))
        df.boxplot(column=c)
        plt.title(f"Boxplot: {c}")
        plt.show()


def plot_attack_distribution(df: pd.DataFrame, target_col='y_binary'):
    """Saldırı dağılımını görselleştirir.
    
    Args:
        df: Veri seti
        target_col: Hedef değişken kolonu
    """
    plt.figure(figsize=(8, 6))
    df[target_col].value_counts().plot(kind='bar')
    plt.title('Saldırı vs Normal Dağılımı')
    plt.xlabel('Sınıf (0: Normal, 1: Attack)')
    plt.ylabel('Sayı')
    plt.xticks(rotation=0)
    plt.show()


def plot_service_attack_ratio(df: pd.DataFrame, top_n=10):
    """En sık kullanılan servislerde saldırı oranlarını gösterir.
    
    Args:
        df: Veri seti
        top_n: Gösterilecek servis sayısı
    """
    # En sık kullanılan servisleri bul
    top_services = df['service'].value_counts().head(top_n).index
    
    # Her servis için saldırı oranını hesapla
    service_attack_ratio = []
    for service in top_services:
        service_data = df[df['service'] == service]
        attack_ratio = service_data['y_binary'].mean()
        service_attack_ratio.append({'service': service, 'attack_ratio': attack_ratio})
    
    ratio_df = pd.DataFrame(service_attack_ratio)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=ratio_df, x='service', y='attack_ratio')
    plt.title(f'Top {top_n} Servislerde Saldırı Oranları')
    plt.xlabel('Servis')
    plt.ylabel('Saldırı Oranı')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_correlation_heatmap(df: pd.DataFrame, figsize=(12, 10)):
    """Sayısal değişkenler arası korelasyon ısı haritası çizer.
    
    Args:
        df: Veri seti
        figsize: Grafik boyutu
    """
    # Sadece sayısal kolonları al
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    plt.figure(figsize=figsize)
    correlation_matrix = df[numeric_cols].corr()
    sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', center=0)
    plt.title('Sayısal Değişkenler Arası Korelasyon')
    plt.tight_layout()
    plt.show()