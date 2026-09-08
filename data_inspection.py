"""
FireWatch Indonesia - Data Inspection Script
Melakukan pemeriksaan data hotspot NASA FIRMS
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("FIREWATCH INDONESIA - DATA INSPECTION")
print("="*60)
print(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ============================================================
# 1. LOAD DATASET
# ============================================================
print("1. Loading dataset...")
df = pd.read_csv('data/raw/fire_nrt_SV-C2_800747.csv')
print("   ✓ Dataset berhasil dimuat!\n")

# ============================================================
# 2. CEK JUMLAH BARIS & KOLOM
# ============================================================
jumlah_baris, jumlah_kolom = df.shape
print("="*60)
print("2. DIMENSI DATASET")
print("="*60)
print(f"   Jumlah Baris (Records): {jumlah_baris:,}")
print(f"   Jumlah Kolom (Features): {jumlah_kolom}")
print(f"\n   Preview 5 baris pertama:")
print(df.head().to_string())
print()

# ============================================================
# 3. CEK TIPE DATA
# ============================================================
print("="*60)
print("3. TIPE DATA SETIAP KOLOM")
print("="*60)
for col, dtype in df.dtypes.items():
    print(f"   {col:20s} : {dtype}")
print()

# ============================================================
# 4. CEK MISSING VALUE
# ============================================================
missing_values = df.isnull().sum()
missing_percent = (df.isnull().sum() / len(df)) * 100
missing_df = pd.DataFrame({
    'Kolom': missing_values.index,
    'Jumlah Missing': missing_values.values,
    'Persentase (%)': missing_percent.values
})
missing_df = missing_df[missing_df['Jumlah Missing'] > 0].sort_values('Jumlah Missing', ascending=False)

print("="*60)
print("4. MISSING VALUES")
print("="*60)
if len(missing_df) > 0:
    print(missing_df.to_string(index=False))
else:
    print("   ✓ Tidak ada missing values dalam dataset.")
print()

# ============================================================
# 5. CEK DUPLIKASI
# ============================================================
jumlah_duplikat = df.duplicated().sum()
persentase_duplikat = (jumlah_duplikat / len(df)) * 100

print("="*60)
print("5. DUPLIKASI DATA")
print("="*60)
print(f"   Jumlah Baris Duplikat: {jumlah_duplikat:,}")
print(f"   Persentase Duplikat: {persentase_duplikat:.2f}%")
if jumlah_duplikat > 0:
    print(f"\n   ⚠️ Ditemukan {jumlah_duplikat:,} baris duplikat")
else:
    print("   ✓ Tidak ada duplikasi data")
print()

# ============================================================
# 6. CEK RENTANG TANGGAL
# ============================================================
df['acq_date'] = pd.to_datetime(df['acq_date'])

print("="*60)
print("6. RENTANG TANGGAL")
print("="*60)
print(f"   Tanggal Awal  : {df['acq_date'].min()}")
print(f"   Tanggal Akhir : {df['acq_date'].max()}")
print(f"   Rentang Waktu : {(df['acq_date'].max() - df['acq_date'].min()).days} hari")

df['bulan'] = df['acq_date'].dt.to_period('M')
distribusi_bulan = df['bulan'].value_counts().sort_index()
print(f"\n   Distribusi Hotspot per Bulan:")
for bulan, jumlah in distribusi_bulan.items():
    print(f"   {bulan} : {jumlah:,} hotspot")
print()

# ============================================================
# 7. CEK KOORDINAT
# ============================================================
# Koordinat Indonesia: Latitude -11° hingga 6°, Longitude 95° hingga 141°
invalid_lat = ((df['latitude'] < -11) | (df['latitude'] > 6)).sum()
invalid_lon = ((df['longitude'] < 95) | (df['longitude'] > 141)).sum()

print("="*60)
print("7. STATISTIK KOORDINAT")
print("="*60)
print(f"   Latitude:")
print(f"     Min  : {df['latitude'].min():.4f}°")
print(f"     Max  : {df['latitude'].max():.4f}°")
print(f"     Mean : {df['latitude'].mean():.4f}°")
print(f"\n   Longitude:")
print(f"     Min  : {df['longitude'].min():.4f}°")
print(f"     Max  : {df['longitude'].max():.4f}°")
print(f"     Mean : {df['longitude'].mean():.4f}°")

print(f"\n   Validasi Koordinat Indonesia:")
print(f"     Latitude di luar rentang  : {invalid_lat:,} baris")
print(f"     Longitude di luar rentang : {invalid_lon:,} baris")

if invalid_lat > 0 or invalid_lon > 0:
    print(f"     ⚠️ Ada koordinat di luar wilayah Indonesia")
else:
    print(f"     ✓ Semua koordinat dalam wilayah Indonesia")
print()

# ============================================================
# 8. CEK KOLOM CONFIDENCE & SATELLITE
# ============================================================
print("="*60)
print("8. INFORMASI TAMBAHAN")
print("="*60)
print(f"   Distribusi Confidence Level:")
for conf, count in df['confidence'].value_counts().items():
    pct = (count/len(df))*100
    print(f"     {conf} : {count:,} ({pct:.1f}%)")

print(f"\n   Distribusi Satelit:")
for sat, count in df['satellite'].value_counts().items():
    pct = (count/len(df))*100
    print(f"     {sat} : {count:,} ({pct:.1f}%)")

print(f"\n   Distribusi Day/Night:")
for dn, count in df['daynight'].value_counts().items():
    pct = (count/len(df))*100
    dn_label = "Day" if dn == "D" else "Night"
    print(f"     {dn_label} : {count:,} ({pct:.1f}%)")
print()

# ============================================================
# 9. SIMPAN HASIL PEMERIKSAAN
# ============================================================
print("="*60)
print("9. MENYIMPAN HASIL PEMERIKSAAN")
print("="*60)

ringkasan = f"""{"="*60}
FIREWATCH INDONESIA - HASIL PEMERIKSAAN DATA
{"="*60}

