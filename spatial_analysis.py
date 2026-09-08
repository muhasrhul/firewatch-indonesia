"""
FireWatch Indonesia - Spatial Analysis
Analisis hotspot per provinsi dengan data batas wilayah administratif
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("FIREWATCH INDONESIA - SPATIAL ANALYSIS")
print("="*70)
print()

# ============================================================
# 1. LOAD DATA
# ============================================================
print("1. Loading data...")
df = pd.read_csv('data/raw/fire_nrt_SV-C2_800747.csv')
df['acq_date'] = pd.to_datetime(df['acq_date'])
print(f"   ✓ Hotspot: {len(df):,} baris")

provinsi_gdf = gpd.read_file('data/raw/indonesia-province-simple.json')
print(f"   ✓ Provinsi: {len(provinsi_gdf)} provinsi")
print()

# ============================================================
# 2. KONVERSI HOTSPOT KE GEODATAFRAME
# ============================================================
print("2. Konversi koordinat ke format spatial...")
geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
hotspot_gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')

if provinsi_gdf.crs != hotspot_gdf.crs:
    provinsi_gdf = provinsi_gdf.to_crs(hotspot_gdf.crs)
print(f"   ✓ GeoDataFrame siap")
print()

# ============================================================
# 3. SPATIAL JOIN
# ============================================================
print("3. Melakukan spatial join...")
print("   (Proses ini memakan waktu beberapa menit...)")
hotspot_with_province = gpd.sjoin(hotspot_gdf, provinsi_gdf, how='left', predicate='within')
print(f"   ✓ Spatial join selesai!")
print()

# ============================================================
# 4. DETEKSI KOLOM NAMA PROVINSI
# ============================================================
nama_kolom = None
for col in ['Propinsi', 'province', 'name', 'NAME_1', 'PROVINSI', 'Nama']:
    if col in hotspot_with_province.columns:
        nama_kolom = col
        break

if nama_kolom is None:
    print("⚠️ Kolom provinsi tidak ditemukan. Kolom yang tersedia:")
    print(hotspot_with_province.columns.tolist())
    exit(1)

print(f"4. Kolom provinsi: '{nama_kolom}'")
print()

# ============================================================
# 5. ANALISIS PER PROVINSI
# ============================================================
print("="*70)
print("5. HOTSPOT PER PROVINSI")
print("="*70)

hotspot_per_provinsi = hotspot_with_province.groupby(nama_kolom).size().reset_index(name='jumlah_hotspot')
hotspot_per_provinsi = hotspot_per_provinsi.sort_values('jumlah_hotspot', ascending=False)

print("TOP 10 PROVINSI DENGAN HOTSPOT TERBANYAK:")
for i, row in hotspot_per_provinsi.head(10).iterrows():
    prov_name = row[nama_kolom]
    if pd.notna(prov_name):
        print(f"  {i+1:2d}. {prov_name:35s} : {row['jumlah_hotspot']:7,} hotspot")

print()

# Hitung persentase
total_hotspot = hotspot_per_provinsi['jumlah_hotspot'].sum()
hotspot_per_provinsi['persentase'] = (hotspot_per_provinsi['jumlah_hotspot'] / total_hotspot * 100)

print(f"Total hotspot teridentifikasi: {total_hotspot:,}")
print()

# ============================================================
# 6. VISUALISASI BAR CHART
# ============================================================
print("6. Membuat visualisasi...")

plt.figure(figsize=(12, 8))
top10 = hotspot_per_provinsi.head(10)
plt.barh(range(len(top10)), top10['jumlah_hotspot'], color='#e74c3c', alpha=0.8)
plt.yticks(range(len(top10)), top10[nama_kolom])
plt.xlabel('Jumlah Hotspot', fontsize=12, fontweight='bold')
plt.ylabel('Provinsi', fontsize=12, fontweight='bold')
plt.title('Top 10 Provinsi dengan Hotspot Terbanyak\n(1 Agustus - 7 September 2026)', 
          fontsize=14, fontweight='bold', pad=20)
plt.gca().invert_yaxis()
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('images/09_top_provinsi.png', dpi=300, bbox_inches='tight')
print("   ✓ Grafik disimpan: images/09_top_provinsi.png")
plt.close()

# ============================================================
# 7. PETA CHOROPLETH
# ============================================================
print("7. Membuat peta choropleth...")

# Gabungkan data
provinsi_with_hotspot = provinsi_gdf.merge(
    hotspot_per_provinsi, 
    left_on=nama_kolom, 
    right_on=nama_kolom, 
    how='left'
)
provinsi_with_hotspot['jumlah_hotspot'] = provinsi_with_hotspot['jumlah_hotspot'].fillna(0)

# Plot choropleth
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
provinsi_with_hotspot.plot(
    column='jumlah_hotspot',
    cmap='YlOrRd',
    linewidth=0.8,
    ax=ax,
    edgecolor='0.8',
    legend=True,
    legend_kwds={'label': 'Jumlah Hotspot', 'shrink': 0.5}
)
ax.set_title('Peta Sebaran Hotspot per Provinsi di Indonesia\n(1 Agustus - 7 September 2026)', 
             fontsize=16, fontweight='bold', pad=20)
ax.axis('off')
plt.tight_layout()
plt.savefig('images/10_peta_choropleth.png', dpi=300, bbox_inches='tight')
print("   ✓ Peta disimpan: images/10_peta_choropleth.png")
plt.close()

# ============================================================
# 8. PETA DENGAN OVERLAY HOTSPOT
# ============================================================
print("8. Membuat peta dengan overlay hotspot...")

fig, ax = plt.subplots(1, 1, figsize=(16, 12))
provinsi_gdf.plot(ax=ax, color='lightgray', edgecolor='black', linewidth=0.5)
hotspot_gdf.plot(ax=ax, color='red', markersize=0.5, alpha=0.3)
ax.set_title('Peta Hotspot dengan Batas Provinsi Indonesia\n(1 Agustus - 7 September 2026)', 
             fontsize=16, fontweight='bold', pad=20)
ax.axis('off')
plt.tight_layout()
plt.savefig('images/11_peta_overlay.png', dpi=300, bbox_inches='tight')
print("   ✓ Peta disimpan: images/11_peta_overlay.png")
plt.close()

# ============================================================
# 9. SIMPAN HASIL
# ============================================================
print()
print("9. Menyimpan hasil analisis...")

# Simpan ke CSV
hotspot_per_provinsi.to_csv('data/processed/hotspot_per_provinsi.csv', index=False)
print("   ✓ CSV disimpan: data/processed/hotspot_per_provinsi.csv")

# Simpan summary
summary = f"""{"="*70}
FIREWATCH INDONESIA - SPATIAL ANALYSIS SUMMARY
{"="*70}

