"""
FireWatch Indonesia - Download Weather Data Seluruh Indonesia
Download data cuaca untuk titik-titik representatif di seluruh Indonesia
"""

import pandas as pd
import requests
import time

print("="*70)
print("DOWNLOAD DATA CUACA SELURUH INDONESIA - NASA POWER API")
print("="*70)
print()

# ============================================================
# KONFIGURASI
# ============================================================
start_date = "20260801"
end_date = "20260901"
parameters = "PRECTOTCORR,T2M_MAX,RH2M"

print(f"Periode: {start_date} - {end_date}")
print(f"Parameter: {parameters}")
print()

# ============================================================
# TITIK SAMPLING SELURUH INDONESIA
# ============================================================
# Coverage: Sumatera, Jawa, Kalimantan, Sulawesi, Papua, Maluku, Nusa Tenggara
sampling_points = {
    # SUMATERA
    "Banda_Aceh_Aceh": {"lat": 5.5, "lon": 95.3},
    "Medan_Sumut": {"lat": 3.6, "lon": 98.7},
    "Pekanbaru_Riau": {"lat": 0.5, "lon": 101.4},
    "Padang_Sumbar": {"lat": -0.9, "lon": 100.4},
    "Jambi": {"lat": -1.6, "lon": 103.6},
    "Palembang_Sumsel": {"lat": -3.0, "lon": 104.7},
    "Bengkulu": {"lat": -3.8, "lon": 102.3},
    "Bandar_Lampung": {"lat": -5.4, "lon": 105.3},
    
    # JAWA
    "Jakarta": {"lat": -6.2, "lon": 106.8},
    "Bandung_Jabar": {"lat": -6.9, "lon": 107.6},
    "Semarang_Jateng": {"lat": -7.0, "lon": 110.4},
    "Yogyakarta": {"lat": -7.8, "lon": 110.4},
    "Surabaya_Jatim": {"lat": -7.3, "lon": 112.7},
    
    # KALIMANTAN
    "Pontianak_Kalbar": {"lat": 0.0, "lon": 109.3},
    "Palangkaraya_Kalteng": {"lat": -2.2, "lon": 113.9},
    "Banjarmasin_Kalsel": {"lat": -3.3, "lon": 114.6},
    "Balikpapan_Kaltim": {"lat": -1.3, "lon": 116.8},
    "Tanjung_Selor_Kaltara": {"lat": 2.8, "lon": 117.4},
    
    # SULAWESI
    "Manado_Sulut": {"lat": 1.5, "lon": 124.8},
    "Gorontalo": {"lat": 0.5, "lon": 123.1},
    "Palu_Sulteng": {"lat": -0.9, "lon": 119.8},
    "Makassar_Sulsel": {"lat": -5.1, "lon": 119.4},
    "Kendari_Sultra": {"lat": -4.0, "lon": 122.5},
    "Mamuju_Sulbar": {"lat": -2.7, "lon": 119.0},
    
    # MALUKU & PAPUA
    "Ambon_Maluku": {"lat": -3.7, "lon": 128.2},
    "Ternate_Malut": {"lat": 0.8, "lon": 127.4},
    "Jayapura_Papua": {"lat": -2.5, "lon": 140.7},
    "Manokwari_Papua_Barat": {"lat": -0.9, "lon": 134.1},
    "Sorong_Papua_Barat": {"lat": -0.9, "lon": 131.3},
    
    # NUSA TENGGARA & BALI
    "Denpasar_Bali": {"lat": -8.7, "lon": 115.2},
    "Mataram_NTB": {"lat": -8.6, "lon": 116.1},
    "Kupang_NTT": {"lat": -10.2, "lon": 123.6},
}

print(f"Total titik sampling: {len(sampling_points)} lokasi")
print("Coverage: Seluruh Indonesia (Sumatera, Jawa, Kalimantan, Sulawesi, Papua, Maluku, Nusa Tenggara)")
print()

# ============================================================
# DOWNLOAD DATA PER TITIK
# ============================================================
all_data = []
success_count = 0
failed_count = 0

print("Memulai pengunduhan...")
print(f"Total request: {len(sampling_points)} titik")
print("(Proses ini memakan waktu ~10-15 menit)")
print()

