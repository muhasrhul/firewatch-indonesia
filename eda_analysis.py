"""
FireWatch Indonesia - Exploratory Data Analysis
Analisis eksplorasi data hotspot
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Konfigurasi
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('Set2')

print("="*70)
print("FIREWATCH INDONESIA - EXPLORATORY DATA ANALYSIS")
print("="*70)
print(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Load data
print("Loading dataset...")
df = pd.read_csv('data/raw/fire_nrt_SV-C2_800747.csv')
df['acq_date'] = pd.to_datetime(df['acq_date'])
print(f"✓ Dataset: {len(df):,} baris\n")

# ============================================================
# 1. STATISTIK DESKRIPTIF
# ============================================================
print("="*70)
print("1. STATISTIK DESKRIPTIF")
print("="*70)
print(df[['brightness', 'frp', 'latitude', 'longitude']].describe())
print()

# ============================================================
# 2. ANALISIS TEMPORAL - TREN HARIAN
# ============================================================
print("="*70)
print("2. ANALISIS TEMPORAL")
print("="*70)

daily_hotspot = df.groupby('acq_date').size().reset_index(name='jumlah')
print(f"Rata-rata hotspot/hari: {daily_hotspot['jumlah'].mean():.0f}")
print(f"Hotspot tertinggi: {daily_hotspot['jumlah'].max():,} pada {daily_hotspot.loc[daily_hotspot['jumlah'].idxmax(), 'acq_date'].strftime('%Y-%m-%d')}")
print(f"Hotspot terendah: {daily_hotspot['jumlah'].min():,} pada {daily_hotspot.loc[daily_hotspot['jumlah'].idxmin(), 'acq_date'].strftime('%Y-%m-%d')}")

plt.figure(figsize=(14, 6))
plt.plot(daily_hotspot['acq_date'], daily_hotspot['jumlah'], 
         marker='o', linewidth=2, markersize=4, color='#e74c3c')
plt.xlabel('Tanggal', fontsize=12, fontweight='bold')
plt.ylabel('Jumlah Hotspot', fontsize=12, fontweight='bold')
plt.title('Tren Harian Deteksi Hotspot di Indonesia', fontsize=14, fontweight='bold', pad=20)
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('images/01_tren_harian.png', dpi=300, bbox_inches='tight')
print("✓ Grafik disimpan: images/01_tren_harian.png")
plt.close()

# Tren mingguan
df['week'] = df['acq_date'].dt.to_period('W')
weekly = df.groupby('week').size().reset_index(name='jumlah')
weekly['week_str'] = weekly['week'].astype(str)

plt.figure(figsize=(12, 6))
plt.bar(range(len(weekly)), weekly['jumlah'], color='#3498db', alpha=0.8)
plt.xlabel('Minggu', fontsize=12, fontweight='bold')
plt.ylabel('Jumlah Hotspot', fontsize=12, fontweight='bold')
plt.title('Distribusi Hotspot per Minggu', fontsize=14, fontweight='bold', pad=20)
plt.xticks(range(len(weekly)), weekly['week_str'], rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('images/02_tren_mingguan.png', dpi=300, bbox_inches='tight')
print("✓ Grafik disimpan: images/02_tren_mingguan.png")
plt.close()
print()

# ============================================================
# 3. CONFIDENCE LEVEL
# ============================================================
print("="*70)
print("3. DISTRIBUSI CONFIDENCE LEVEL")
print("="*70)

conf_dist = df['confidence'].value_counts()
conf_labels = {'n': 'Normal', 'l': 'Low', 'h': 'High'}
for conf in ['n', 'l', 'h']:
    if conf in conf_dist.index:
        count = conf_dist[conf]
        pct = (count/len(df))*100
        print(f"  {conf_labels[conf]:10s}: {count:7,} ({pct:5.2f}%)")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Bar chart
conf_plot = conf_dist.copy()
conf_plot.index = conf_plot.index.map(conf_labels)
conf_plot.plot(kind='bar', ax=ax1, color=['#3498db', '#e74c3c', '#2ecc71'], alpha=0.8)
ax1.set_xlabel('Confidence Level', fontsize=12, fontweight='bold')
ax1.set_ylabel('Jumlah Hotspot', fontsize=12, fontweight='bold')
ax1.set_title('Distribusi Confidence Level', fontsize=13, fontweight='bold')
ax1.tick_params(axis='x', rotation=0)
ax1.grid(axis='y', alpha=0.3)

# Pie chart
colors = ['#3498db', '#e74c3c', '#2ecc71']
ax2.pie(conf_plot.values, labels=conf_plot.index, autopct='%1.1f%%',
        startangle=90, colors=colors, textprops={'fontsize': 11})
ax2.set_title('Proporsi Confidence Level', fontsize=13, fontweight='bold')

plt.tight_layout()
plt.savefig('images/03_confidence_level.png', dpi=300, bbox_inches='tight')
print("✓ Grafik disimpan: images/03_confidence_level.png")
plt.close()
print()

# ============================================================
# 4. DAY VS NIGHT
# ============================================================
print("="*70)
print("4. DISTRIBUSI SIANG VS MALAM")
print("="*70)

dn_dist = df['daynight'].value_counts()
dn_labels = {'D': 'Day (Siang)', 'N': 'Night (Malam)'}
for dn in ['D', 'N']:
    if dn in dn_dist.index:
        count = dn_dist[dn]
        pct = (count/len(df))*100
        print(f"  {dn_labels[dn]:15s}: {count:7,} ({pct:5.2f}%)")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Bar chart
dn_plot = dn_dist.copy()
dn_plot.index = dn_plot.index.map(dn_labels)
dn_plot.plot(kind='bar', ax=ax1, color=['#f39c12', '#34495e'], alpha=0.8)
ax1.set_xlabel('Waktu Deteksi', fontsize=12, fontweight='bold')
ax1.set_ylabel('Jumlah Hotspot', fontsize=12, fontweight='bold')
ax1.set_title('Distribusi Deteksi Siang vs Malam', fontsize=13, fontweight='bold')
ax1.tick_params(axis='x', rotation=0)
ax1.grid(axis='y', alpha=0.3)

# Pie chart
ax2.pie(dn_plot.values, labels=dn_plot.index, autopct='%1.1f%%',
        startangle=90, colors=['#f39c12', '#34495e'], textprops={'fontsize': 11})
ax2.set_title('Proporsi Deteksi Siang vs Malam', fontsize=13, fontweight='bold')

plt.tight_layout()
plt.savefig('images/04_day_vs_night.png', dpi=300, bbox_inches='tight')
print("✓ Grafik disimpan: images/04_day_vs_night.png")
plt.close()
print()

# ============================================================
# 5. BRIGHTNESS & FRP ANALYSIS
# ============================================================
print("="*70)
print("5. ANALISIS BRIGHTNESS & FRP")
print("="*70)
print(f"Brightness - Mean: {df['brightness'].mean():.2f}, Median: {df['brightness'].median():.2f}")
print(f"FRP - Mean: {df['frp'].mean():.2f}, Median: {df['frp'].median():.2f}")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Brightness distribution
axes[0,0].hist(df['brightness'], bins=50, color='#e74c3c', alpha=0.7, edgecolor='black')
axes[0,0].set_xlabel('Brightness (K)', fontweight='bold')
axes[0,0].set_ylabel('Frequency', fontweight='bold')
axes[0,0].set_title('Distribusi Brightness', fontweight='bold')
axes[0,0].grid(alpha=0.3)

# FRP distribution
axes[0,1].hist(df['frp'], bins=50, color='#3498db', alpha=0.7, edgecolor='black')
axes[0,1].set_xlabel('FRP (MW)', fontweight='bold')
axes[0,1].set_ylabel('Frequency', fontweight='bold')
axes[0,1].set_title('Distribusi Fire Radiative Power (FRP)', fontweight='bold')
axes[0,1].grid(alpha=0.3)

# Brightness boxplot
axes[1,0].boxplot(df['brightness'], vert=True)
axes[1,0].set_ylabel('Brightness (K)', fontweight='bold')
axes[1,0].set_title('Boxplot Brightness', fontweight='bold')
axes[1,0].grid(alpha=0.3)

# FRP boxplot
axes[1,1].boxplot(df['frp'], vert=True)
axes[1,1].set_ylabel('FRP (MW)', fontweight='bold')
axes[1,1].set_title('Boxplot FRP', fontweight='bold')
axes[1,1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('images/05_brightness_frp.png', dpi=300, bbox_inches='tight')
print("✓ Grafik disimpan: images/05_brightness_frp.png")
plt.close()
print()

# ============================================================
# 6. DISTRIBUSI GEOGRAFIS
# ============================================================
print("="*70)
print("6. DISTRIBUSI GEOGRAFIS")
print("="*70)
print(f"Latitude: {df['latitude'].min():.2f}° hingga {df['latitude'].max():.2f}°")
print(f"Longitude: {df['longitude'].min():.2f}° hingga {df['longitude'].max():.2f}°")

plt.figure(figsize=(14, 8))
plt.scatter(df['longitude'], df['latitude'], alpha=0.1, s=1, c='red')
plt.xlabel('Longitude', fontsize=12, fontweight='bold')
plt.ylabel('Latitude', fontsize=12, fontweight='bold')
plt.title('Distribusi Geografis Hotspot di Indonesia', fontsize=14, fontweight='bold', pad=20)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('images/06_distribusi_geografis.png', dpi=300, bbox_inches='tight')
print("✓ Grafik disimpan: images/06_distribusi_geografis.png")
plt.close()
print()

# Heatmap density
plt.figure(figsize=(14, 8))
plt.hexbin(df['longitude'], df['latitude'], gridsize=50, cmap='YlOrRd', mincnt=1)
plt.colorbar(label='Jumlah Hotspot')
plt.xlabel('Longitude', fontsize=12, fontweight='bold')
plt.ylabel('Latitude', fontsize=12, fontweight='bold')
plt.title('Heatmap Density Hotspot di Indonesia', fontsize=14, fontweight='bold', pad=20)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('images/07_heatmap_density.png', dpi=300, bbox_inches='tight')
print("✓ Grafik disimpan: images/07_heatmap_density.png")
plt.close()
print()

# ============================================================
# 7. TOP LOKASI HOTSPOT
# ============================================================
print("="*70)
print("7. TOP LOKASI DENGAN HOTSPOT TERBANYAK")
print("="*70)

# Buat grid koordinat (0.5 derajat)
df['lat_grid'] = (df['latitude'] // 0.5) * 0.5
df['lon_grid'] = (df['longitude'] // 0.5) * 0.5
df['grid_cell'] = df['lat_grid'].astype(str) + ',' + df['lon_grid'].astype(str)

top_locations = df['grid_cell'].value_counts().head(10)
print("Top 10 Grid Cell (0.5° x 0.5°) dengan Hotspot Terbanyak:")
for i, (grid, count) in enumerate(top_locations.items(), 1):
    lat, lon = grid.split(',')
    print(f"  {i:2d}. Lat {float(lat):7.2f}°, Lon {float(lon):7.2f}° : {count:6,} hotspot")

plt.figure(figsize=(12, 6))
plt.bar(range(len(top_locations)), top_locations.values, color='#e67e22', alpha=0.8)
plt.xlabel('Grid Cell', fontsize=12, fontweight='bold')
plt.ylabel('Jumlah Hotspot', fontsize=12, fontweight='bold')
plt.title('Top 10 Lokasi dengan Hotspot Terbanyak', fontsize=14, fontweight='bold', pad=20)
plt.xticks(range(len(top_locations)), [f"#{i+1}" for i in range(len(top_locations))])
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('images/08_top_locations.png', dpi=300, bbox_inches='tight')
print("✓ Grafik disimpan: images/08_top_locations.png")
plt.close()
print()

# ============================================================
# SIMPAN SUMMARY
# ============================================================
print("="*70)
print("MENYIMPAN SUMMARY EDA")
print("="*70)

summary = f"""{"="*70}
FIREWATCH INDONESIA - EDA SUMMARY
{"="*70}

