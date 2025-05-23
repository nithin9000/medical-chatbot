
# Project Title

MedBot is a medical chatbot!


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