"""
FireWatch Indonesia - Weather vs Hotspot Analysis
Analisis korelasi antara kondisi cuaca dengan aktivitas hotspot
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("FIREWATCH INDONESIA - WEATHER VS HOTSPOT ANALYSIS")
print("="*70)
print()

# ============================================================
# 1. LOAD DATA
# ============================================================
print("1. Loading data...")

# Load hotspot data
df_hotspot = pd.read_csv('data/raw/fire_nrt_SV-C2_800747.csv')
df_hotspot['acq_date'] = pd.to_datetime(df_hotspot['acq_date'])

# Load weather data (rata-rata Indonesia)
df_weather = pd.read_csv('data/raw/cuaca_indonesia_avg.csv')
df_weather['date'] = pd.to_datetime(df_weather['date'])

print(f"   ✓ Hotspot: {len(df_hotspot):,} records")
print(f"   ✓ Cuaca: {len(df_weather)} hari")
print()

# ============================================================
# 2. AGREGASI HOTSPOT HARIAN
# ============================================================
print("2. Menghitung jumlah hotspot per hari...")

daily_hotspot = df_hotspot.groupby('acq_date').size().reset_index(name='jumlah_hotspot')
daily_hotspot = daily_hotspot.rename(columns={'acq_date': 'date'})

print(f"   ✓ Data harian hotspot: {len(daily_hotspot)} hari")
print()

# ============================================================
# 3. MERGE DATA CUACA & HOTSPOT
# ============================================================
print("3. Menggabungkan data cuaca dan hotspot...")

# Merge berdasarkan tanggal
df_merged = pd.merge(
    daily_hotspot,
    df_weather,
    on='date',
    how='inner'
)

print(f"   ✓ Data gabungan: {len(df_merged)} hari")
print(f"   Periode: {df_merged['date'].min().strftime('%Y-%m-%d')} s/d {df_merged['date'].max().strftime('%Y-%m-%d')}")
print()

# ============================================================
# 4. ANALISIS KORELASI
# ============================================================
print("="*70)
print("4. ANALISIS KORELASI")
print("="*70)

# Drop missing values untuk korelasi
df_clean = df_merged[['jumlah_hotspot', 'temperature_max_celsius', 
                       'precipitation_mm', 'humidity_percent']].dropna()

print(f"\nData untuk korelasi: {len(df_clean)} hari (setelah remove missing values)")
print()

# Hitung korelasi Pearson
try:
    corr_temp = stats.pearsonr(df_clean['temperature_max_celsius'], df_clean['jumlah_hotspot'])
    corr_precip = stats.pearsonr(df_clean['precipitation_mm'], df_clean['jumlah_hotspot'])
    corr_humid = stats.pearsonr(df_clean['humidity_percent'], df_clean['jumlah_hotspot'])
    
    print("Korelasi Pearson dengan Jumlah Hotspot:")
    print("-" * 60)
    print(f"Suhu Maksimum      : r = {corr_temp[0]:7.4f}, p-value = {corr_temp[1]:.6f}")
    print(f"Curah Hujan        : r = {corr_precip[0]:7.4f}, p-value = {corr_precip[1]:.6f}")
    print(f"Kelembapan         : r = {corr_humid[0]:7.4f}, p-value = {corr_humid[1]:.6f}")
    print()
    
    # Interpretasi korelasi
    print("Interpretasi:")
    
    # Suhu
    if corr_temp[1] < 0.05:
        strength = "KUAT" if abs(corr_temp[0]) > 0.5 else "SEDANG"
        print(f"  ✓ Suhu: Korelasi positif {strength} & SIGNIFIKAN")
        print(f"    → Suhu tinggi = hotspot meningkat")
    else:
        print(f"  ✗ Suhu: Tidak signifikan")
    
    # Hujan
    if corr_precip[1] < 0.05:
        strength = "KUAT" if abs(corr_precip[0]) > 0.5 else "SEDANG"
        direction = "positif" if corr_precip[0] > 0 else "negatif"
        print(f"  ✓ Hujan: Korelasi {direction} {strength} & SIGNIFIKAN")
    else:
        print(f"  ✗ Hujan: Korelasi lemah & tidak signifikan")
        print(f"    → Hujan bukan faktor kuat")
    
    # Kelembapan
    if corr_humid[1] < 0.05:
        strength = "SANGAT KUAT" if abs(corr_humid[0]) > 0.7 else "KUAT" if abs(corr_humid[0]) > 0.5 else "SEDANG"
        print(f"  ✓ Kelembapan: Korelasi negatif {strength} & SANGAT SIGNIFIKAN!")
        print(f"    → Kelembapan rendah = hotspot meningkat drastis")
    else:
        print(f"  ✗ Kelembapan: Tidak signifikan")
    
    print()
    
except Exception as e:
    print(f"⚠️ Error dalam perhitungan korelasi: {e}")
    corr_temp = (0, 1)
    corr_precip = (0, 1)
    corr_humid = (0, 1)

# ============================================================
# 5. STATISTIK DESKRIPTIF
# ============================================================
print("="*70)
print("5. STATISTIK DESKRIPTIF")
print("="*70)
print("\nRata-rata Hotspot per Hari:")
print(f"  Semua hari: {df_merged['jumlah_hotspot'].mean():.0f} hotspot")

# Hari dengan/tanpa hujan
rainy_days = df_merged[df_merged['precipitation_mm'] > 1.0]
dry_days = df_merged[df_merged['precipitation_mm'] <= 1.0]

if len(rainy_days) > 0:
    print(f"  Hari hujan (>1mm): {rainy_days['jumlah_hotspot'].mean():.0f} hotspot (n={len(rainy_days)})")
if len(dry_days) > 0:
    print(f"  Hari kering (≤1mm): {dry_days['jumlah_hotspot'].mean():.0f} hotspot (n={len(dry_days)})")

# Hari panas vs normal
hot_days = df_merged[df_merged['temperature_max_celsius'] > df_merged['temperature_max_celsius'].median()]
normal_days = df_merged[df_merged['temperature_max_celsius'] <= df_merged['temperature_max_celsius'].median()]

print(f"\n  Hari panas (>median): {hot_days['jumlah_hotspot'].mean():.0f} hotspot (n={len(hot_days)})")
print(f"  Hari normal (≤median): {normal_days['jumlah_hotspot'].mean():.0f} hotspot (n={len(normal_days)})")
print()

# ============================================================
# 6. VISUALISASI - TIME SERIES
# ============================================================
print("6. Membuat visualisasi...")

fig, axes = plt.subplots(3, 1, figsize=(14, 12))

# Plot 1: Hotspot dan Suhu
ax1 = axes[0]
ax1_twin = ax1.twinx()

ax1.plot(df_merged['date'], df_merged['jumlah_hotspot'], 
         color='#e74c3c', linewidth=2, marker='o', markersize=4, label='Jumlah Hotspot')
ax1_twin.plot(df_merged['date'], df_merged['temperature_max_celsius'], 
              color='#f39c12', linewidth=2, marker='s', markersize=4, label='Suhu Max')

ax1.set_xlabel('Tanggal', fontweight='bold')
ax1.set_ylabel('Jumlah Hotspot', fontweight='bold', color='#e74c3c')
ax1_twin.set_ylabel('Suhu Maksimum (°C)', fontweight='bold', color='#f39c12')
ax1.set_title('Hubungan Suhu Maksimum dengan Jumlah Hotspot', fontsize=13, fontweight='bold', pad=15)
ax1.tick_params(axis='y', labelcolor='#e74c3c')
ax1_twin.tick_params(axis='y', labelcolor='#f39c12')
ax1.legend(loc='upper left')
ax1_twin.legend(loc='upper right')
ax1.grid(True, alpha=0.3)
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

# Plot 2: Hotspot dan Curah Hujan
ax2 = axes[1]
ax2_twin = ax2.twinx()

ax2.plot(df_merged['date'], df_merged['jumlah_hotspot'], 
         color='#e74c3c', linewidth=2, marker='o', markersize=4, label='Jumlah Hotspot')
ax2_twin.bar(df_merged['date'], df_merged['precipitation_mm'], 
             color='#3498db', alpha=0.6, label='Curah Hujan')

ax2.set_xlabel('Tanggal', fontweight='bold')
ax2.set_ylabel('Jumlah Hotspot', fontweight='bold', color='#e74c3c')
ax2_twin.set_ylabel('Curah Hujan (mm/hari)', fontweight='bold', color='#3498db')
ax2.set_title('Hubungan Curah Hujan dengan Jumlah Hotspot', fontsize=13, fontweight='bold', pad=15)
ax2.tick_params(axis='y', labelcolor='#e74c3c')
ax2_twin.tick_params(axis='y', labelcolor='#3498db')
ax2.legend(loc='upper left')
ax2_twin.legend(loc='upper right')
ax2.grid(True, alpha=0.3)
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)

# Plot 3: Hotspot dan Kelembapan
ax3 = axes[2]
ax3_twin = ax3.twinx()

ax3.plot(df_merged['date'], df_merged['jumlah_hotspot'], 
         color='#e74c3c', linewidth=2, marker='o', markersize=4, label='Jumlah Hotspot')
ax3_twin.plot(df_merged['date'], df_merged['humidity_percent'], 
              color='#2ecc71', linewidth=2, marker='^', markersize=4, label='Kelembapan')

ax3.set_xlabel('Tanggal', fontweight='bold')
ax3.set_ylabel('Jumlah Hotspot', fontweight='bold', color='#e74c3c')
ax3_twin.set_ylabel('Kelembapan (%)', fontweight='bold', color='#2ecc71')
ax3.set_title('Hubungan Kelembapan dengan Jumlah Hotspot', fontsize=13, fontweight='bold', pad=15)
ax3.tick_params(axis='y', labelcolor='#e74c3c')
ax3_twin.tick_params(axis='y', labelcolor='#2ecc71')
ax3.legend(loc='upper left')
ax3_twin.legend(loc='upper right')
ax3.grid(True, alpha=0.3)
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)

plt.tight_layout()
plt.savefig('images/12_weather_vs_hotspot_timeseries.png', dpi=300, bbox_inches='tight')
print("   ✓ Grafik time series disimpan: images/12_weather_vs_hotspot_timeseries.png")
plt.close()

# ============================================================
# 7. VISUALISASI - SCATTER PLOTS (Simple)
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Scatter 1: Suhu vs Hotspot
axes[0].scatter(df_merged['temperature_max_celsius'], df_merged['jumlah_hotspot'], 
                alpha=0.6, s=100, color='#e74c3c', edgecolors='black', linewidth=0.5)
axes[0].set_xlabel('Suhu Maksimum (°C)', fontweight='bold')
axes[0].set_ylabel('Jumlah Hotspot', fontweight='bold')
axes[0].set_title(f'Suhu vs Hotspot\nr = {corr_temp[0]:.3f}', fontweight='bold')
axes[0].grid(True, alpha=0.3)

# Scatter 2: Curah Hujan vs Hotspot
axes[1].scatter(df_merged['precipitation_mm'], df_merged['jumlah_hotspot'], 
                alpha=0.6, s=100, color='#3498db', edgecolors='black', linewidth=0.5)
axes[1].set_xlabel('Curah Hujan (mm/hari)', fontweight='bold')
axes[1].set_ylabel('Jumlah Hotspot', fontweight='bold')
axes[1].set_title(f'Curah Hujan vs Hotspot\nr = {corr_precip[0]:.3f}', fontweight='bold')
axes[1].grid(True, alpha=0.3)

# Scatter 3: Kelembapan vs Hotspot
axes[2].scatter(df_merged['humidity_percent'], df_merged['jumlah_hotspot'], 
                alpha=0.6, s=100, color='#2ecc71', edgecolors='black', linewidth=0.5)
axes[2].set_xlabel('Kelembapan (%)', fontweight='bold')
axes[2].set_ylabel('Jumlah Hotspot', fontweight='bold')
axes[2].set_title(f'Kelembapan vs Hotspot\nr = {corr_humid[0]:.3f}', fontweight='bold')
axes[2].grid(True, alpha=0.3)

plt.suptitle('Korelasi Kondisi Cuaca dengan Jumlah Hotspot', 
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('images/13_weather_vs_hotspot_scatter.png', dpi=300, bbox_inches='tight')
print("   ✓ Grafik scatter plots disimpan: images/13_weather_vs_hotspot_scatter.png")
plt.close()

# ============================================================
# 8. HEATMAP KORELASI
# ============================================================
# Buat correlation matrix
corr_data = df_merged[['jumlah_hotspot', 'temperature_max_celsius', 
                        'precipitation_mm', 'humidity_percent']].copy()
corr_data.columns = ['Jumlah Hotspot', 'Suhu Max (°C)', 'Curah Hujan (mm)', 'Kelembapan (%)']
corr_matrix = corr_data.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='RdYlGn_r', 
            center=0, square=True, linewidths=2, cbar_kws={"shrink": 0.8},
            vmin=-1, vmax=1)
plt.title('Correlation Matrix: Cuaca vs Hotspot', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('images/14_correlation_heatmap.png', dpi=300, bbox_inches='tight')
print("   ✓ Heatmap korelasi disimpan: images/14_correlation_heatmap.png")
plt.close()

print()

# ============================================================
# 9. SIMPAN HASIL ANALISIS
# ============================================================
print("7. Menyimpan hasil analisis...")

# Simpan data gabungan
df_merged.to_csv('data/processed/weather_hotspot_merged.csv', index=False)
print("   ✓ Data gabungan: data/processed/weather_hotspot_merged.csv")

# Simpan summary
summary = f"""{"="*70}
FIREWATCH INDONESIA - WEATHER VS HOTSPOT ANALYSIS
{"="*70}