Waktu Analisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Hotspot: {len(df):,}
Periode: {df['acq_date'].min().strftime('%Y-%m-%d')} s/d {df['acq_date'].max().strftime('%Y-%m-%d')}

TREN TEMPORAL
{"="*70}
Rata-rata hotspot per hari: {daily_hotspot['jumlah'].mean():.0f}
Hari dengan hotspot tertinggi: {daily_hotspot['jumlah'].max():,} pada {daily_hotspot.loc[daily_hotspot['jumlah'].idxmax(), 'acq_date'].strftime('%Y-%m-%d')}
Hari dengan hotspot terendah: {daily_hotspot['jumlah'].min():,} pada {daily_hotspot.loc[daily_hotspot['jumlah'].idxmin(), 'acq_date'].strftime('%Y-%m-%d')}

CONFIDENCE LEVEL
{"="*70}
"""

for conf in ['n', 'l', 'h']:
    if conf in conf_dist.index:
        count = conf_dist[conf]
        pct = (count/len(df))*100
        summary += f"{conf_labels[conf]:10s}: {count:7,} ({pct:5.2f}%)\n"

summary += f"""
DAY VS NIGHT
{"="*70}
"""

for dn in ['D', 'N']:
    if dn in dn_dist.index:
        count = dn_dist[dn]
        pct = (count/len(df))*100
        summary += f"{dn_labels[dn]:15s}: {count:7,} ({pct:5.2f}%)\n"

summary += f"""
STATISTIK BRIGHTNESS & FRP
{"="*70}
Brightness - Mean: {df['brightness'].mean():.2f} K, Median: {df['brightness'].median():.2f} K
FRP - Mean: {df['frp'].mean():.2f} MW, Median: {df['frp'].median():.2f} MW

