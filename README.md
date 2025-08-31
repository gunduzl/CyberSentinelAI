# KDD Cup 1999 Siber Saldırı Tespit Sistemi

> **Kapsamlı Ağ Güvenliği Analizi ve Makine Öğrenmesi Uygulaması**

Bu proje, KDD Cup 1999 veri kümesi kullanılarak geliştirilmiş kapsamlı bir siber saldırı tespit sistemidir. Hem denetimli (supervised) hem de denetimsiz (unsupervised) makine öğrenmesi yöntemleri ile ağ trafiğindeki anomalileri ve saldırıları tespit etmeyi amaçlamaktadır.

## 🚀 Hızlı Başlangıç

```bash
# Projeyi klonlayın
git clone <repository-url>
cd kdd-cup-1999-ids

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Jupyter Lab'i başlatın
jupyter lab
```

## 📊 Temel Sonuçlar

- **İkili Sınıflandırma**: %97.6 doğruluk, F1-Score: 0.979
- **Çok Sınıflı Sınıflandırma**: %93.5 doğruluk, Weighted F1: 0.968
- **Anomali Tespiti**: LOF algoritması ile %98.8 F1-Score

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
│   ├── 03_multiclass_attack_family.ipynb # Multi-class sınıflandırma
│   └── 04_network_anomaly_detection.ipynb # Anomali tespiti
├── src/                           # Kaynak kodlar
│   ├── data.py                    # Veri yükleme fonksiyonları
│   ├── preprocess.py              # Ön işleme pipeline'ları
│   ├── models.py                  # Model pipeline'ları
│   ├── eval.py                    # Değerlendirme fonksiyonları
│   └── viz.py                     # Görselleştirme fonksiyonları
├── reports/                       # Raporlar ve görseller
│   ├── figures/                   # Grafik ve şekiller
│   └── report.md                  # Detaylı proje raporu
├── requirements.txt               # Python bağımlılıkları
└── README.md                      # Bu dosya
```

## 🎯 Proje Amaçları

1. **Binary Sınıflandırma**: Ağ trafiğinin normal mi yoksa saldırı mı olduğunu tespit etme
2. **Multi-class Sınıflandırma**: Tespit edilen saldırıların hangi aileye (DoS, Probe, R2L, U2R) ait olduğunu belirleme
3. **Unsupervised Anomali Tespiti**: Etiketli veri gerektirmeden anomali tespiti yapma

## 📈 Ana Bulgular

### İkili Sınıflandırma
- **En İyi Model**: Random Forest
- **F1-Score**: 0.952
- **ROC-AUC**: 0.980
- **Doğruluk**: %97.6

### Çok Sınıflı Sınıflandırma
- **En İyi Model**: Logistic Regression
- **Macro F1**: 0.575
- **Weighted F1**: 0.914
- **Doğruluk**: %93.6

### Anomali Tespiti (Unsupervised)
- **En İyi Model**: LOF (Local Outlier Factor)
- **F1-Score**: 0.988
- **ROC-AUC**: 0.974
- **Precision**: 0.979

## 🔧 Kullanım

### Veri Yükleme

```python
from src.data import load_kdd

# Eğitim verisi
train_df = load_kdd('data/kddcup.data_10_percent.gz')

# Test verisi
test_df = load_kdd('data/corrected.gz')
```

### Model Eğitimi

```python
from src.models import make_binary_pipelines
from src.preprocess import add_targets, split_features

# Veri hazırlama
train_df = add_targets(train_df)
X_train, y_binary, y_multi = split_features(train_df)

# Model eğitimi
binary_models = make_binary_pipelines()
for name, model in binary_models.items():
    model.fit(X_train, y_binary)
```

### Sonuçları Görüntüleme

```python
from src.eval import plot_roc_pr, plot_cm

# ROC ve PR eğrileri
plot_roc_pr(y_true, y_pred_proba)

