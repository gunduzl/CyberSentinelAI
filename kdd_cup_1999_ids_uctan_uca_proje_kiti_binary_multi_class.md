# KDD Cup 1999 IDS – Uçtan Uca Proje Kiti (Binary + Multi‑Class)

Bu doküman, **KDD Cup 1999** veri kümesi ile iki aşamalı bir siber saldırı tespit projesini uçtan uca tamamlamanız için hazırlandı:

1) **Binary sınıflandırma:** *attack mı değil mi?*
2) **Multi‑class:** *attack ise hangi attack tipi?*  (isteğe göre **family**: DoS, Probe, R2L, U2R veya **spesifik 22+ alt saldırı ismi**)

Aşağıda; veri hazırlama, modelleme, değerlendirme, görselleştirme, notebook & repo iskeleti, rapor ve sunum şablonları yer alır. Kodlar **scikit‑learn** uyumludur ve “pipeline + CV + HPO” yaklaşımı ile verilir.

---

## 0) Proje klasör yapısı

```text
kdd99-ids/
├─ data/
│  ├─ kddcup.data_10_percent.gz          # train (örnek) – ham
│  ├─ corrected.gz                        # test  – ham
│  └─ names.txt                           # (opsiyonel) açıklama
├─ notebooks/
│  ├─ 01_eda.ipynb
│  ├─ 02_binary_attack_detection.ipynb
│  └─ 03_multiclass_attack_family.ipynb
├─ src/
│  ├─ data.py
│  ├─ preprocess.py
│  ├─ models.py
│  ├─ eval.py
│  └─ viz.py
├─ reports/
│  ├─ figures/
│  ├─ report.md
│  └─ slides-outline.md
├─ requirements.txt
└─ README.md
```

**requirements.txt (öneri)**
```txt
numpy
pandas
scikit-learn
imbalanced-learn
matplotlib
seaborn
```

> Not: Büyük veri için `xgboost`/`lightgbm` de ekleyebilirsiniz.

---

## 1) Veri setine hızlı bakış ve kolon isimleri

KDD’99’da **41 özellik** + **label** vardır. 3 kategorik: `protocol_type`, `service`, `flag`. Diğerleri sayısaldır.

```python
# src/data.py
import pandas as pd
from pathlib import Path

KDD_COLS = [
    'duration','protocol_type','service','flag','src_bytes','dst_bytes','land','wrong_fragment','urgent',
    'hot','num_failed_logins','logged_in','num_compromised','root_shell','su_attempted','num_root',
    'num_file_creations','num_shells','num_access_files','num_outbound_cmds','is_host_login','is_guest_login',
    'count','srv_count','serror_rate','srv_serror_rate','rerror_rate','srv_rerror_rate','same_srv_rate',
    'diff_srv_rate','srv_diff_host_rate','dst_host_count','dst_host_srv_count','dst_host_same_srv_rate',
    'dst_host_diff_srv_rate','dst_host_same_src_port_rate','dst_host_srv_diff_host_rate','dst_host_serror_rate',
    'dst_host_srv_serror_rate','dst_host_rerror_rate','dst_host_srv_rerror_rate','label'
]

ATTACK_FAMILY = {
    # DoS
    'back':'dos','land':'dos','neptune':'dos','pod':'dos','smurf':'dos','teardrop':'dos','apache2':'dos','udpstorm':'dos','processtable':'dos','worm':'dos',
    # Probe
    'satan':'probe','ipsweep':'probe','nmap':'probe','portsweep':'probe','mscan':'probe','saint':'probe',
    # R2L
    'ftp_write':'r2l','guess_passwd':'r2l','imap':'r2l','multihop':'r2l','phf':'r2l','spy':'r2l','warezclient':'r2l','warezmaster':'r2l','named':'r2l','sendmail':'r2l','snmpgetattack':'r2l','snmpguess':'r2l','worm':'r2l',
    # U2R
    'buffer_overflow':'u2r','loadmodule':'u2r','perl':'u2r','rootkit':'u2r','httptunnel':'u2r','ps':'u2r','sqlattack':'u2r','xterm':'u2r'
}


def load_kdd(path: str | Path, gz: bool = True) -> pd.DataFrame:
    path = Path(path)
    df = pd.read_csv(path, names=KDD_COLS, header=None, compression='gzip' if gz else None)
    return df
```