Total Hotspot: {total_hotspot:,}
Jumlah Provinsi dengan Hotspot: {len(hotspot_per_provinsi)}

TOP 10 PROVINSI DENGAN HOTSPOT TERBANYAK
{"="*70}
"""

for i, row in hotspot_per_provinsi.head(10).iterrows():
    prov_name = row[nama_kolom]
    if pd.notna(prov_name):
        summary += f"{i+1:2d}. {prov_name:35s} : {row['jumlah_hotspot']:7,} ({row['persentase']:5.2f}%)\n"

summary += f"""
STATISTIK
{"="*70}
Mean hotspot per provinsi: {hotspot_per_provinsi['jumlah_hotspot'].mean():.0f}
Median hotspot per provinsi: {hotspot_per_provinsi['jumlah_hotspot'].median():.0f}
Std Dev: {hotspot_per_provinsi['jumlah_hotspot'].std():.0f}

VISUALISASI YANG DIHASILKAN
{"="*70}
1. images/09_top_provinsi.png - Bar chart top 10 provinsi
2. images/10_peta_choropleth.png - Peta choropleth
3. images/11_peta_overlay.png - Peta dengan overlay hotspot
"""

with open('data/processed/spatial_analysis_summary.txt', 'w', encoding='utf-8') as f:
    f.write(summary)

print("   ✓ Summary disimpan: data/processed/spatial_analysis_summary.txt")
print()

print("="*70)
print("SPATIAL ANALYSIS SELESAI")
print("="*70)
print(f"Total visualisasi: 3 peta")
print(f"Lokasi: folder images/")
