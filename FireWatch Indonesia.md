
# FireWatch Indonesia

### Analisis Spasial dan Temporal Titik Panas Kebakaran Hutan dan Lahan Berbasis Data Satelit

> **Status:** In Progress  
> **Project Type:** Data Analyst Portfolio Project  
> **Focus:** Exploratory Data Analysis, Spatial Analysis, and Interactive Dashboard

## 1. Project Overview

**FireWatch Indonesia** adalah proyek analisis data yang bertujuan untuk memahami pola persebaran dan perubahan titik panas kebakaran hutan dan lahan di Indonesia berdasarkan lokasi, waktu, dan kondisi lingkungan.

Proyek ini menggunakan data pengamatan satelit untuk mengidentifikasi pola hotspot, membandingkan aktivitas kebakaran antarwilayah, serta menyajikan hasil analisis dalam bentuk visualisasi dan dashboard interaktif.

> **Catatan:** Titik panas merupakan deteksi anomali panas dari satelit, bukan pengukuran langsung luas kebakaran. Oleh karena itu, hasil analisis akan ditafsirkan sebagai pola deteksi hotspot, bukan sebagai kepastian bahwa setiap titik merupakan kebakaran hutan atau lahan.

## 2. Objectives

- Mengidentifikasi persebaran titik panas kebakaran di Indonesia.
- Menganalisis tren hotspot berdasarkan waktu.
- Membandingkan jumlah deteksi hotspot antarwilayah.
- Mengeksplorasi hubungan antara kondisi cuaca dan aktivitas hotspot.
- Mengembangkan dashboard interaktif untuk menyajikan hasil analisis.
- Menghasilkan insight berbasis data yang dapat digunakan untuk memahami pola kebakaran.

## 3. Research Questions

1. Wilayah mana yang memiliki jumlah deteksi hotspot tertinggi?
2. Bagaimana perubahan jumlah hotspot dari waktu ke waktu?
3. Pada bulan atau periode apa aktivitas hotspot paling tinggi?
4. Apakah terdapat hubungan antara kondisi cuaca dan jumlah deteksi hotspot?
5. Bagaimana persebaran hotspot berdasarkan lokasi geografis?
6. Apa keterbatasan data yang perlu dipertimbangkan dalam interpretasi hasil?

## 4. Data Sources

### Primary Data

**NASA FIRMS — Fire Information for Resource Management System**

Data utama yang digunakan adalah data *active fire* atau titik panas hasil pengamatan satelit.

- **Source:** [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/)
- **Planned dataset:** VIIRS 375 m
- **Planned coverage:** Indonesia
- **Planned period:** 1 Januari–31 Desember 2025
- **Format:** CSV

### Supporting Data

| Dataset | Purpose |
|---|---|
| **Weather Data** | Mengeksplorasi hubungan kondisi cuaca dengan aktivitas hotspot. |
| **Administrative Boundaries** | Mengelompokkan hotspot berdasarkan provinsi atau kabupaten. |

> Dataset pendukung akan ditentukan setelah struktur data utama diperiksa.

## 5. Project Scope

### Included

- Data collection
- Data cleaning
- Exploratory Data Analysis (EDA)
- Spatial analysis
- Temporal analysis
- Data visualization
- Interactive dashboard
- Insight and reporting

### Not Included in Initial Version

- Sistem peringatan dini kebakaran secara real-time.
- Prediksi kebakaran operasional.
- Pengukuran langsung luas area terbakar.
- Sistem monitoring yang menggantikan informasi resmi kebencanaan.

Pengembangan machine learning untuk prediksi risiko dapat dipertimbangkan sebagai **fase lanjutan**, setelah data dan hasil analisis awal memadai.

## 6. Project Workflow

```text
Data Collection
      ↓
Data Cleaning
      ↓
Exploratory Data Analysis
      ↓
Spatial & Temporal Analysis
      ↓
Data Visualization
      ↓
Interactive Dashboard
      ↓
Insights & Reporting
```

## 7. Tools & Technologies

| Tool | Purpose |
|---|---|
| **Python** | Data cleaning, EDA, dan analisis. |
| **Pandas** | Manipulasi dan pengolahan data tabular. |
| **GeoPandas** | Analisis data geografis. |
| **SQL** | Penyimpanan, penggabungan, dan agregasi data. |
| **QGIS** | Visualisasi dan analisis spasial. |
| **Power BI / Tableau** | Pembuatan dashboard interaktif. |
| **GitHub** | Dokumentasi dan version control. |