KOORDINAT
{"="*70}
Latitude: {df['latitude'].min():.2f}° hingga {df['latitude'].max():.2f}°
Longitude: {df['longitude'].min():.2f}° hingga {df['longitude'].max():.2f}°

TOP 10 LOKASI HOTSPOT (Grid 0.5° x 0.5°)
{"="*70}
"""

for i, (grid, count) in enumerate(top_locations.items(), 1):
    lat, lon = grid.split(',')
    summary += f"{i:2d}. Lat {float(lat):7.2f}°, Lon {float(lon):7.2f}° : {count:6,} hotspot\n"

summary += f"""
VISUALISASI YANG DIHASILKAN
{"="*70}
1. images/01_tren_harian.png
2. images/02_tren_mingguan.png
3. images/03_confidence_level.png
4. images/04_day_vs_night.png
5. images/05_brightness_frp.png
6. images/06_distribusi_geografis.png
7. images/07_heatmap_density.png
8. images/08_top_locations.png
"""

with open('data/processed/eda_summary.txt', 'w', encoding='utf-8') as f:
    f.write(summary)

print("✓ Summary disimpan: data/processed/eda_summary.txt")
print()

print("="*70)
print("EDA SELESAI")
print("="*70)
print(f"Total visualisasi: 8 grafik")
print(f"Lokasi: folder images/")
