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
    'back.':'dos','land.':'dos','neptune.':'dos','pod.':'dos','smurf.':'dos','teardrop.':'dos','apache2.':'dos','udpstorm.':'dos','processtable.':'dos','worm.':'dos',
    # Probe
    'satan.':'probe','ipsweep.':'probe','nmap.':'probe','portsweep.':'probe','mscan.':'probe','saint.':'probe',
    # R2L
    'ftp_write.':'r2l','guess_passwd.':'r2l','imap.':'r2l','multihop.':'r2l','phf.':'r2l','spy.':'r2l','warezclient.':'r2l','warezmaster.':'r2l','named.':'r2l','sendmail.':'r2l','snmpgetattack.':'r2l','snmpguess.':'r2l',
    # U2R
    'buffer_overflow.':'u2r','loadmodule.':'u2r','perl.':'u2r','rootkit.':'u2r','httptunnel.':'u2r','ps.':'u2r','sqlattack.':'u2r','xterm.':'u2r'
}


def load_kdd(path: str | Path, gz: bool = True) -> pd.DataFrame:
    """KDD Cup 1999 veri setini yükler.
    
    Args:
        path: Veri dosyasının yolu
        gz: Dosyanın gzip ile sıkıştırılmış olup olmadığı
        
    Returns:
        pandas.DataFrame: Yüklenen veri seti
    """
    path = Path(path)
    df = pd.read_csv(path, names=KDD_COLS, header=None, compression='gzip' if gz else None)
    return df


def load_kdd_data():
    """KDD Cup 1999 veri setini yükler ve train/test olarak böler.
    
    Returns:
        tuple: (X_train, X_test, y_train, y_test)
    """
    from sklearn.model_selection import train_test_split
    
    # Veri dosyalarının yolları
    data_dir = Path(__file__).parent.parent / 'data'
    train_path = data_dir / 'kddcup.data_10_percent.gz'
    test_path = data_dir / 'corrected.gz'
    
    # Eğitim verisini yükle
    if train_path.exists():
        df_train = load_kdd(train_path, gz=True)
    else:
        # Alternatif yol dene
        train_path = data_dir / 'kddcup.data_10_percent'
        if train_path.exists():
            df_train = load_kdd(train_path, gz=False)
        else:
            raise FileNotFoundError(f"Eğitim veri dosyası bulunamadı: {train_path}")
    
    # Test verisini yükle
    if test_path.exists():
        df_test = load_kdd(test_path, gz=True)
    else:
        # Alternatif yol dene
        test_path = data_dir / 'corrected'
        if test_path.exists():
            df_test = load_kdd(test_path, gz=False)
        else:
            # Test verisi yoksa train'den böl
            X = df_train.drop('label', axis=1)
            y = df_train['label']
            return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Özellikleri ve etiketleri ayır
    X_train = df_train.drop('label', axis=1)
    y_train = df_train['label']
    X_test = df_test.drop('label', axis=1)
    y_test = df_test['label']
    
    return X_train, X_test, y_train, y_test