## 8. Planned Analysis

### 8.1 Data Cleaning

- Memeriksa struktur dataset.
- Memeriksa missing values.
- Memeriksa duplikasi data.
- Memastikan format tanggal dan waktu.
- Memeriksa validitas koordinat.
- Menentukan penanganan data yang tidak lengkap.

### 8.2 Exploratory Data Analysis

- Distribusi jumlah hotspot.
- Tren hotspot harian dan bulanan.
- Perbandingan jumlah hotspot antarwilayah.
- Distribusi tingkat confidence.
- Perbandingan berdasarkan jenis satelit.

### 8.3 Spatial Analysis

- Pemetaan persebaran hotspot.
- Agregasi hotspot berdasarkan wilayah administrasi.
- Identifikasi wilayah dengan konsentrasi hotspot tinggi.
- Visualisasi pola geografis.

### 8.4 Weather Analysis

- Menggabungkan data hotspot dengan data cuaca.
- Mengeksplorasi hubungan suhu, curah hujan, atau kelembapan dengan jumlah hotspot.
- Menilai apakah hubungan yang ditemukan konsisten pada periode analisis.

> Hubungan statistik tidak otomatis menunjukkan hubungan sebab-akibat.

## 9. Dashboard Plan

Dashboard akan dirancang untuk menampilkan:

### Key Performance Indicators

- Total deteksi hotspot.
- Jumlah hotspot berdasarkan wilayah.
- Periode dengan aktivitas hotspot tertinggi.
- Periode analisis.

### Visualizations

- **Interactive Map:** Persebaran hotspot di Indonesia.
- **Line Chart:** Tren jumlah hotspot dari waktu ke waktu.
- **Bar Chart:** Ranking wilayah berdasarkan jumlah hotspot.
- **Monthly Comparison:** Perbandingan aktivitas hotspot antarbulan.
- **Weather Analysis:** Hubungan kondisi cuaca dengan jumlah hotspot.

### Filters

- Periode waktu.
- Provinsi atau wilayah.
- Confidence.
- Jenis satelit.

## 10. Expected Deliverables

| Deliverable | Description |
|---|---|
| **Dataset** | Data hotspot yang telah dikumpulkan dan dipersiapkan. |
| **Jupyter Notebook** | Proses cleaning, EDA, dan analisis. |
| **SQL Queries** | Query untuk pengolahan dan agregasi data. |
| **Interactive Dashboard** | Visualisasi hasil analisis. |
| **README.md** | Dokumentasi proyek. |
| **Final Insights** | Ringkasan temuan dan keterbatasan analisis. |

## 11. Project Structure

```text
firewatch-indonesia/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda.ipynb
│   └── 04_spatial_analysis.ipynb
│
├── sql/
│   └── analysis_queries.sql
│
├── dashboard/
│
├── images/
│
├── README.md
│
└── requirements.txt
```

## 12. Limitations

- Data hotspot merupakan hasil deteksi satelit, bukan pengukuran langsung luas kebakaran.
- Tidak semua kebakaran dapat terdeteksi oleh satelit.
- Data dapat memiliki keterbatasan resolusi, waktu pengamatan, dan kualitas deteksi.
- Hubungan antara cuaca dan hotspot tidak selalu menunjukkan hubungan sebab-akibat.
- Hasil analisis bergantung pada periode dan wilayah yang digunakan.

## 13. Future Improvements

- Menambahkan data historis dengan periode yang lebih panjang.
- Mengembangkan analisis perubahan hotspot antarperiode.
- Menambahkan data tutupan lahan.
- Mengembangkan analisis risiko berbasis machine learning.
- Membuat pipeline pengambilan data otomatis.
- Mengembangkan dashboard yang diperbarui secara berkala.

## 14. Project Status

**Current Stage:** Data Collection

### Progress

- [x] Menentukan topik proyek.
- [x] Menentukan nama proyek.
- [x] Menentukan scope awal.
- [x] Menentukan pertanyaan analisis.
- [x] Menentukan sumber data utama.
- [ ] Mengunduh dataset hotspot.
- [ ] Memeriksa struktur dataset.
- [ ] Melakukan data cleaning.
- [ ] Melakukan EDA.
- [ ] Melakukan spatial analysis.
- [ ] Membuat dashboard.
- [ ] Menyusun final insights.

## 15. Author

**Asrul**  
Data Analyst & Data Scientist

---

*This project is developed for educational and portfolio purposes. Findings will be interpreted based on the available data and its limitations.*