# Confusion matrix
plot_cm(y_true, y_pred)
```

## 📊 Veri Kümesi

### Özellikler
- **41 özellik** + 1 etiket kolonu
- **Kategorik özellikler**: `protocol_type`, `service`, `flag`
- **Sayısal özellikler**: 38 adet
- **Eğitim seti**: ~494,021 kayıt
- **Test seti**: ~311,029 kayıt

### Saldırı Türleri
- **Normal**: Normal ağ trafiği (%19.7)
- **DoS**: Denial of Service saldırıları (%79.2)
- **Probe**: Port tarama ve keşif saldırıları (%0.8)
- **R2L**: Remote to Local saldırıları (%0.2)
- **U2R**: User to Root saldırıları (%0.01)

## 🔍 Önemli Özellikler

**Top 5 Özellik** (Random Forest özellik önemleri):
1. `dst_host_srv_count` - Hedef host servis sayısı
2. `count` - Aynı host ve servis bağlantı sayısı
3. `srv_count` - Aynı servis bağlantı sayısı
4. `dst_host_count` - Hedef host bağlantı sayısı
5. `src_bytes` - Kaynak byte sayısı

## 📝 Notebook Açıklamaları

### 01_eda.ipynb - Keşifsel Veri Analizi
- Veri kümesi genel bakış
- Sınıf dağılımları analizi
- Özellik korelasyon analizi
- Veri kalitesi değerlendirmesi

### 02_binary_attack_detection.ipynb - Binary Sınıflandırma
- İkili sınıflandırma modelleri
- Hiperparametre optimizasyonu
- ROC ve PR eğrileri
- Model performans karşılaştırması

### 03_multiclass_attack_family.ipynb - Multi-class Sınıflandırma
- Saldırı ailesi sınıflandırması
- Sınıf dengesizliği analizi
- Confusion matrix değerlendirmesi
- Özellik önemleri analizi

### 04_network_anomaly_detection.ipynb - Anomali Tespiti
- Unsupervised öğrenme yaklaşımları
- 5 farklı algoritma karşılaştırması
- Anomali tespit performansı
- Algoritma avantaj/dezavantaj analizi

## 🚨 Veri Kalitesi Sorunları

1. **Ciddi Sınıf Dengesizliği**: U2R sınıfı sadece 52 örnek (%0.01)
2. **Yüksek Duplikasyon**: Eğitim setinde %70.5 tekrar eden kayıt
3. **Sabit Kolonlar**: `num_outbound_cmds` gibi sıfır varyanslı kolonlar
4. **Aykırı Değerler**: Çok geniş aralıklarda değer dağılımları

## 🔬 Algoritma Karşılaştırması

### Supervised Yöntemler
| Model | Yaklaşım | F1-Score | ROC-AUC | Avantajlar |
|-------|----------|----------|---------|------------|
| Random Forest | Binary | 0.952 | 0.980 | Yüksek doğruluk, özellik önemleri |
| Logistic Regression | Multi-class | 0.575 | - | Hızlı, yorumlanabilir |

### Unsupervised Yöntemler
| Algoritma | F1-Score | ROC-AUC | Kullanım Alanı |
|-----------|----------|---------|----------------|
| LOF | 0.988 | 0.974 | Genel amaçlı anomali tespiti |
| One-Class SVM | 0.987 | 0.964 | Karmaşık veri dağılımları |
| Isolation Forest | 0.985 | 0.944 | Büyük veri setleri |

## 🎯 Sonuçlar ve Öneriler

### Başarılı Yönler
- İkili sınıflandırmada yüksek performans (%97.6 doğruluk)
- Unsupervised yöntemlerle etkili anomali tespiti
- DoS saldırıları için mükemmel tespit (F1: 0.995)

### İyileştirme Alanları
- R2L ve U2R sınıfları için düşük performans
- Sınıf dengesizliği problemi
- Veri kalitesi sorunları

### Gelecek Çalışmalar
- Modern veri setleri ile test (CICIDS-2017, UNSW-NB15)
- Deep learning yaklaşımları
- Gerçek zamanlı anomali tespiti
- Explainable AI entegrasyonu

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

**Not**: Detaylı analiz sonuçları, görselleştirmeler ve teknik açıklamalar için `reports/report.md` dosyasını inceleyiniz.

**Proje Durumu**: ✅ Tamamlandı (Ocak 2025)
**Versiyon**: 2.0 (Unsupervised Anomali Tespiti ile Genişletilmiş)