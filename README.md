# 🎯 Job Recommendation System Using Resume

A machine learning-powered web application that analyzes a candidate's resume (PDF) and recommends the best-fit **companies** and **job roles** based on extracted skills and academic performance.

---

## 📸 Screenshots

> *(Add screenshots of your app here after deployment)*

---

## 🚀 Features

- 📄 **PDF Resume Parsing** — Automatically extracts text from uploaded resumes
- 🧠 **Skill Extraction** — Identifies technical skills using NLP (spaCy) and a LinkedIn skills database
- 🎓 **Education & Marks Detection** — Extracts CGPA, percentage, and degree information
- 🏢 **Company Recommendation** — Uses a CNN deep learning model to predict best-fit companies (Infosys, TCS, Wipro, Cognizant, and more)
- 💼 **Job Role Suggestion** — Maps extracted skills to relevant job roles
- 🔐 **User Authentication** — Register/Login system with SQLite database

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Machine Learning | TensorFlow/Keras (CNN), scikit-learn |
| NLP | spaCy (`en_core_web_sm`), NLTK |
| Resume Parsing | pdfminer.six |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Data | pandas, NumPy |

---

## 📁 Project Structure

```
job-recommendation-using-resume/
│
├── templates/
│   ├── index.html       # Login & Register page
│   ├── upload.html      # Resume upload page
│   └── result.html      # Results display page
│
├── static/
│   ├── first.png        # Background image (index)
│   ├── resume.jpg       # Background image (upload)
│   └── result.jpg       # Background image (result)
│
├── Input resumes/       # Sample resumes for testing
├── app.py               # Main Flask application
├── main.py              # ML model (CNN) + role suggestion logic
├── Book2.csv            # Training dataset
├── linkedin skill       # LinkedIn skills reference file
├── new.db               # SQLite database (auto-created)
├── requirements.txt     # Python dependencies
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Aruneshaaron/job-recommendation-using-resume.git
cd job-recommendation-using-resume
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download spaCy Language Model
```bash
python -m spacy download en_core_web_sm
```

### 5. Download NLTK Stopwords
```python
python -c "import nltk; nltk.download('stopwords')"
```

### 6. Run the Application
```bash
python app.py
```

Open your browser and go to: **http://localhost:800**

---

## 🧪 How It Works

1. User **registers/logs in**
2. User **uploads a PDF resume**
3. The app **extracts** skills, education, and marks using NLP
4. A **CNN model** trained on placement data predicts matching companies
5. A **skill-to-role mapping** suggests relevant job titles
6. Results are displayed on the **results page**

---

## 🏢 Companies in Prediction Model

- Birlasoft
- Cognizant
- Hexaware Technologies
- Infosys
- KPIT Technologies
- L&T Infotech
- Tech Mahindra
- Wipro Technologies
- CSS Corp
- TCS

---

## 📦 Dataset

The model is trained on `Book2.csv`, which contains placement data with:
- Skills Known
- CGPA / Marks
- Department
- Company Placed

---

## 🔮 Future Improvements

- [ ] Save model weights instead of retraining on every prediction
- [ ] Add password hashing for secure authentication
- [ ] Expand the company and role database
- [ ] Add resume scoring/feedback feature
- [ ] Deploy to cloud (Render / Railway / Heroku)

---

## 👨‍💻 Author

**Aruneshwar**  
Final Year Project — Velammal Institute of Technology  
[GitHub Profile](https://github.com/Aruneshaaron)

---

## 📄 License

This project is for educational purposes.
