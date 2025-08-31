# src/eval.py
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import (
    roc_curve, auc, precision_recall_curve, confusion_matrix,
    ConfusionMatrixDisplay, PrecisionRecallDisplay, RocCurveDisplay,
    f1_score
)


def plot_roc_pr(y_true, y_score, title_prefix="Binary"):
    """ROC ve Precision-Recall eğrilerini çizer.
    
    Args:
        y_true: Gerçek etiketler
        y_score: Tahmin skorları
        title_prefix: Grafik başlığı öneki
    """
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
    """Confusion matrix çizer.
    
    Args:
        y_true: Gerçek etiketler
        y_pred: Tahmin edilen etiketler
        labels: Sınıf etiketleri
        normalize: Normalizasyon türü
        title: Grafik başlığı
    """
    cm = confusion_matrix(y_true, y_pred, labels=labels, normalize=normalize)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(cmap='Blues', xticks_rotation=45)
    plt.title(title)
    plt.show()


def find_best_threshold(y_true, y_scores):
    """En iyi F1 skoru veren eşiği bulur.
    
    Args:
        y_true: Gerçek etiketler
        y_scores: Tahmin skorları
        
    Returns:
        tuple: (en_iyi_eşik, en_iyi_f1_skoru)
    """
    best_t, best_f1 = 0.5, -1
    for t in np.linspace(0.1, 0.9, 81):
        f1 = f1_score(y_true, (y_scores>=t).astype(int))
        if f1 > best_f1:
            best_t, best_f1 = t, f1
    return best_t, best_f1