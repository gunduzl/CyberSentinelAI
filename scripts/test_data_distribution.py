#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data import load_kdd
from src.preprocess import add_targets
from sklearn.model_selection import train_test_split

# Veri yükleme
print('Veri yükleniyor...')
train_raw = load_kdd('data/kddcup.data_10_percent.gz')
test_raw = load_kdd('data/corrected.gz')

# Hedef değişkenleri ekle
train_full = add_targets(train_raw)
test_full = add_targets(test_raw)

print(f'Full train boyutu: {train_full.shape}')
print(f'Full test boyutu: {test_full.shape}')

# Saldırı dağılımını kontrol et
print('\nFull train - Binary dağılım:')
print(train_full['y_binary'].value_counts())
print('\nFull train - Family dağılım:')
print(train_full['y_family'].value_counts())

print('\nFull train - Saldırı isimleri (ilk 10):')
attack_labels = train_full[train_full['y_binary'] == 1]['label'].unique()[:10]
print(attack_labels)

print('\nFull train - Attack name (ilk 10):')
attack_names = train_full[train_full['y_binary'] == 1]['attack_name'].unique()[:10]
print(attack_names)

# %50 örneklem al
train, _ = train_test_split(train_full, test_size=0.5, random_state=42, stratify=train_full['y_binary'])
test, _ = train_test_split(test_full, test_size=0.5, random_state=42, stratify=test_full['y_binary'])

print(f'\nSample train boyutu: {train.shape}')
print(f'Sample test boyutu: {test.shape}')

print('\nSample train - Binary dağılım:')
print(train['y_binary'].value_counts())
print('\nSample train - Family dağılım:')
print(train['y_family'].value_counts())

# Multiclass veri hazırla
train_mc = train.copy()
test_mc = test.copy()

# Normal trafikler için y_family = 'normal' ata
train_mc.loc[train_mc['y_binary'] == 0, 'y_family'] = 'normal'
test_mc.loc[test_mc['y_binary'] == 0, 'y_family'] = 'normal'

# NaN değerleri olan satırları kaldır
train_mc = train_mc.dropna(subset=['y_family'])
test_mc = test_mc.dropna(subset=['y_family'])

print(f'\nMulticlass train boyutu: {train_mc.shape}')
print(f'Multiclass test boyutu: {test_mc.shape}')

print('\nMulticlass train - Family dağılım:')
print(train_mc['y_family'].value_counts())
print('\nMulticlass test - Family dağılım:')
print(test_mc['y_family'].value_counts())