Waktu Pemeriksaan: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
File: fire_nrt_SV-C2_800747.csv

DIMENSI DATASET
{"="*60}
Jumlah Baris (Records)    : {jumlah_baris:,}
Jumlah Kolom (Features)   : {jumlah_kolom}

DUPLIKASI
{"="*60}
Jumlah Baris Duplikat     : {jumlah_duplikat:,}
Persentase Duplikat       : {persentase_duplikat:.2f}%

MISSING VALUES
{"="*60}
"""

if len(missing_df) > 0:
    ringkasan += missing_df.to_string(index=False) + "\n"
else:
    ringkasan += "Tidak ada missing values.\n"

ringkasan += f"""
RENTANG TANGGAL
{"="*60}
Tanggal Awal              : {df['acq_date'].min()}
Tanggal Akhir             : {df['acq_date'].max()}
Rentang Waktu             : {(df['acq_date'].max() - df['acq_date'].min()).days} hari

KOORDINAT
{"="*60}
Latitude Min              : {df['latitude'].min():.4f}°
Latitude Max              : {df['latitude'].max():.4f}°
Longitude Min             : {df['longitude'].min():.4f}°
Longitude Max             : {df['longitude'].max():.4f}°
Koordinat Invalid (Lat)   : {invalid_lat:,}
Koordinat Invalid (Lon)   : {invalid_lon:,}

TIPE DATA
{"="*60}
"""

for col, dtype in df.dtypes.items():
    ringkasan += f"{col:20s} : {dtype}\n"

ringkasan += f"""
DISTRIBUSI BULAN
{"="*60}
"""
for bulan, jumlah in distribusi_bulan.items():
    ringkasan += f"{bulan} : {jumlah:,}\n"

# Simpan ke file
with open('data/processed/data_inspection_summary.txt', 'w', encoding='utf-8') as f:
    f.write(ringkasan)

print("   ✓ Hasil pemeriksaan disimpan ke:")
print("     data/processed/data_inspection_summary.txt")
print()

print("="*60)
print("PEMERIKSAAN DATA SELESAI")
print("="*60)