> **İpucu:** `num_outbound_cmds` çoğu kaynakta **hep 0** (sabit). Sıfır varyanslı kolonları tespit edip düşürmek faydalıdır.

---

## 2) Hedef tanımları (binary + multi‑class)

```python
# src/preprocess.py
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

BINARY_TARGET = 'y_binary'
MULTI_TARGET  = 'y_family'   # veya 'y_attack' (tek tek saldırı ismi)

CATEGORICAL = ['protocol_type','service','flag']

class ConstantDropper(BaseEstimator, TransformerMixin):
    """Sıfır varyanslı sayısal kolonları otomatik düşürür."""
    def __init__(self):
        self.keep_cols_ = None
    def fit(self, X, y=None):
        if isinstance(X, pd.DataFrame):
            nunique = X.nunique()
            self.keep_cols_ = nunique[nunique > 1].index.tolist()
        else:
            self.keep_cols_ = list(range(X.shape[1]))
        return self
    def transform(self, X):
        return X[self.keep_cols_]


def add_targets(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out[BINARY_TARGET] = (out['label'] != 'normal').astype(int)
    out['attack_name'] = out['label'].where(out['label']!='normal', other=np.nan)
    out[MULTI_TARGET]  = out['attack_name'].map(ATTACK_FAMILY)
    return out


def split_features(df: pd.DataFrame):
    X = df.drop(columns=['label','attack_name',BINARY_TARGET,MULTI_TARGET], errors='ignore')
    y_bin = df[BINARY_TARGET] if BINARY_TARGET in df else None
    y_family = df[MULTI_TARGET] if MULTI_TARGET in df else None
    num_cols = [c for c in X.columns if c not in CATEGORICAL]
    cat_cols = [c for c in X.columns if c in CATEGORICAL]
    return X, y_bin, y_family, num_cols, cat_cols
```

---

## 3) Pipeline ve Ön‑işleme

- **ColumnTransformer** ile sayısallara `StandardScaler`, kategoriklere `OneHotEncoder(handle_unknown='ignore')`.
- Sıfır varyanslı kolonları `ConstantDropper` ile at.
- **Sızıntı (leakage) önlemi:** Tüm dönüşümler **Pipeline** içinde ve **CV** sırasında fit edilmelidir.

```python
# src/models.py
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as IMBPipeline


def make_preprocessor(num_cols, cat_cols):
    numeric = Pipeline(steps=[
        ('scale', StandardScaler(with_mean=False))  # sparse ile uyumlu
    ])
    categorical = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    pre = ColumnTransformer([
        ('num', numeric, num_cols),
        ('cat', categorical, cat_cols)
    ], remainder='drop')
    return pre


def make_binary_pipelines(num_cols, cat_cols):
    pre = make_preprocessor(num_cols, cat_cols)

    pipe_lr = IMBPipeline(steps=[
        ('const_drop', ConstantDropper()),
        ('pre', pre),
        ('smote', SMOTE()),
        ('clf', LogisticRegression(max_iter=1000, n_jobs=None, class_weight='balanced'))
    ])

    pipe_rf = IMBPipeline(steps=[
        ('const_drop', ConstantDropper()),
        ('pre', pre),
        ('smote', SMOTE()),
        ('clf', RandomForestClassifier(class_weight='balanced'))
    ])

    pipe_gb = IMBPipeline(steps=[
        ('const_drop', ConstantDropper()),
        ('pre', pre),
        ('clf', GradientBoostingClassifier())  # SMOTE genelde ağaç dışı modellerle daha anlamlı
    ])

    grids = {
        'lr': (pipe_lr, {
            'clf__C': [0.1, 1, 3],
            'clf__solver': ['lbfgs','saga']
        }),
        'rf': (pipe_rf, {
            'clf__n_estimators': [200, 400],
            'clf__max_depth': [None, 20, 40],
            'clf__min_samples_split': [2, 10]
        }),
        'gb': (pipe_gb, {
            'clf__n_estimators': [150, 300],
            'clf__learning_rate': [0.05, 0.1],
            'clf__max_depth': [3, 5]
        })
    }
    return grids


def make_multiclass_pipelines(num_cols, cat_cols):
    pre = make_preprocessor(num_cols, cat_cols)

    pipe_lr = IMBPipeline(steps=[
        ('const_drop', ConstantDropper()),
        ('pre', pre),
        ('smote', SMOTE()),
        ('clf', LogisticRegression(max_iter=1000, multi_class='ovr'))
    ])

    pipe_rf = IMBPipeline(steps=[
        ('const_drop', ConstantDropper()),
        ('pre', pre),
        ('clf', RandomForestClassifier())
    ])

    grids = {
        'lr': (pipe_lr, {
            'clf__C': [0.5, 1, 2]
        }),
        'rf': (pipe_rf, {
            'clf__n_estimators': [300, 600],
            'clf__max_depth': [None, 20, 40]
        })
    }
    return grids
```

