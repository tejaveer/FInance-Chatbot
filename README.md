# FInance-Chatbot
The Finance-Chatbot built with Streamlit and powered by local LLMs (Gemma:2b, Granite3.3:2b), helps with budgeting, savings, and investments. It supports chat and PDF analysis, extracting expenses, generating visual reports, and providing AI insights. Runs locally with no cloud use, ensuring privacy and a user-friendly financial advisor experience.
# 💹 Finance Chatbot

An **AI-powered financial assistant** built with [Streamlit](https://streamlit.io/) and [Ollama](https://ollama.ai/), powered by local LLMs **Gemma:2b** and **Granite3.3:2b**.  
This chatbot helps with **budgeting, investments, savings, and expense analysis** using both chat and PDF insights.

---

## 🚀 Features
- 💬 **Chat Assistant** – Ask about investments, budgeting, or financial advice  
- 📂 **PDF Insights** – Upload PDFs, extract expenses, and auto-generate reports  
- 📊 **Data Visualization** – Pie charts & bar charts for financial insights  
- 🔒 **Privacy First** – Runs locally, no cloud uploads  
- 🤝 **Casual Mode** – Friendly conversations supported  

---

## 🖥️ Tech Stack
- [Streamlit](https://streamlit.io/) – UI Framework  
- [Ollama](https://ollama.ai/) – Local LLM Runner  
- [Gemma:2b](https://huggingface.co/google/gemma-2b) – Finance-focused model  
- [Granite3.3:2b](https://huggingface.co/ibm) – Casual/General text model from [@IBM](https://github.com/IBM)  
- [pdfplumber](https://github.com/jsvine/pdfplumber) – PDF parsing  
- [Matplotlib](https://matplotlib.org/) & [Pandas](https://pandas.pydata.org/) – Data analysis & visualization  

---

## ⚙️ Setup
```bash
# Clone repo
git clone https://github.com/your-username/finance-chatbot.git
cd finance-chatbot

# Install dependencies
pip install -r requirements.txt

# Pull LLM models
ollama pull gemma:2b
ollama pull granite3.3:2b

# Run Streamlit app
streamlit run app.py