Periode Analisis: {df_merged['date'].min().strftime('%Y-%m-%d')} s/d {df_merged['date'].max().strftime('%Y-%m-%d')}
Total Hari: {len(df_merged)}

KORELASI PEARSON
{"="*70}
Suhu Maksimum vs Hotspot      : r = {corr_temp[0]:7.4f}, p = {corr_temp[1]:.6f}
Curah Hujan vs Hotspot        : r = {corr_precip[0]:7.4f}, p = {corr_precip[1]:.6f}
Kelembapan vs Hotspot         : r = {corr_humid[0]:7.4f}, p = {corr_humid[1]:.6f}

INTERPRETASI
{"="*70}
"""

if corr_temp[1] < 0.05:
    summary += f"✓ Suhu memiliki korelasi SIGNIFIKAN (p < 0.05)\n"
else:
    summary += f"✗ Suhu TIDAK memiliki korelasi signifikan (p ≥ 0.05)\n"

if corr_precip[1] < 0.05:
    summary += f"✓ Curah hujan memiliki korelasi SIGNIFIKAN (p < 0.05)\n"
else:
    summary += f"✗ Curah hujan TIDAK memiliki korelasi signifikan (p ≥ 0.05)\n"

if corr_humid[1] < 0.05:
    summary += f"✓ Kelembapan memiliki korelasi SIGNIFIKAN (p < 0.05)\n"
else:
    summary += f"✗ Kelembapan TIDAK memiliki korelasi signifikan (p ≥ 0.05)\n"

summary += f"""
STATISTIK HOTSPOT
{"="*70}
Rata-rata hotspot semua hari     : {df_merged['jumlah_hotspot'].mean():.0f}
"""
if len(rainy_days) > 0:
    summary += f"Rata-rata hari hujan (>1mm)      : {rainy_days['jumlah_hotspot'].mean():.0f} (n={len(rainy_days)})\n"
if len(dry_days) > 0:
    summary += f"Rata-rata hari kering (≤1mm)     : {dry_days['jumlah_hotspot'].mean():.0f} (n={len(dry_days)})\n"

summary += f"""Rata-rata hari panas (>median)   : {hot_days['jumlah_hotspot'].mean():.0f} (n={len(hot_days)})
Rata-rata hari normal (≤median)  : {normal_days['jumlah_hotspot'].mean():.0f} (n={len(normal_days)})

VISUALISASI
{"="*70}
1. images/12_weather_vs_hotspot_timeseries.png - Time series overlay
2. images/13_weather_vs_hotspot_scatter.png - Scatter plots
3. images/14_correlation_heatmap.png - Correlation heatmap
"""

with open('data/processed/weather_hotspot_summary.txt', 'w', encoding='utf-8') as f:
    f.write(summary)

print("   ✓ Summary: data/processed/weather_hotspot_summary.txt")
print()

print("="*70)
print("ANALISIS SELESAI!")
print("="*70)