---

## 4) Eğitim/Test ayrımı ve HPO

- **Öneri:** KDD’99’un `kddcup.data_10_percent` dosyasını **eğitim**, `corrected` dosyasını **test** olarak kullanın.
- Eğitim sırasında **StratifiedKFold CV** ve **RandomizedSearchCV** / **GridSearchCV** ile hiperparametre arayın.

```python
# notebooks/02_binary_attack_detection.ipynb (çekirdek hücre)
import pandas as pd
from pathlib import Path
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.metrics import classification_report, roc_auc_score

from src.data import load_kdd
from src.preprocess import add_targets, split_features
from src.models import make_binary_pipelines

train = add_targets(load_kdd('data/kddcup.data_10_percent.gz'))
test  = add_targets(load_kdd('data/corrected.gz'))

X_tr, yb_tr, _, num_cols, cat_cols = split_features(train)
X_te, yb_te, _, _, _               = split_features(test)

grids = make_binary_pipelines(num_cols, cat_cols)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

results = []
for name, (pipe, param_grid) in grids.items():
    search = GridSearchCV(
        estimator=pipe,
        param_grid=param_grid,
        scoring='f1',
        cv=cv,
        n_jobs=-1,
        verbose=1
    )
    search.fit(X_tr, yb_tr)

    y_pred = search.best_estimator_.predict(X_te)
    y_proba = getattr(search.best_estimator_, 'predict_proba', None)
    auc = roc_auc_score(yb_te, y_proba(X_te)[:,1]) if y_proba else None

    print(f"\nModel: {name}\nBest params: {search.best_params_}")
    print(classification_report(yb_te, y_pred, digits=4))
    print("ROC AUC:", auc)

    results.append({
        'model': name,
        'best_params': search.best_params_,
        'roc_auc': auc,
    })

pd.DataFrame(results)
```

**Multi‑class (sadece `attack` satırları ile):**

```python
# notebooks/03_multiclass_attack_family.ipynb (çekirdek hücre)
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from src.models import make_multiclass_pipelines

train_attack = train[train['y_binary']==1].copy()
test_attack  = test[test['y_binary']==1].copy()

X_tr_f, _, y_tr_f, num_cols, cat_cols = split_features(train_attack)
X_te_f, _, y_te_f, _, _               = split_features(test_attack)

grids = make_multiclass_pipelines(num_cols, cat_cols)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

mc_results = []
for name, (pipe, param_grid) in grids.items():
    search = GridSearchCV(
        estimator=pipe,
        param_grid=param_grid,
        scoring='f1_macro',
        cv=cv,
        n_jobs=-1,
        verbose=1
    )
    search.fit(X_tr_f, y_tr_f)
    y_pred = search.best_estimator_.predict(X_te_f)
    f1m = f1_score(y_te_f, y_pred, average='macro')
    print(f"\nModel: {name}\nBest params: {search.best_params_}\nMacro F1: {f1m:.4f}")
    mc_results.append({'model': name, 'best_params': search.best_params_, 'f1_macro': f1m})

pd.DataFrame(mc_results)
```

