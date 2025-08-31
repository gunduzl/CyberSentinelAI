# src/preprocess.py
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from .data import ATTACK_FAMILY

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
    """Binary ve multi-class hedef değişkenlerini ekler.
    
    Args:
        df: Ham KDD veri seti
        
    Returns:
        pandas.DataFrame: Hedef değişkenleri eklenmiş veri seti
    """
    out = df.copy()
    out[BINARY_TARGET] = (out['label'] != 'normal.').astype(int)
    out['attack_name'] = out['label'].where(out['label']!='normal.', other=np.nan)
    out[MULTI_TARGET]  = out['attack_name'].map(ATTACK_FAMILY)
    return out


def split_features(df: pd.DataFrame):
    """Özellikleri ve hedef değişkenleri ayırır.
    
    Args:
        df: İşlenmiş veri seti
        
    Returns:
        tuple: X, y_bin, y_family, num_cols, cat_cols
    """
    X = df.drop(columns=['label','attack_name',BINARY_TARGET,MULTI_TARGET], errors='ignore')
    y_bin = df[BINARY_TARGET] if BINARY_TARGET in df else None
    y_family = df[MULTI_TARGET] if MULTI_TARGET in df else None
    num_cols = [c for c in X.columns if c not in CATEGORICAL]
    cat_cols = [c for c in X.columns if c in CATEGORICAL]
    return X, y_bin, y_family, num_cols, cat_cols