# 🧠 SmartPrep AI — Mock Interview Coach

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&pause=1000&color=7F77DD&center=true&vCenter=true&width=500&lines=AI-Powered+Mock+Interview+Coach;Paste+JD+%E2%86%92+Practice+%E2%86%92+Get+Feedback;Built+with+Gemini+%2B+Streamlit+%F0%9F%9A%80" alt="Typing SVG" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Gemini%20API-4285F4?style=for-the-badge&logo=google&logoColor=white"/>
  <img src="https://img.shields.io/badge/Status-Live-22c55e?style=for-the-badge"/>
</p>

---

## 🎯 What is SmartPrep AI?

SmartPrep AI is a fully AI-powered mock interview coach. Paste any job description, answer AI-generated questions, and get instant feedback with scores — just like a real interview but without the anxiety.

**Built this because I was job hunting and wanted smarter interview practice. 😄**

---

## ✨ Features

- 🎯 **Custom questions** — AI reads the JD and generates 10 role-specific questions
- 🤖 **Instant feedback** — Score, strengths, improvement tips, and ideal answer for every response
- 📊 **Performance report** — Full session breakdown with overall score
- 📥 **Downloadable report** — Save your results as a text file
- 🔄 **Unlimited sessions** — Practice as many roles as you want, for free

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web UI |
| Google Gemini API | AI question generation + answer evaluation |
| python-dotenv | Secure API key management |

---

## 🚀 Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/Mehakkhannn/smartprep-ai.git
cd smartprep-ai
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up your API key**

Create a `.env` file in the root folder:
```
GEMINI_API_KEY=your_gemini_api_key_here
```
Get your free key at [aistudio.google.com](https://aistudio.google.com)

**4. Run the app**
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser 🎉

---

## 📸 How It Works

```
Paste Job Description  →  AI generates 10 questions
        ↓
  Answer each question  →  AI scores + gives feedback
        ↓
  Full performance report  →  Download & improve
```

---

## 🌐 Deploy for Free (Streamlit Cloud)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub → select this repo → set `app.py` as main file
4. Add `GEMINI_API_KEY` in the Secrets section
5. Click Deploy — your app goes live with a public URL!

---

## 📚 What I Learned

- Prompt engineering for structured AI outputs
- Google Gemini API integration
- Building stateful multi-screen Streamlit apps
- Secure API key management with `.env`
- Deploying Python apps to the cloud

---

## 🤝 Connect

Made with 💜 by **Mehak Khan**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/mehak-khan-611a40284)
[![GitHub](https://img.shields.io/badge/GitHub-Mehakkhannn-181717?style=flat&logo=github)](https://github.com/Mehakkhannn)

---

> ⭐ Star this repo if it helped you — it means a lot!
> [![Live App](https://img.shields.io/badge/Live%20App-Click%20Here-FF4B4B?style=for-the-badge&logo=streamlit)](https://smartprep-ai-fhdrqh5oq3bfgbieyihkz3.streamlit.app)