---

## 5) Değerlendirme metrikleri ve görselleştirme

```python
# src/eval.py
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import (
    roc_curve, auc, precision_recall_curve, confusion_matrix,
    ConfusionMatrixDisplay, PrecisionRecallDisplay, RocCurveDisplay
)


def plot_roc_pr(y_true, y_score, title_prefix="Binary"):
    fpr, tpr, _ = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)
    prec, rec, _ = precision_recall_curve(y_true, y_score)
    pr_auc = auc(rec, prec)

    RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc).plot()
    plt.title(f"{title_prefix} ROC (AUC={roc_auc:.3f})")
    plt.show()

    PrecisionRecallDisplay(precision=prec, recall=rec).plot()
    plt.title(f"{title_prefix} PR (AUC={pr_auc:.3f})")
    plt.show()


def plot_cm(y_true, y_pred, labels=None, normalize=None, title="Confusion Matrix"):
    cm = confusion_matrix(y_true, y_pred, labels=labels, normalize=normalize)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(cmap='Blues', xticks_rotation=45)
    plt.title(title)
    plt.show()
```

**Kullanım örneği:**

```python
# Binary model sonrası (test set):
proba = search.best_estimator_.predict_proba(X_te)[:,1]
plot_roc_pr(yb_te, proba, title_prefix="Binary Attack Detection")
plot_cm(yb_te, (proba>=0.5).astype(int), labels=[0,1], title="Binary CM", normalize='true')

# Multi-class (family):
y_pred = search.best_estimator_.predict(X_te_f)
labels = sorted(y_te_f.unique())
plot_cm(y_te_f, y_pred, labels=labels, title="Family CM", normalize='true')
```

---

## 6) EDA: Aykırı değer ve anomali görselleştirme

```python
# src/viz.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def zscore_outliers(df: pd.DataFrame, cols, threshold=3.0):
    Z = (df[cols] - df[cols].mean())/df[cols].std(ddof=0)
    mask = (np.abs(Z) > threshold).any(axis=1)
    return df[mask], Z


def boxplots(df: pd.DataFrame, cols, max_cols=6):
    cols = cols[:max_cols]
    for c in cols:
        df.boxplot(column=c)
        plt.title(f"Boxplot: {c}")
        plt.show()
```

**Öneriler:**
- `src_bytes`, `dst_bytes`, `count`, `srv_count`, `dst_host_count` gibi değişkenlerde boxplot ve z‑score ile uç değerleri inceleyin.
- Kategorik `service` değişkeninde **en sık 10 servis** için saldırı/normal oranlarını bar grafikte kıyaslayın.

---

## 7) İm balans stratejileri

- **Sınıf ağırlıkları:** `class_weight='balanced'`
- **Örnekleme:** `SMOTE`, `RandomUnderSampler`, veya `SMOTEENN`
- **Eşik ayarı:** ROC/PR eğrilerine göre optimal eşik belirleme.

```python
from sklearn.metrics import f1_score
import numpy as np

def find_best_threshold(y_true, y_scores):
    best_t, best_f1 = 0.5, -1
    for t in np.linspace(0.1, 0.9, 81):
        f1 = f1_score(y_true, (y_scores>=t).astype(int))
        if f1 > best_f1:
            best_t, best_f1 = t, f1
    return best_t, best_f1
```

---

## 8) Deney planı (minimum 2 algoritma şartını sağlayan yol haritası)

1. **Binary baseline:** Logistic Regression vs Random Forest  
   - Skor: F1, ROC AUC, PR AUC
2. **Binary iyileştirme:** Eşik ayarı + SMOTE/undersample karşılaştırması
3. **Multi‑class (family):** Logistic Regression (OvR) vs Random Forest  
   - Skor: Macro‑F1, weighted‑F1, CM  
