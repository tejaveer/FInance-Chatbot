import streamlit as st
import requests
from datetime import datetime
import pdfplumber
import re
import pandas as pd
import matplotlib.pyplot as plt

# --- Streamlit Page Setup ---
st.set_page_config(
    page_title="Finance Chatbot",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2331/2331947.png", width=80)
    st.title("Finance Chatbot 💹")
    st.markdown("AI-powered assistant for **finance, expenses & investments**.")
    st.divider()
    st.markdown("⚙️ **Setup**")
    st.code("ollama pull gemma:2b", language="bash")
    st.code("ollama pull granite3.3:2b", language="bash")
    st.code("streamlit run app.py", language="bash")
    st.divider()
    st.caption("Powered by Gemma:2b, Granite3.3 & Streamlit")

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a professional financial assistant."}
    ]
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "pdf_text" not in st.session_state:
    st.session_state["pdf_text"] = ""
if "pdf_history" not in st.session_state:   # NEW: store past uploads
    st.session_state["pdf_history"] = []

# --- Main Layout with Tabs ---
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📂 PDF Insights", "ℹ️ About"])

# ----------------- TAB 1: Chat -----------------
with tab1:
    st.header("💬 Financial Assistant")
    st.write("Ask me about **investments, budgeting, savings, or financial advice.**")

    # Display chat history
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.chat_message("user").markdown(msg["content"])
        elif msg["role"] == "assistant":
            st.chat_message("assistant").markdown(msg["content"])

    # Chat input
    if user_input := st.chat_input("Type your financial question here..."):
        st.session_state["messages"].append({"role": "user", "content": user_input})
        st.chat_message("user").markdown(user_input)

        # --- Decide which model to use ---
        casual_triggers = ["hi", "hello", "hey", "good morning", "good evening", "how are you", "what’s up"]
        if any(trigger in user_input.lower() for trigger in casual_triggers):
            model_to_use = "granite3.3:2b"  # ✅ IBM Granite via Ollama
        else:
            model_to_use = "gemma:2b"       # ✅ Finance-focused Gemma

        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": model_to_use,
                    "messages": st.session_state["messages"],
                    "stream": False
                }
            )
            if response.status_code == 200:
                data = response.json()
                bot_reply = data["message"]["content"]
            else:
                bot_reply = f"⚠️ Error: {response.text}"
        except Exception as e:
            bot_reply = f"❌ Could not connect to Ollama: {e}"

        st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
        st.chat_message("assistant").markdown(bot_reply)

        st.session_state["chat_history"].append(
            {"timestamp": datetime.now().strftime("%H:%M:%S"), "user": user_input, "bot": bot_reply}
        )

# ----------------- TAB 2: PDF Insights -----------------
with tab2:
    st.header("📂 Upload PDF for Financial Insights")

    pdf_file = st.file_uploader("📂 Upload a PDF with your expenses/income", type=["pdf"])
    if pdf_file:
        with pdfplumber.open(pdf_file) as pdf:
            extracted_text = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
            st.session_state["pdf_text"] = extracted_text

        st.success("✅ PDF uploaded and text extracted!")
        st.text_area("📄 Extracted Data", st.session_state["pdf_text"], height=200)

        # --- Try to parse expenses automatically ---
        expenses = []
        for line in st.session_state["pdf_text"].splitlines():
            match = re.match(r"([A-Za-z\s]+)\s+(\d+)", line.strip())
            if match:
                category = match.group(1).strip()
                amount = float(match.group(2))
                expenses.append({"Category": category, "Amount": amount})

        df = None
        if expenses:
            df = pd.DataFrame(expenses)
            st.subheader("📊 Parsed Expenses")
            st.dataframe(df)

            # --- Pie Chart ---
            fig1, ax1 = plt.subplots()
            df.groupby("Category")["Amount"].sum().plot.pie(
                autopct="%1.1f%%", ax=ax1, ylabel=""
            )
            st.pyplot(fig1)

            # --- Bar Chart ---
            fig2, ax2 = plt.subplots()
            df.groupby("Category")["Amount"].sum().sort_values(ascending=False).plot.bar(
                ax=ax2
            )
            ax2.set_ylabel("Amount")
            ax2.set_title("Expenses by Category")
            st.pyplot(fig2)

        # --- Button to Analyze with LLM ---
        if st.button("🔎 Analyze PDF Data"):
            try:
                response = requests.post(
                    "http://localhost:11434/api/chat",
                    json={
                        "model": "gemma:2b",
                        "messages": [
                            {"role": "system", "content": "You are a financial analyst."},
                            {"role": "user", "content": f"Here is my financial data:\n{st.session_state['pdf_text']}\n\nPlease analyze my income, expenses, and savings. Give me insights."}
                        ],
                        "stream": False
                    }
                )
                if response.status_code == 200:
                    analysis = response.json()["message"]["content"]
                    st.subheader("🤖 PDF Analysis by AI")
                    st.write(analysis)

                    # Save history
                    st.session_state["pdf_history"].append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "text": st.session_state["pdf_text"],
                        "df": df,
                        "analysis": analysis
                    })

                else:
                    st.error(f"⚠️ Error: {response.text}")
            except Exception as e:
                st.error(f"❌ Could not analyze PDF: {e}")

    # --- Show PDF Analysis History ---
    if st.session_state["pdf_history"]:
        st.divider()
        st.subheader("📜 PDF Analysis History")
        for i, entry in enumerate(st.session_state["pdf_history"][::-1]):
            with st.expander(f"📂 Analysis from {entry['timestamp']}"):
                st.text_area("Extracted Data", entry["text"], height=150)
                if entry["df"] is not None:
                    st.dataframe(entry["df"])

                    # Re-plot charts
                    fig1, ax1 = plt.subplots()
                    entry["df"].groupby("Category")["Amount"].sum().plot.pie(
                        autopct="%1.1f%%", ax=ax1, ylabel=""
                    )
                    st.pyplot(fig1)

                    fig2, ax2 = plt.subplots()
                    entry["df"].groupby("Category")["Amount"].sum().sort_values(ascending=False).plot.bar(ax=ax2)
                    ax2.set_ylabel("Amount")
                    ax2.set_title("Expenses by Category")
                    st.pyplot(fig2)

                st.markdown("### 🤖 Previous Analysis")
                st.write(entry["analysis"])

# ----------------- TAB 3: About -----------------
with tab3:
    st.header("ℹ️ About This App")
    st.write("""
    This chatbot is built using:
    - **[Streamlit](https://streamlit.io/)** for the user interface  
    - **[Ollama](https://ollama.ai/)** for running local LLMs  
    - **Gemma:2b** for finance-focused reasoning  
    - **Granite 3.3:2B** for casual/basic text generation  

    💡 Use this assistant for:
    - Budget planning  
    - Investment suggestions  
    - Expense analysis (manual or via PDF upload)  
    - General financial queries  
    - Small talk & casual conversation  
    """)
    st.success("Your data stays local — no cloud uploads required ✅")

