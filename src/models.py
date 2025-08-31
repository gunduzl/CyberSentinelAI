# src/models.py
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as IMBPipeline
from .preprocess import ConstantDropper


def make_preprocessor(num_cols, cat_cols):
    """Ön işleme pipeline'ı oluşturur.
    
    Args:
        num_cols: Sayısal kolon isimleri
        cat_cols: Kategorik kolon isimleri
        
    Returns:
        ColumnTransformer: Ön işleme pipeline'ı
    """
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
    """Binary sınıflandırma için pipeline'ları oluşturur.
    
    Args:
        num_cols: Sayısal kolon isimleri
        cat_cols: Kategorik kolon isimleri
        
    Returns:
        dict: Model isimleri ve (pipeline, param_grid) çiftleri
    """
    pre = make_preprocessor(num_cols, cat_cols)

    pipe_lr = IMBPipeline(steps=[
        ('preprocessor', pre),
        ('smote', SMOTE()),
        ('classifier', LogisticRegression(max_iter=1000, n_jobs=None, class_weight='balanced'))
    ])

    pipe_rf = IMBPipeline(steps=[
        ('preprocessor', pre),
        ('smote', SMOTE()),
        ('classifier', RandomForestClassifier(class_weight='balanced'))
    ])

    pipe_gb = IMBPipeline(steps=[
        ('preprocessor', pre),
        ('classifier', GradientBoostingClassifier())  # SMOTE genelde ağaç dışı modellerle daha anlamlı
    ])

    # Hızlı test için basitleştirilmiş hiperparametre gridleri
    grids = {
        'lr': (pipe_lr, {
            'classifier__C': [0.1, 1]
        }),
        'rf': (pipe_rf, {
            'classifier__n_estimators': [100, 200],
            'classifier__max_depth': [None, 20]
        })
    }
    return grids


def make_multiclass_pipelines(num_cols, cat_cols):
    """Multi-class sınıflandırma için pipeline'ları oluşturur.
    
    Args:
        num_cols: Sayısal kolon isimleri
        cat_cols: Kategorik kolon isimleri
        
    Returns:
        dict: Model isimleri ve (pipeline, param_grid) çiftleri
    """
    pre = make_preprocessor(num_cols, cat_cols)

    pipe_lr = Pipeline(steps=[
        ('pre', pre),
        ('clf', LogisticRegression(max_iter=1000, multi_class='ovr'))
    ])

    pipe_rf = Pipeline(steps=[
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