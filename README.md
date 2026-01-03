# SpaceX Falcon 9 Landing Prediction

An end-to-end machine learning project predicting SpaceX Falcon 9 first stage booster landing success with **94.4% accuracy**. This project demonstrates the complete data science lifecycle from data collection to model deployment.

![SpaceX Falcon 9](https://images.unsplash.com/photo-1541185933-ef5d8ed016c2?w=800)

## Live Demo

**[View Live Application](https://spacex-landing-predictor.onrender.com)** *(Link will be active after deployment)*

## Project Highlights

- **94.4% Prediction Accuracy** using Support Vector Machine (SVM)
- **$103M+ Cost Savings** potential through accurate landing predictions
- **90+ Launches Analyzed** with comprehensive feature engineering
- **6 ML Models Compared** including ensemble methods
- **SHAP Model Interpretability** for explainable AI insights

## Key Findings

1. **Simpler Models Win**: SVM (94.4%) outperformed complex ensembles like XGBoost (83.3%) on this small dataset
2. **Landing Infrastructure Critical**: LandingPadUsed is the #1 predictor of success
3. **Experience Matters**: Boosters with prior flights show higher success rates
4. **Payload Impact**: Higher payload mass correlates with better landing outcomes

## Tech Stack

### Data Science & ML
- Python, Pandas, NumPy, Scikit-learn
- XGBoost, LightGBM, CatBoost
- SHAP for model interpretability
- Plotly, Folium for visualizations

### Web Application
- HTML5, CSS3, JavaScript
- Flask & Gunicorn (backend)
- GSAP, AOS for animations
- Chart.js for interactive charts

### Deployment
- Render.com (hosting)
- GitHub (version control)

## Project Structure

```
Capstone Project/
├── Datasets/                    # Raw and processed data files
├── models/                      # Trained ML models (.pkl files)
├── api/                         # FastAPI prediction endpoint
├── webapp/                      # Web application (deployment folder)
│   ├── index.html              # Main webpage
│   ├── styles.css              # Styling
│   ├── app.js                  # Main JavaScript
│   ├── animations.js           # Animation effects
│   ├── server.py               # Flask server
│   ├── data/                   # JSON data for frontend
│   └── images/                 # Visualization images
├── *.ipynb                      # Jupyter notebooks (analysis)
├── DS_capstone_presentation.pdf # Project presentation
└── README.md                    # This file
```

## Notebooks Overview

| Notebook | Description |
|----------|-------------|
| `Data Collection API.ipynb` | SpaceX API data extraction |
| `Data Collection with Web Scrapping.ipynb` | Wikipedia launch data scraping |
| `Data Wrangling.ipynb` | Data cleaning and preparation |
| `EDA with SQL.ipynb` | SQL-based exploratory analysis |
| `EDA with Data Visualization.ipynb` | Visual data exploration |
| `Interactive Visual Analytics with Folium.ipynb` | Geospatial analysis |
| `Advanced_Feature_Engineering.ipynb` | Feature creation and selection |
| `Advanced_ML_Models.ipynb` | Model training and evaluation |
| `Machine Learning Prediction.ipynb` | Final prediction pipeline |

## Run Locally

### Prerequisites
- Python 3.11+
- pip package manager

### Quick Start (Web App Only)

```bash
# Clone the repository
git clone https://github.com/ParshvCrafts/SpaceX-Landing-Predictor.git
cd SpaceX-Landing-Predictor/webapp

# Install dependencies
pip install -r requirements.txt

# Run the server
python server.py
```

Open `http://localhost:8080` in your browser.

### Full Data Science Environment

```bash
# Install all dependencies
pip install -r requirements.txt

# Launch Jupyter
jupyter notebook
```

## Model Performance

| Model | Accuracy | F1-Score |
|-------|----------|----------|
| SVM (RBF Kernel) | **94.4%** | 0.95 |
| Logistic Regression | 83.3% | 0.86 |
| Decision Tree | 77.8% | 0.80 |
| KNN | 83.3% | 0.86 |
| XGBoost | 83.3% | 0.86 |
| LightGBM | 83.3% | 0.86 |

## SHAP Feature Importance

| Feature | SHAP Value | Impact |
|---------|------------|--------|
| LandingPadUsed | 0.681 | Positive |
| ReusedCount | 0.657 | Positive |
| LandingHardwareScore | 0.346 | Positive |
| PayloadMassRelative | 0.320 | Negative |
| Legs | 0.249 | Positive |

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions on Render.com.

**Quick Deploy:**
1. Fork this repository
2. Connect to Render.com
3. Set Root Directory: `webapp`
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn server:app`

## Author

**Parshv Patel**

- [LinkedIn](https://linkedin.com/in/parshv-patel)
- [GitHub](https://github.com/ParshvCrafts)
- [Portfolio](https://parshvpatel.netlify.app/)
- [Email](mailto:parshvpatel09@gmail.com)

## Acknowledgments

- SpaceX for making launch data publicly available
- IBM Data Science Professional Certificate program
- The open-source community for amazing tools and libraries

## License

This project is open source and available under the [MIT License](LICENSE).

---

*Built with data, powered by curiosity.*
