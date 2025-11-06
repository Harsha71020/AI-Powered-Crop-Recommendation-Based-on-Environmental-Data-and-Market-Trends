🌾 AI-Powered Crop Recommendation Based on Environmental Data and Market Trends


An intelligent web-based system that leverages Machine Learning (ML) and data-driven insights to recommend the most suitable crops based on soil conditions, climate, and market trends.


This project aims to assist farmers and agricultural planners in making data-backed crop decisions for better yield and profit.


🚀 Features


✅ Crop Recommendation — Suggests the best crop based on soil nutrients, temperature, humidity, and rainfall.


📈 Market Trend Integration — Considers recent crop demand and price trends.


🧠 Machine Learning Model — Trained using real agricultural datasets (Crop_data.csv).


💾 Database Support — Stores user data and prediction logs using SQLite.


📊 Interactive Dashboard — Displays visual insights and model performance reports.


🧩 User-Friendly Interface — Simple and responsive web frontend built with HTML, CSS, and JS.


🏗️ Project Structure


main/


├── app.py                 # Flask backend for web app


├── database.db            # SQLite database


├── script.js              # Frontend JS logic


│


├── data/


│   └── Crop_data.csv      # Dataset for training/testing


│


├── ml/


│   └── train.py           # Model training script


│


├── ml_models/             # Saved ML models and scalers


│   ├── crop_model.joblib


│   ├── yield_model.joblib


│   ├── label_encoder.joblib


│   ├── scaler.joblib


│   └── sample_data.csv


│


├── static/


│   ├── style.css


│   ├── dashboard.css


│   └── images/


│       ├── apple.png


│       ├── banana.png


│       ├── blackgram.png


│       └── ...


│


├── reports/


│   ├── report.html


│   ├── remidee project.html


│   └── assets/style.css


│


└── screenshots/

    
    └── (test screenshots)




⚙️ Installation & Setup


1️⃣ Clone the repository


git clone https://github.com/Harsha71020/AI-Powered-Crop-Recommendation-Based-on-Environmental-Data-and-Market-Trends.git


cd AI-Powered-Crop-Recommendation-Based-on-Environmental-Data-and-Market-Trends/main


2️⃣ Create a virtual environment


python -m venv venv


venv\Scripts\activate   # On Windows


# OR


source venv/bin/activate   # On Mac/Linux



3️⃣ Install dependencies


pip install -r requirements.txt


(If requirements.txt doesn’t exist, install manually: pip install flask pandas scikit-learn joblib)



4️⃣ Run the application


python app.py


Then open your browser at http://127.0.0.1:5000/

 
 🌐



📊 Machine Learning Overview


Algorithm Used: Random Forest Classifier


Dataset: Crop production and environmental data (temperature, humidity, rainfall, pH, nitrogen, phosphorus, potassium)


Evaluation Metrics: Accuracy, Precision, Recall, F1-Score


Model Output: Recommended crop and expected yield


🧠 Workflow


User inputs environmental parameters 🌡️


Model processes data and normalizes features 📈


Prediction generated from trained model 🧮


Output displayed with insights and confidence level ✅



📷 Screenshots


Login Page	Dashboard	Result Page

	
	
🧾 Reports


Detailed reports on training, accuracy, and results are available under:


main/reports/


You can open report.html to view ML performance metrics.


🔮 Future Enhancements


🌐 Real-time weather API integration


📱 Android app for farmers


💰 Market trend forecasting using live data


🛰️ Satellite-based soil data collection


🧑‍💻 Author


Harsha


📍 Computer Science Engineering Student


💼 Project: AI-Powered Crop Recommendation System


📧 [gggpharshavardhan@gmail.com]

📜 License

This project is licensed under the MIT License — free to use, modify, and distribute.