4. **(Opsiyonel)** Spesifik saldırı adları (22+ sınıf) – RF/GB + class weight

Sonuçları tablo ve grafiklerle raporlayın (aşağıdaki şablon).

---

## 9) Rapor şablonu (report.md)

```markdown
# KDD Cup 1999 IDS – Proje Raporu

## 1. Amaç
Binary (attack vs normal) ve multi-class (attack family) tespiti.

## 2. Veri Kümesi
- KDD’99 açıklaması, train/test ayrımı, kolonlar, dağılımlar.
- Dengesizlik, tekrar eden kayıtlar, sabit kolonlar.

## 3. Yöntem
- Ön işleme (OHE, StandardScaler, ConstantDropper)
- Pipeline + StratifiedKFold CV
- Algoritmalar: LR, RF (gerekçe)

## 4. Deneyler
- Hiperparametre aralıkları ve en iyi setler
- Binary sonuçlar: Accuracy, F1, ROC AUC, PR AUC (eğriler)
- Multi-class: Macro-F1, weighted-F1, CM (ısı haritası)

## 5. Tartışma
- Hangi özellikler etkili? (özellik önemi / SHAP opsiyonel)
- Yanlış sınıflamalar ve nedenleri
- Kısıtlar (KDD’99’in tekrar içermesi, gerçek dağılıma uzaklık)

## 6. Sonuç & Gelecek Çalışma
- En iyi model(ler) ve öneriler
- NSL‑KDD ile genelleme testi (opsiyonel)
```

---

## 10) Sunum (slides-outline.md)

- **Problem Tanımı** (1 slayt)  
- **Veri & Özellikler** (2 slayt)  
- **Ön İşleme ve Pipeline** (2 slayt)  
- **Modeller & HPO** (2 slayt)  
- **Performans** – ROC/PR/CM (3–4 slayt)  
- **Aykırı Değer İncelemeleri** (1–2 slayt)  
- **Sonuçlar & Öneriler** (1–2 slayt)

---

## 11) README taslağı

```markdown
# KDD99 Intrusion Detection (Binary + Multi-Class)

## Kurulum
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Veri
`data/` klasörüne KDD’99 train/test dosyalarını (.gz) koyun.

## Çalıştırma
- EDA: `notebooks/01_eda.ipynb`
- Binary: `notebooks/02_binary_attack_detection.ipynb`
- Multi-class: `notebooks/03_multiclass_attack_family.ipynb`
```

---

## 12) Sık hatalar ve ipuçları

- **Leakage:** `fit_transform` sadece eğitim katında çalışmalı; test için `transform`. Pipeline bunu doğal olarak sağlar.
- **Aşırı tekrar/overfit:** KDD’99’da çok **duplike** satır vardır; `drop_duplicates()` deneyin.
- **Hesap yükü:** OHE ile `service` genişler; RF/GB gibi ağaç tabanlılar OHE’siz de çalışabilir ama burada karışık tipler için standart yolu koruduk.
- **Sabit kolonlar:** `num_outbound_cmds` gibi kolonları atın.
- **Sınıf dengesizliği:** Macro‑F1 ve PR eğrilerine bakın; sadece accuracy kullanmayın.

---

## 13) Genişletme önerileri (opsiyonel)

- **Özellik önemi / SHAP** ile yorumlanabilirlik
- **Threshold tuning** ile işletim noktası seçimi (örn. %95 precision eşiği)
- **Hierarchical** akış: Önce binary, sonra family modeli (bu kılavuz bu yapıyı kullanır)
- **Model kayıt** (`joblib.dump`) ve **inference script** (CLI/API)

---

Bu iskelet ile projeyi direkt başlatabilir, en az iki algoritma (LR, RF) ile **Pipeline + HPO + CV** süreçlerini tamamlayıp, metrik ve grafiklerle sonuçları raporlayabilirsiniz. İsterseniz `xgboost`/`lightgbm` ekleyerek performans karşılaştırmasını genişletebilirsiniz.

