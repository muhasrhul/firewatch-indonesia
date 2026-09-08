# 🔥 FireWatch Indonesia

Analisis temporal dan spasial titik panas kebakaran hutan dan lahan di Indonesia menggunakan data satelit NASA FIRMS (Agustus-September 2026).

## 📊 Highlights

- **192,897 hotspot detections** dalam 37 hari (1 Agustus - 7 September 2026)
- **Kelembapan udara** sebagai prediktor terkuat (r = -0.786, p < 0.001)
- **Kalimantan** menyumbang 58.5% dari total hotspot
- **14 visualisasi profesional** dan analisis komprehensif

## 🎯 Key Findings

### 1. Korelasi Cuaca vs Hotspot
- **Kelembapan**: r = -0.786 (p < 0.001) - Highly significant
- **Suhu**: r = 0.597 (p = 0.0006) - Significant
- **Curah Hujan**: r = -0.277 (p = 0.146) - Not significant (musim kemarau, variance rendah)

### 2. Distribusi Geografis
- Kalimantan: 58.5% (lahan gambut & deforestasi)
- Papua: 9.52% (illegal logging area)
- Sumatera Selatan: 6.25% (peat fire hotspot)

### 3. Temporal Pattern
- Peak: **11,100 hotspot** pada 29 Agustus 2026
- Rata-rata: 5,213 hotspot/hari
- Hari panas menghasilkan 84% lebih banyak hotspot

## 📁 Project Structure

```
firewatch-indonesia/
├── data/
│   ├── raw/                          # Raw data from NASA FIRMS & POWER
│   │   ├── fire_nrt_SV-C2_800747.csv
│   │   ├── cuaca_indonesia_avg.csv
│   │   └── indonesia-province-simple.json
│   └── processed/                    # Processed summaries
│       ├── hotspot_per_provinsi.csv
│       ├── weather_hotspot_merged.csv
│       └── *.txt (analysis summaries)
│
├── images/                           # 14 visualizations
│   ├── 01_tren_harian.png
│   ├── 02_tren_mingguan.png
│   ├── ...
│   └── 14_correlation_heatmap.png
│
├── notebooks/                        # Jupyter analysis notebooks
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda.ipynb
│   └── 04_spatial_analysis.ipynb
│
├── presentation/                     # Main deliverables
│   ├── FireWatch_Indonesia_Report.ipynb  # Full report
│   ├── FireWatch_Indonesia_Report.pdf    # PDF export (1.53 MB, 30 pages)
│   └── README.md
│
├── *.py                              # Analysis scripts
│   ├── data_inspection.py
│   ├── eda_analysis.py
│   ├── spatial_analysis.py
│   ├── weather_hotspot_analysis.py
│   └── export_notebook_to_pdf.py    # Reusable PDF export tool
│
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Analysis

```bash
# Data inspection
python data_inspection.py

# EDA
python eda_analysis.py

# Spatial analysis
python spatial_analysis.py

# Weather correlation
python weather_hotspot_analysis.py

# Generate all visualizations
python generate_all_visualizations.py
```

### 3. View Report

```bash
jupyter notebook presentation/FireWatch_Indonesia_Report.ipynb
```

### 4. Export to PDF

```bash
python export_notebook_to_pdf.py presentation/FireWatch_Indonesia_Report.ipynb
```

## 📦 Requirements

- Python 3.8+
- pandas, numpy, matplotlib, seaborn
- geopandas, folium (for spatial analysis)
- jupyter, nbconvert (for reports)
- Pandoc & MiKTeX (for PDF export)

See `requirements.txt` for complete list.

## � Visualizations

All 14 visualizations generated:

1. **Temporal Analysis**
   - Daily trend
   - Weekly trend
   - Confidence level distribution
   - Day vs night detection

2. **Characteristics**
   - Brightness & FRP distribution
   - Geographic distribution
   - Density heatmap
   - Top hotspot locations

3. **Spatial Analysis**
   - Top 10 provinces
   - Choropleth map
   - Overlay map with hotspot points

4. **Weather Correlation**
   - Time series overlay
   - Scatter plots
   - Correlation heatmap

## 🔬 Methodology

### Data Sources
1. **NASA FIRMS** - VIIRS active fire data (375m resolution)
2. **NASA POWER** - Weather data (temperature, precipitation, humidity)
3. **GeoJSON** - Indonesia province boundaries

### Analysis Pipeline
1. Data inspection & cleaning
2. Exploratory data analysis (EDA)
3. Spatial join with administrative boundaries
4. Weather correlation analysis
5. Statistical testing (Pearson correlation, p-values)

### Statistical Tests
- Pearson correlation for continuous variables
- Significance threshold: α = 0.05
- Sample size: 192,897 hotspots, 31 days weather data

## 📝 Key Insights

### Why Humidity is the Strongest Predictor

Kelembapan udara memiliki korelasi terkuat karena:
- Langsung mempengaruhi fuel moisture content
- Gambut Kalimantan sangat sensitif terhadap kelembapan
- Tetap bervariasi (75-80%) meskipun musim kemarau

### Why Precipitation is Not Significant

Dalam periode Agustus-September (musim kemarau):
- Curah hujan sangat rendah (0.7-4.6 mm/hari)
- Tidak ada variasi cukup untuk deteksi korelasi
- Semua hari basically "kering"

**Kesimpulan**: Untuk fire prediction di musim kemarau, gunakan humidity sebagai indikator, bukan rainfall.

## ⚠️ Limitations

1. **Temporal scope**: 37 hari (tidak representatif untuk seluruh tahun)
2. **Seasonal bias**: Data hanya musim kemarau (peak fire season)
3. **Weather resolution**: 32 lokasi untuk seluruh Indonesia
4. **Correlation ≠ causation**: Banyak confounding factors (human activity, wind, fuel load)

## 🎓 Citation

```bibtex
@misc{firewatch2026,
  title={FireWatch Indonesia: Spatiotemporal Analysis of Forest Fire Hotspots},
  author={Your Name},
  year={2026},
  howpublished={\url{https://github.com/yourusername/firewatch-indonesia}}
}
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- NASA FIRMS for active fire data
- NASA POWER for weather data
- GeoJSON Indonesia boundaries

## 📧 Contact

For questions or collaborations: [your.email@example.com]

---

**⭐ If you find this analysis useful, please star this repo!**
