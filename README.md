# 🧠 MedChat AI

**MedChat AI** is a privacy-focused medical chatbot that uses a locally hosted Mistral 7B LLM with Retrieval-Augmented Generation (RAG) from the Gale Encyclopedia of Medicine to deliver accurate, context-aware health information. It features a responsive React UI, contextual memory, and location-based doctor recommendations—all with a strong commitment to ethical AI use.

---

## 🚀 Features

- 🔒 **Local LLM**: Runs Mistral 7B via Ollama, ensuring full privacy and offline support.
- 📚 **RAG Knowledge Base**: Uses Gale Encyclopedia of Medicine for accurate, medical-grade responses.
- 🧠 **Contextual Memory**: Maintains conversation history for natural multi-turn dialogue.
- 📍 **Doctor Finder**: Recommends nearby specialists using a location-aware MongoDB dataset.
- 💬 **React + FastAPI Stack**: Modern, mobile-friendly frontend with a robust Python backend.
- ⚠️ **Medical Disclaimer**: Each response includes a built-in notice that it's not a substitute for professional care.

---

## 🛠️ Tech Stack

- **Frontend**: React + TypeScript + Tailwind CSS
- **Backend**: FastAPI + Python
- **LLM**: Mistral 7B (via [Ollama](https://ollama.com/))
- **RAG**: Custom ingestion using Gale Encyclopedia `.txt` files + vector store
- **Database**: MongoDB (for doctor & hospital info)
## Installation

1. Create a Environment

```bash
  python -m venv medbot
  source medbot/bin/activate
```
2. Install required packages
```bash
  pip install -r requirements.txt
```
3. Start Local database with MongoDBCompass and select Database.json file from data directory.

4. Install ollama and download the LLM you want to use.

4. Start backend
```bash
  uvicorn main:app --reload
```
5. Start Frontend
```bash
  cd frontend
  npm install
  npm run dev
```
6. Open localhost with your browser to see the result.
```bash
  http://localhost:5173
```