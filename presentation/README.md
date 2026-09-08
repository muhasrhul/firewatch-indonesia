# 📊 FireWatch Indonesia - Presentation

Folder ini berisi **Jupyter Notebook** lengkap yang menyajikan seluruh hasil analisis FireWatch Indonesia dalam format storytelling profesional.

## 📁 Contents

### `FireWatch_Indonesia_Report.ipynb`

Notebook lengkap yang mencakup:

1. **Executive Summary** - Ringkasan temuan utama
2. **Dataset Overview** - Karakteristik data NASA FIRMS
3. **Data Inspection & Cleaning** - Proses quality check
4. **Exploratory Data Analysis** - 8 visualisasi temporal & karakteristik
5. **Spatial Analysis** - Analisis per provinsi dengan 3 peta
6. **Weather vs Hotspot** - Analisis korelasi cuaca (3 visualisasi)
7. **Key Insights & Recommendations** - Temuan utama & rekomendasi aksi
8. **Limitations & Future Work** - Keterbatasan & rencana pengembangan

**Total:** 14 visualisasi profesional + narasi lengkap

---

## 🚀 Cara Menggunakan

### 1. Install Dependencies

```bash
pip install -r ../requirements.txt
```

### 2. Jalankan Jupyter Notebook

```bash
jupyter notebook FireWatch_Indonesia_Report.ipynb
```

### 3. Export ke HTML (untuk portfolio website)

```bash
jupyter nbconvert --to html FireWatch_Indonesia_Report.ipynb
```

Akan menghasilkan file `FireWatch_Indonesia_Report.html` yang bisa langsung di-upload ke website portfolio.

### 4. Export ke PDF (untuk presentasi)

```bash
jupyter nbconvert --to pdf FireWatch_Indonesia_Report.ipynb
```

---

## 📊 Key Findings

### 🎯 Top 3 Insights:

1. **Kalimantan** adalah zona kritis (58.5% total hotspot)
2. **Kelembapan** adalah faktor cuaca terkuat (r = -0.786, p < 0.001)
3. **Hari panas** menghasilkan 84% lebih banyak hotspot

### 🗺️ Geographic:

- **Top Province:** Kalimantan Barat (49,645 hotspot)
- **Total Mapped:** 191,697 hotspot (99.4%)

### ⏰ Temporal:

- **Peak Day:** 29 Agustus 2026 (11,100 hotspot)
- **Average:** 5,213 hotspot/hari

### ☁️ Weather Correlation:

| Variable | Correlation | Significance |
|----------|-------------|--------------|
| Kelembapan | r = -0.786 | p < 0.001 ⭐ |
| Suhu | r = +0.597 | p < 0.001 ⭐ |
| Hujan | r = -0.277 | p = 0.146 ✗ |

---

## 💡 Use Cases

### For Portfolio:
- Export to HTML and host on GitHub Pages
- Share direct link to potential employers
- Demonstrates end-to-end data analysis skills

### For Presentation:
- Export to PDF for slide deck
- Run live in Jupyter for interactive demo
- Share notebook via nbviewer

### For Documentation:
- Complete project documentation
- Reproducible analysis workflow
- Teaching material for data analysis

---

## 📈 What This Shows

**Technical Skills:**
- Data cleaning & quality assurance
- Exploratory data analysis (EDA)
- Geospatial analysis with GeoPandas
- Statistical correlation analysis
- Data visualization with matplotlib/seaborn
- Scientific storytelling

**Domain Knowledge:**
- Understanding of satellite remote sensing
- Weather-fire relationship analysis
- Spatial pattern recognition
- Risk assessment & recommendations

---

## 🔗 Related Files

- **Raw Data:** `../data/raw/`
- **Processed Data:** `../data/processed/`
- **Visualizations:** `../images/`
- **Python Scripts:** `../` (root directory)
- **Documentation:** `../README.md`, `../FireWatch Indonesia.md`

---

## 📝 Notes

- **All visualizations** are embedded as images, so the notebook can be viewed even offline
- **All code cells** are included for reproducibility
- **Narrative text** explains each step for easy understanding
- **Professional formatting** ready for portfolio presentation

---

**Created by:** Asrul  
**Date:** September 8, 2026  
**Project:** FireWatch Indonesia
