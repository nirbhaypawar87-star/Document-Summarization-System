# 📄 Document Summarization System

### AI-Powered Document Summarization Using Python, Streamlit and NLP

## 📌 Project Overview

The Document Summarization System is an AI-based web application developed using Python and Streamlit. It automatically generates concise summaries from lengthy documents, helping users understand important information quickly and efficiently.

The system supports multiple document formats, including PDF, DOCX, and TXT. It uses Natural Language Processing (NLP) and a pre-trained transformer model to generate meaningful summaries.

## 🎯 Objectives

- To automatically summarize lengthy documents.
- To reduce the time required to read large documents.
- To extract important information from uploaded files.
- To support multiple document formats.
- To provide downloadable summaries.
- To maintain a history of previously generated summaries.

## ✨ Key Features

### 1. Multiple File Format Support
- Upload PDF documents.
- Upload DOCX documents.
- Upload TXT files.

### 2. AI-Based Text Summarization
- Uses a pre-trained NLP model.
- Generates concise and meaningful summaries.
- Processes lengthy text documents.

### 3. Adjustable Summary Length
- Allows users to control summary length.
- Generates summaries according to user requirements.

### 4. Word Count Analysis
- Displays original document word count.
- Displays summarized text word count.
- Helps understand the reduction in document length.

### 5. Reading Time Estimation
- Estimates the reading time of the original document.
- Helps users save time.

### 6. Download Summary
- Allows users to download generated summaries.
- Makes summarized content easy to save and share.

### 7. Summary History
- Stores previously generated summaries.
- Uses SQLite database for history management.
- Allows users to view and manage saved summaries.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core Programming Language |
| Streamlit | Web Application Framework |
| Hugging Face Transformers | NLP Model Integration |
| DistilBART | Text Summarization |
| PyTorch | Deep Learning Framework |
| PyPDF2 / PDF Library | PDF Text Extraction |
| python-docx | DOCX File Processing |
| SQLite | Database Management |
| Pandas | Data Handling |

## 🤖 Model Used

**Model:** `sshleifer/distilbart-cnn-12-6`

The DistilBART model is a transformer-based language model used for abstractive text summarization. It generates shorter versions of documents while retaining important information.

## 📂 Project Structure

```text
Document_Summarization_System/
│
├── app.py
├── app_backup.py
├── history.py
├── requirements.txt
├── summary_history.db
│
└── README.md
```

## ⚙️ Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/nirbhaypawar87-star/Document-Summarization-System.git
```

### Step 2: Navigate to Project Folder

```bash
cd Document-Summarization-System
```

### Step 3: Create Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
streamlit run app.py
```

### Step 7: Open in Browser

```text
http://localhost:8501
```

## 🔄 System Workflow

1. Open the Document Summarization System.
2. Upload a PDF, DOCX, or TXT file.
3. Extract text from the uploaded document.
4. Select the required summary length.
5. Generate the summary using the NLP model.
6. View the generated summary and word count.
7. Download the summarized content.
8. Access previous summaries through Summary History.

## 🎓 Applications

- Academic Document Summarization
- Research Paper Summarization
- Educational Content Analysis
- Business Document Summarization
- Report Summarization
- Information Management

## ⚠️ Limitations

- Scanned PDF documents may require OCR for text extraction.
- Summary quality depends on the input document and NLP model.
- Very large documents may require additional processing time.
- Generated summaries should be reviewed for accuracy.

## 🔮 Future Enhancements

- Add OCR support for scanned PDF documents.
- Support additional languages.
- Improve summarization accuracy.
- Add user authentication.
- Deploy the application online.

## 👨‍💻 Developer

**Nirbhay Raghunath Pawar**

Computer Engineering Student

PVG's College of Engineering, Pune

## 📜 License

This project is developed for academic and educational purposes.
