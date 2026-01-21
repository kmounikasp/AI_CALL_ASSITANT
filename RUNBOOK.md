# AI Call Assistant - Runbook

This guide explains how to set up and run the AI Call Assistant on your local machine.

## Prerequisites
- **Node.js**: v18 or later
- **Python**: 3.8 or later
- **OpenAI API Key**: Required for AI features (sentiment, coaching, keywords)

---

## 1. Environment Configuration

### PowerShell Execution Policy
If you get an error that scripts are disabled in PowerShell, run this command:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

### API Key
Create a `.env` file in the `backend` folder and add your key:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 2. Backend Setup & Run

1. **Navigate to backend folder**:
   ```bash
   cd backend
   ```
2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   ```
3. **Install Dependencies**:
   ```bash
   .\venv\Scripts\pip install -r requirements.txt
   ```
4. **Start Server**:
   ```bash
   .\venv\Scripts\python main.py
   ```
   *The backend will run on `http://localhost:8000`*

---

## 3. Frontend Setup & Run

1. **Navigate to frontend folder**:
   ```bash
   cd frontend
   ```
2. **Install Dependencies**:
   ```bash
   npm install
   ```
3. **Start Dev Server**:
   ```bash
   npm run dev
   ```
   *The frontend will run on `http://localhost:5173`*

---

## 4. How to Use

1. Open **`http://localhost:5173`** in your browser.
2. Click **"Start New Call"**.
3. **Voice Input**: Click the Microphone icon to start speaking. It will turn red and pulse.
4. **Text Input**: Type in the "Simulate customer speech..." box and press Enter.
5. **Dashboard**: 
   - **Product Recs**: Shows suggested products based on keywords.
   - **Live Sentiment**: Shows if the customer is Positive, Negative, or Neutral.
   - **Sales Coaching**: Gives real-time advice on what to say next.

---

## Troubleshooting

- **No recommendations?**: Ensure the backend is running. If your OpenAI API key has no credits, the system uses a fallback keyword matching list.
- **Microphone not working?**: Ensure you allow microphone access in your browser when prompted.
- **Port already in use?**: If you get a port error, close any existing terminal windows running the app or restart your computer.
