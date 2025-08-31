# KDD Cup 1999 IDS - Uçtan Uca Proje Kiti

Bu proje, KDD Cup 1999 veri kümesi kullanılarak iki aşamalı bir siber saldırı tespit sistemi geliştirmeyi amaçlamaktadır:

1. **Binary Sınıflandırma**: Ağ trafiğinin normal mi yoksa saldırı mı olduğunu tespit etme
2. **Multi-class Sınıflandırma**: Tespit edilen saldırıların hangi aileye (DoS, Probe, R2L, U2R) ait olduğunu belirleme

## 📁 Proje Yapısı

```
kdd-cup-1999-ids/
├── data/                          # Veri dosyaları
│   ├── kddcup.data_10_percent.gz  # Eğitim verisi
│   ├── corrected.gz               # Test verisi
│   └── kddcup.names.txt          # Özellik isimleri
├── notebooks/                     # Jupyter notebook'ları
│   ├── 01_eda.ipynb              # Keşifsel Veri Analizi
│   ├── 02_binary_attack_detection.ipynb  # Binary sınıflandırma
│   └── 03_multiclass_attack_family.ipynb # Multi-class sınıflandırma
├── src/                           # Kaynak kodlar
│   ├── __init__.py
│   ├── data.py                    # Veri yükleme fonksiyonları
│   ├── preprocess.py              # Ön işleme pipeline'ları
│   ├── models.py                  # Model pipeline'ları
│   ├── eval.py                    # Değerlendirme fonksiyonları
│   └── viz.py                     # Görselleştirme fonksiyonları
├── reports/                       # Raporlar ve görseller
│   ├── figures/                   # Grafik ve şekiller
│   └── report.md                  # Proje raporu
├── requirements.txt               # Python bağımlılıkları
└── README.md                      # Bu dosya
```

## 🚀 Hızlı Başlangıç

### 1. Gereksinimler

```bash
# Python 3.8+ gereklidir
pip install -r requirements.txt
```

### 2. Veri İndirme

KDD Cup 1999 veri setini indirin:

```bash
# data/ klasörüne gidin
cd data/

# Eğitim verisi
wget http://kdd.ics.uci.edu/databases/kddcup99/kddcup.data_10_percent.gz

# Test verisi
wget http://kdd.ics.uci.edu/databases/kddcup99/corrected.gz

# Özellik isimleri
wget http://kdd.ics.uci.edu/databases/kddcup99/kddcup.names -O kddcup.names.txt
```

### 3. Notebook'ları Çalıştırma

```bash
# Jupyter Lab'i başlatın
jupyter lab

# Sırasıyla notebook'ları çalıştırın:
# 1. notebooks/01_eda.ipynb
# 2. notebooks/02_binary_attack_detection.ipynb
# 3. notebooks/03_multiclass_attack_family.ipynb
```

## 📊 Veri Kümesi

### Özellikler
- **41 özellik** + 1 etiket kolonu
- **Kategorik özellikler**: `protocol_type`, `service`, `flag`
- **Sayısal özellikler**: 38 adet
- **Eğitim seti**: ~494,021 kayıt
- **Test seti**: ~311,029 kayıt

### Saldırı Türleri
- **Normal**: Normal ağ trafiği
- **DoS**: Denial of Service saldırıları
- **Probe**: Port tarama ve keşif saldırıları
- **R2L**: Remote to Local saldırıları
- **U2R**: User to Root saldırıları

## 🔧 Kullanım

### Veri Yükleme

```python
from src.data import load_kdd

# Eğitim verisi
train_df = load_kdd('data/kddcup.data_10_percent.gz')

# Test verisi
test_df = load_kdd('data/corrected.gz')
```

### Ön İşleme

```python
from src.preprocess import add_targets, split_features

# Hedef değişkenleri ekle
train_df = add_targets(train_df)

# Özellikleri ayır
X_train, y_binary, y_multi = split_features(train_df)
```

### Model Eğitimi

```python
from src.models import make_binary_pipelines, make_multiclass_pipelines

# Binary sınıflandırma modelleri
binary_models = make_binary_pipelines()

# Multi-class sınıflandırma modelleri
multi_models = make_multiclass_pipelines()

# Model eğitimi
for name, model in binary_models.items():
    model.fit(X_train, y_binary)
```

### Model Değerlendirme

```python
from src.eval import plot_roc_pr, plot_cm

# ROC ve PR eğrileri
plot_roc_pr(y_true, y_pred_proba)

# Confusion matrix
plot_cm(y_true, y_pred)
```

## 📈 Sonuçlar

### Binary Sınıflandırma
- **En İyi Model**: Random Forest
- **ROC AUC**: 0.992
- **F1 Score**: 0.979
- **Accuracy**: 0.976

### Multi-class Sınıflandırma
- **En İyi Model**: Random Forest
- **Macro F1**: 0.857
- **Weighted F1**: 0.968
- **Accuracy**: 0.935

## 🔍 Önemli Özellikler

**Top 5 Özellik** (Random Forest özellik önemleri):
1. `dst_host_srv_count`
2. `count`
3. `srv_count`
4. `dst_host_count`
5. `src_bytes`

## 📝 Notebook Açıklamaları

### 01_eda.ipynb - Keşifsel Veri Analizi
- Veri kümesi genel bakış
- Sınıf dağılımları
- Özellik analizi
- Korelasyon analizi
- Aykırı değer tespiti

### 02_binary_attack_detection.ipynb - Binary Sınıflandırma
- Veri hazırlama
- Model karşılaştırması (Logistic Regression vs Random Forest)
- Hiperparametre optimizasyonu
- Performans değerlendirmesi
- ROC ve PR eğrileri
- Eşik optimizasyonu

### 03_multiclass_attack_family.ipynb - Multi-class Sınıflandırma
- Saldırı ailesi sınıflandırması
- Model karşılaştırması
- Confusion matrix analizi
- Sınıf bazında performans
- Özellik önemleri
- Hata analizi

## 🛠️ Geliştirme

### Kod Yapısı
- `src/data.py`: Veri yükleme ve temel işlemler
- `src/preprocess.py`: Veri ön işleme pipeline'ları
- `src/models.py`: Model pipeline'ları ve hiperparametre aralıkları
- `src/eval.py`: Model değerlendirme ve görselleştirme
- `src/viz.py`: EDA görselleştirme fonksiyonları

### Test Etme

```bash
# Tüm modülleri test et
python -c "from src import data, preprocess, models, eval, viz; print('Tüm modüller başarıyla yüklendi!')"
```

## 📚 Referanslar

1. [KDD Cup 1999 Data](http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html)
2. [NSL-KDD Dataset](https://www.unb.ca/cic/datasets/nsl.html)
3. Tavallaee, M., et al. "A detailed analysis of the KDD CUP 99 data set." (2009)

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📞 İletişim

Sorularınız için issue açabilir veya pull request gönderebilirsiniz.

---

**Not**: Bu proje KDD Cup 1999 veri kümesi üzerinde akademik çalışma amaçlı geliştirilmiştir. Gerçek üretim ortamlarında kullanmadan önce güncel veri setleri ve yöntemler ile test edilmelidir.