for idx, (name, coords) in enumerate(sampling_points.items(), 1):
    print(f"[{idx}/{len(sampling_points)}] {name}...", end=" ")
    
    url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point?"
        f"latitude={coords['lat']}&longitude={coords['lon']}&"
        f"parameters={parameters}&community=AG&"
        f"start={start_date}&end={end_date}&format=JSON"
    )
    
    try:
        response = requests.get(url, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            param_data = data.get('properties', {}).get('parameter', {})
            
            if param_data:
                # Extract dates
                dates = None
                for param in parameters.split(","):
                    if param in param_data:
                        if dates is None:
                            dates = list(param_data[param].keys())
                
                # Build rows
                rows = []
                for date_str in dates:
                    row = {
                        'location': name,
                        'lat': coords['lat'],
                        'lon': coords['lon'],
                        'date': pd.to_datetime(date_str, format='%Y%m%d')
                    }
                    for param in parameters.split(","):
                        if param in param_data:
                            value = param_data[param].get(date_str)
                            # Handle missing value flag (-999)
                            if value == -999 or value < -900:
                                value = None
                            row[param] = value
                    rows.append(row)
                
                df_point = pd.DataFrame(rows)
                all_data.append(df_point)
                success_count += 1
                print(f"✓ ({len(df_point)} hari)")
            else:
                failed_count += 1
                print("✗ Data kosong")
                
        else:
            failed_count += 1
            print(f"✗ HTTP {response.status_code}")
            
    except Exception as e:
        failed_count += 1
        print(f"✗ Error")
    
    # Rate limiting: small delay between requests
    time.sleep(0.5)

print()
print(f"Selesai! Sukses: {success_count}, Gagal: {failed_count}")
print()

# ============================================================
# GABUNGKAN DATA
# ============================================================
if all_data:
    df_all = pd.concat(all_data, ignore_index=True)
    
    print("="*70)
    print("HASIL DOWNLOAD")
    print("="*70)
    print(f"Total data points: {len(df_all):,}")
    print(f"Jumlah lokasi: {df_all['location'].nunique()}")
    print(f"Periode: {df_all['date'].min()} s/d {df_all['date'].max()}")
    print()
    
    # ============================================================
    # HITUNG RATA-RATA INDONESIA
    # ============================================================
    print("Menghitung rata-rata untuk seluruh Indonesia...")
    
    df_avg = df_all.groupby('date').agg({
        'PRECTOTCORR': 'mean',
        'T2M_MAX': 'mean',
        'RH2M': 'mean'
    }).reset_index()
    
    # Rename columns
    df_avg = df_avg.rename(columns={
        'PRECTOTCORR': 'precipitation_mm',
        'T2M_MAX': 'temperature_max_celsius',
        'RH2M': 'humidity_percent'
    })
    
    print(f"  ✓ Data rata-rata: {len(df_avg)} hari")
    print()
    
    # ============================================================
    # SIMPAN DATA
    # ============================================================
    # Simpan data detail per lokasi
    output_detail = "data/raw/cuaca_indonesia_detail.csv"
    df_all.to_csv(output_detail, index=False)
    print(f"✓ Data detail tersimpan di: {output_detail}")
    
    # Simpan data rata-rata
    output_avg = "data/raw/cuaca_indonesia_avg.csv"
    df_avg.to_csv(output_avg, index=False)
    print(f"✓ Data rata-rata tersimpan di: {output_avg}")
    print()
    
    # ============================================================
    # PREVIEW
    # ============================================================
    print("="*70)
    print("PREVIEW DATA RATA-RATA INDONESIA")
    print("="*70)
    print(df_avg.head(10))
    print()
    
    # ============================================================
    # STATISTIK
    # ============================================================
    print("="*70)
    print("STATISTIK CUACA INDONESIA (1 Agustus - 1 September 2026)")
    print("="*70)
    print(f"\nCurah Hujan (mm/hari):")
    print(f"  Rata-rata: {df_avg['precipitation_mm'].mean():.2f} mm")
    print(f"  Total: {df_avg['precipitation_mm'].sum():.2f} mm")
    print(f"  Hari hujan: {(df_avg['precipitation_mm'] > 1.0).sum()} hari")
    
    print(f"\nSuhu Maksimum (°C):")
    print(f"  Rata-rata: {df_avg['temperature_max_celsius'].mean():.2f} °C")
    print(f"  Min: {df_avg['temperature_max_celsius'].min():.2f} °C")
    print(f"  Max: {df_avg['temperature_max_celsius'].max():.2f} °C")
    
    print(f"\nKelembapan (%):")
    print(f"  Rata-rata: {df_avg['humidity_percent'].mean():.2f} %")
    print(f"  Min: {df_avg['humidity_percent'].min():.2f} %")
    print(f"  Max: {df_avg['humidity_percent'].max():.2f} %")
    
    print()
    print("="*70)
    print("DOWNLOAD SELESAI!")
    print("="*70)
    print()
    print("Catatan:")
    print(f"- Data ini adalah rata-rata {success_count} titik sampling di seluruh Indonesia")
    print("- Coverage: Sumatera, Jawa, Kalimantan, Sulawesi, Papua, Maluku, Nusa Tenggara")
    print("- Representatif untuk analisis cuaca nasional vs hotspot")
    print("- Periode: 1 Agustus - 1 September 2026")

else:
    print("="*70)
    print("DOWNLOAD GAGAL")
    print("="*70)
    print("Tidak ada data yang berhasil diunduh")
