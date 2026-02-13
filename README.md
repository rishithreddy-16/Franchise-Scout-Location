# Franchise-Scout-Location

# 📍 Franchise Scout: Location Intelligence Tool

## 🚀 Project Overview
A data-driven location intelligence tool designed to identify optimal spots for Quick-Service Restaurant (QSR) expansion. This project leverages **OpenStreetMap (OSM)** data, **Machine Learning**, and **interactive visualization** to analyze competitor density, customer demand drivers, and revenue potential in real-time.

## 🛠️ Tech Stack
- **Python**: Core logic and data processing
- **Streamlit**: Interactive web application framework
- **OSMnx**: Geospatial data retrieval from OpenStreetMap
- **Folium**: Interactive map visualization
- **Pandas & NumPy**: Data structuring and analysis
- **Scikit-learn**: Machine Learning models for revenue forecasting
- **Geopy**: Address geocoding and location search

## 🎯 Current Features
- **🗺️ Interactive Map Interface**: Click anywhere to analyze site potential
- **🔍 Smart Location Search**: Geocode addresses and landmarks instantly
- **🤖 AI-Powered Revenue Forecasting**: Dual ML models for different franchise personas
  - ☕ Premium Cafe Model (leisure-driven)
  - 🍵 Budget Tea Stall Model (traffic-driven)
- **📊 Real-Time Metrics Dashboard**: 
  - Competitor density analysis
  - Demand drivers (schools, offices, universities)
  - Leisure indicators (parks, malls)
- **🎯 Site Verdict System**: AI-generated recommendations (Prime/Viable/Avoid)
- **📏 Adjustable Scan Radius**: Customize analysis area (200m - 2km)

## 🌐 Live Demo
🔗 **Try it now**: [Franchise Scout on Streamlit](https://franchise-scout-location-3erzzcqez46yvm2ecs3fur.streamlit.app/))

## 👤 About the Developer
**Connect with me:**  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rishith-reddy-nomula-612a18237/))

## 🔮 Roadmap
- [ ] **Sentiment Analysis**: NLP integration for competitor review analysis
- [ ] **Demographic Filtering**: Census data integration for customer profiling
- [ ] **ROI Estimator**: Commercial rent data for profitability scoring
- [ ] **Historical Traffic Data**: Pedestrian and vehicle flow analysis
- [ ] **Multi-City Support**: Expand beyond New Jersey/New York
- [ ] **Export Reports**: PDF generation with site analysis summaries

## 📦 Installation & Local Setup

### Prerequisites
```bash
Python 3.8+
```

### Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Franchise-Scout-Location.git
cd Franchise-Scout-Location
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Locally
```bash
streamlit run app.py
```

## 📄 Project Structure
```
Franchise-Scout-Location/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── packages.txt          # System-level dependencies (optional)
└── README.md             # Project documentation
```

## 🧪 How It Works

1. **Data Collection**: Uses OSMnx to query OpenStreetMap for points of interest
2. **Feature Engineering**: Extracts competitor count, demand drivers, and leisure indicators
3. **ML Prediction**: Random Forest models trained on synthetic business logic
4. **Visualization**: Folium maps with interactive click-to-analyze functionality
5. **Decision Support**: AI-generated site verdicts based on revenue thresholds

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License
This project is open source and available under the [MIT License](LICENSE).

## 📧 Contact
For questions or collaboration opportunities, reach out via [LinkedIn](YOUR_LINKEDIN_URL).

---

**Made with ❤️ for data-driven business expansion**
