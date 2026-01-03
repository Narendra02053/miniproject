# Memory Decay Predictor

A full-stack web application that predicts when you might forget learned material based on various factors like study time, confidence level, difficulty, mood, and more. The application uses machine learning to help optimize your study schedule through spaced repetition.

## ⚡ Quick Start (Windows PowerShell)

```powershell
# Backend Setup (Terminal 1)
cd "backend (3)\backend\backend"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload

# Frontend Setup (Terminal 2)
cd "frontend (2)\frontend\frontend"
npm install
npm run dev
```

Then visit: **http://localhost:5173**

## 📋 Table of Contents

- [Quick Start](#quick-start-windows-powershell)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Testing](#testing)

## ✨ Features

- **Secure Authentication**: Email/password login with bcrypt encryption and MongoDB persistence
- **Memory Decay Prediction**: ML-powered prediction of days until review needed using XGBoost and scikit-learn
- **AI-Powered Chat**: Real-time study assistance powered by Groq's LLaMA 3.1 model
- **Notes Management**: Create, update, and delete study notes with persistent storage
- **Personalized User Sessions**: All predictions and chat history tied to user email
- **Input-Based Predictions**: Each unique input combination produces distinct predictions based on ML model
- **Protected Routes**: Authentication required for accessing predictions and chat features

## 🛠️ Tech Stack

**Backend:**
- Python 3.8+
- FastAPI (modern async web framework)
- PyTorch (deep learning)
- XGBoost & scikit-learn (machine learning models)
- MongoDB (user data, predictions, chat history)
- Groq API (AI-powered chat with LLaMA 3.1)
- Uvicorn (ASGI server)
- Passlib with bcrypt (password hashing)

**Frontend:**
- React 18.2.0
- Vite (fast build tool)
- React Router DOM (client-side routing)
- Axios (HTTP client)

**ML Libraries:**
- Transformers (NLP preprocessing)
- Sentencepiece (tokenization)
- Pandas & NumPy (data manipulation)

## 🔧 Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software

1. **Python 3.8 or higher**
   - Check version: `python --version` or `python3 --version`
   - Download: [Python Official Website](https://www.python.org/downloads/)

2. **Node.js 16 or higher and npm**
   - Check version: `node --version` and `npm --version`
   - Download: [Node.js Official Website](https://nodejs.org/)

3. **Git** (optional, for cloning the repository)
   - Download: [Git Official Website](https://git-scm.com/downloads)

### Optional Software

- **MongoDB** (required for user login and data persistence)
  - MongoDB powers user authentication, prediction history, and chat history
  - Download: [MongoDB Official Website](https://www.mongodb.com/try/download/community)
  - Or use MongoDB Atlas (cloud-based): [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

- **Groq API Key** (required for AI chat feature)
  - Free API key: [Groq Console](https://console.groq.com)

## 📦 Installation

### Step 1: Clone or Download the Project

If you have the project files, navigate to the project directory:

```powershell
cd memorydecaystudy-main
cd memorydecaystudy-main
```

### Step 2: Backend Setup

1. **Navigate to the backend directory:**
   ```powershell
   cd "backend (3)\backend\backend"
   ```

2. **Create a virtual environment:**
   ```powershell
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   *If you get an execution policy error, run:*
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

4. **Install Python dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
   
   **Note:** This may take several minutes as it installs machine learning libraries (PyTorch, XGBoost, scikit-learn, etc.)

5. **Create a `.env` file for configuration:**
   
   Create a file named `.env` in the `backend (3)/backend/` directory:
   
   ```env
   MONGO_URI=mongodb://127.0.0.1:27017
   DB_NAME=memory_decay_db
   GROQ_API_KEY=your_groq_api_key_here
   ```
   
   - **MONGO_URI**: Your MongoDB connection string (local or Atlas)
   - **DB_NAME**: Name of your MongoDB database
   - **GROQ_API_KEY**: Get free key from [Groq Console](https://console.groq.com)

### Step 3: Frontend Setup

1. **Navigate to the frontend directory:**
   
   From project root:
   ```powershell
   cd "frontend (2)\frontend\frontend"
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```
   
   This will install React, Vite, Axios, and other frontend dependencies.

### Step 4: Verify Backend Connection

Before running, ensure the backend API URL is correctly configured:

1. Open `frontend (2)/frontend/src/services/api.jsx`
2. Verify the API base URL points to your backend (default: `http://127.0.0.1:8000`)

## 🚀 Running the Application

You need to run both the backend and frontend servers. Open **two separate terminal windows**.

### Terminal 1: Backend Server

1. **Navigate to backend directory:**
   ```powershell
   cd "backend (3)\backend\backend"
   ```

2. **Activate virtual environment:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

3. **Start the backend server:**
   ```powershell
   python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
   ```
   
   You should see output like:
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
   INFO:     Started server process
   INFO:     Application startup complete.
   ```

### Terminal 2: Frontend Server

1. **Navigate to frontend directory:**
   ```powershell
   cd "frontend (2)\frontend\frontend"
   ```

2. **Start the frontend development server:**
   ```powershell
   npm run dev
   ```
   
   You should see output like:
   ```
   VITE v5.x.x  ready in xxx ms
   
   ➜  Local:   http://localhost:5173/
   ➜  Network: use --host to expose
   ```

### Access the Application

Once both servers are running:

- **Frontend (Main Application):** http://localhost:5173
- **Backend API:** http://127.0.0.1:8000
- **API Documentation (Swagger UI):** http://127.0.0.1:8000/docs
- **Alternative API Docs (ReDoc):** http://127.0.0.1:8000/redoc

## 🔐 Authentication & Workflows

### First-Time User Registration
1. Visit http://localhost:5173/login
2. Enter an email and password
3. Click **Continue** to create your account
4. The system automatically creates your user record in MongoDB
5. You'll be redirected to the prediction dashboard

### Returning Users
1. Enter your registered email and password
2. Click **Continue** to log in
3. Your prediction history and chat messages load automatically

### Protected Routes
- `/` (Prediction Dashboard) - Requires authentication
- `/chat` (Chat Assistant) - Requires authentication
- `/login` (Login Page) - Public

## 📁 Project Structure

```
memorydecaystudy-main/
├── backend (3)/
│   └── backend/
│       ├── app.py                      # FastAPI application entry point
│       ├── requirements.txt            # Python dependencies
│       ├── .env                        # Environment variables (create this)
│       ├── models/                     # ML model files (pickle files)
│       │   ├── memory_model.pkl
│       │   ├── scaler.pkl
│       │   └── label_encoders.pkl
│       ├── routes/                     # API route handlers
│       │   ├── __init__.py
│       │   ├── auth_routes.py          # Login/registration endpoints
│       │   ├── prediction_routes.py    # Memory prediction endpoints
│       │   ├── chat_routes.py          # Chat assistant endpoints
│       │   └── notes_routes.py         # Notes management endpoints
│       ├── services/                   # Business logic layer
│       │   ├── __init__.py
│       │   ├── prediction_service.py   # ML prediction logic
│       │   ├── preprocess.py           # Data preprocessing
│       │   ├── chat_service.py         # Groq AI integration
│       │   └── note_service.py         # Notes business logic
│       ├── db/                         # Database models & connection
│       │   ├── __init__.py
│       │   ├── connection.py           # MongoDB connection setup
│       │   ├── user_model.py           # User collection schema
│       │   ├── prediction_model.py     # Predictions collection
│       │   ├── chat_model.py           # Chat history collection
│       │   └── notes_model.py          # Notes collection
│       ├── api/                        # Vercel serverless functions
│       │   └── index.py
│       └── venv/                       # Virtual environment (don't commit)
│
└── frontend (2)/
    └── frontend/
        ├── package.json                # Node.js dependencies
        ├── vite.config.jsx             # Vite configuration
        ├── src/
        │   ├── main.jsx                # React entry point
        │   ├── app.jsx                 # Main router component
        │   ├── index.css               # Global styles
        │   ├── pages/
        │   │   ├── Login.jsx           # Login page
        │   │   ├── Predict.jsx         # Prediction dashboard
        │   │   └── Chat.jsx            # Chat assistant page
        │   ├── components/
        │   │   ├── Navbar.jsx          # Navigation bar
        │   │   ├── ProtectedRoute.jsx  # Auth guard for routes
        │   │   └── AuthContext.jsx     # Auth state management
        │   ├── context/
        │   │   └── AuthContext.jsx     # User authentication context
        │   └── services/
        │       ├── api.jsx             # Axios instance & config
        │       ├── authApi.js          # Auth API calls
        │       └── chatApi.js          # Chat API calls
        └── dist/                       # Build output (generated)
```

## 📡 API Documentation

All API endpoints require proper request/response formatting. The backend includes Swagger UI for interactive testing.

### Authentication Endpoints

**POST** `/api/auth/register`
Register a new user.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "User registered successfully",
  "user_id": "uuid"
}
```

**POST** `/api/auth/login`
Authenticate an existing user.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Login successful",
  "user_id": "uuid"
}
```

### Prediction Endpoints

**POST** `/api/predict/`
Get memory decay prediction.

**Request:**
```json
{
  "email": "user@example.com",
  "topic_name": "Neuroplasticity",
  "category": "science",
  "domain": "school",
  "category_type": "concept",
  "study_time": 1.5,
  "review_count": 2,
  "confidence": 4,
  "difficulty": "medium",
  "stress_level": 2,
  "sleep_hours": 7.5,
  "mood": "calm",
  "distraction_level": 1,
  "recent_event": "none",
  "attention_level": 4
}
```

**Response:**
```json
{
  "status": "success",
  "prediction": 5.23
}
```

**GET** `/api/predict/{email}`
Retrieve user's prediction history (last 10 predictions).

**Response:**
```json
{
  "status": "success",
  "predictions": [
    {
      "topic_name": "Neuroplasticity",
      "prediction": 5.23,
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Chat Endpoints

**POST** `/api/chat/`
Send a message to the AI study assistant.

**Request:**
```json
{
  "email": "user@example.com",
  "message": "How can I improve my memory retention?"
}
```

**Response:**
```json
{
  "status": "success",
  "reply": "Here are some effective strategies for improving memory retention..."
}
```

**GET** `/api/chat/{email}`
Get chat history for a user.

**Response:**
```json
{
  "status": "success",
  "chat_history": [
    {
      "role": "user",
      "message": "How can I improve my memory retention?",
      "timestamp": "2024-01-15T10:30:00Z"
    },
    {
      "role": "bot",
      "message": "Here are some effective strategies...",
      "timestamp": "2024-01-15T10:31:00Z"
    }
  ]
}
```

### Notes Endpoints

**GET** `/api/notes/{email}`
Get all notes for a user.

**POST** `/api/notes/`
Create a new note.

**Request:**
```json
{
  "email": "user@example.com",
  "title": "Memory Techniques",
  "content": "Note content here..."
}
```

**PUT** `/api/notes/{note_id}`
Update an existing note.

**DELETE** `/api/notes/{note_id}`
Delete a note.

For detailed interactive API documentation, visit: http://127.0.0.1:8000/docs

## 🧪 Testing

### Test Backend Functionality

Run the comprehensive test suite:

```powershell
cd "backend (3)\backend\backend"
python test_backend.py
```

This tests:
- Database connections
- Authentication endpoints
- Prediction accuracy

### Test Input Variation

Verify that different inputs produce different predictions:

```powershell
cd "backend (3)\backend\backend"
python test_all_features.py
```

### Test Specific Features

**Test Categorical Predictions:**
```powershell
python test_categorical.py
```

**Test Chat Functionality:**
```powershell
python test_chat.py
```

**Test Encoding:**
```powershell
python test_encoding.py
```

## 🔍 Troubleshooting

### Backend Issues

**Problem: Module not found errors**
- **Solution:** Ensure virtual environment is activated and dependencies are installed:
  ```bash
  pip install -r requirements.txt
  ```

**Problem: Model files not found**
- **Solution:** Ensure all `.pkl` files exist in `models/` directory:
  - `memory_model.pkl`
  - `scaler.pkl`
  - `label_encoders.pkl`

**Problem: Port 8000 already in use**
- **Solution:** Either kill the process or use a different port:
  ```powershell
  # Find and kill process using port 8000
  netstat -ano | findstr :8000
  taskkill /PID <process_id> /F
  
  # Or use a different port
  cd "backend (3)\backend\backend"
  python -m uvicorn app:app --host 127.0.0.1 --port 8001 --reload
  ```
  Then update frontend API URL in `frontend (2)/frontend/frontend/src/services/api.jsx`

**Problem: MongoDB connection errors**
- **Solution:** 
  - Ensure MongoDB is running locally (on Windows, MongoDB service should be running):
    ```powershell
    # Check if MongoDB service is running
    Get-Service MongoDB | Select-Object Status
    
    # Or start mongod if running standalone
    mongod
    ```
  - Check MONGO_URI in `.env` file
  - Verify MongoDB is accessible at the URI specified
  - Default local connection: `mongodb://127.0.0.1:27017`

**Problem: GROQ_API_KEY not found**
- **Solution:**
  - Get a free API key from [Groq Console](https://console.groq.com)
  - Add it to your `.env` file: `GROQ_API_KEY=your_key_here`

**Problem: Python version compatibility**
- **Solution:** Ensure Python 3.8+:
  ```bash
  python --version
  ```

### Frontend Issues

**Problem: npm install fails**
- **Solution:**
  ```powershell
  # Clear npm cache
  npm cache clean --force
  
  # Delete node_modules and package-lock.json
  Remove-Item node_modules -Recurse -Force
  Remove-Item package-lock.json
  
  # Reinstall
  npm install
  ```

**Problem: Frontend can't connect to backend**
- **Solution:**
  - Ensure backend is running on http://127.0.0.1:8000
  - Check browser console for CORS errors
  - Verify API URL in `frontend (2)/frontend/frontend/src/services/api.jsx`

**Problem: Port 5173 already in use**
- **Solution:** Vite will auto-select the next available port, or specify:
  ```powershell
  npm run dev -- --port 3000
  ```
  Or find and kill the process:
  ```powershell
  netstat -ano | findstr :5173
  taskkill /PID <process_id> /F
  ```

**Problem: Blank page or 404 on load**
- **Solution:**
  - Clear browser cache (Ctrl+Shift+Delete)
  - Ensure you're accessing http://localhost:5173
  - Check that frontend dev server is running

### Authentication Issues

**Problem: Login fails with "User not found"**
- **Solution:**
  - Register first if this is your first time
  - Check MongoDB is running
  - Verify email and password are correct

**Problem: Can't access protected routes**
- **Solution:**
  - Log in first at http://localhost:5173/login
  - Check browser console for auth errors
  - Clear browser localStorage and try again

### Data & ML Issues

**Problem: All predictions are the same value**
- **Solution:**
  - Verify ML model files exist in `models/` directory
  - Check that input data is properly preprocessed
  - Review `preprocess.py` for encoding issues

**Problem: Different inputs produce same prediction**
- **Solution:**
  - Ensure sufficient variety in input values
  - Check that categorical variables are properly encoded
  - Run `test_all_features.py` to debug

## 🛠️ Development & Deployment

### Building for Production

**Frontend:**
```powershell
cd "frontend (2)\frontend\frontend"
npm run build
```

Build output will be in `dist/` directory.

**Backend (Uvicorn):**
```powershell
cd "backend (3)\backend\backend"
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

**Backend (Production with Gunicorn - Linux/Mac only):**
```bash
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker
```

**Backend (Windows using Waitress - Recommended):**
```powershell
pip install waitress
waitress-serve --port=8000 app:app
```

### Environment Configuration

Create `.env` with these variables for production:

```env
MONGO_URI=your_production_mongodb_uri
DB_NAME=memory_decay_db
GROQ_API_KEY=your_groq_api_key
ENVIRONMENT=production
```

## 📝 Important Notes

- **ML Models:** Required model files must be present in `models/` directory
- **MongoDB:** Essential for login, predictions history, and chat memory
- **Groq API:** Free tier available; required for AI chat feature
- **CORS:** Backend includes CORS middleware for frontend integration
- **Security:** Passwords are hashed with bcrypt; never store plain text passwords
- **Predictions:** Different input combinations produce different values based on the trained ML model

## 📄 License

This project is for educational purposes.

## 🤝 Support & Contributions

If you encounter issues:
1. Check the **Troubleshooting** section above
2. Verify all prerequisites are installed correctly
3. Ensure both backend and frontend servers are running
4. Check terminal output for error messages
5. Visit the interactive API docs: http://127.0.0.1:8000/docs
6. Review logs in both backend and frontend terminals

For contributions or feedback, feel free to submit issues or pull requests.

---

**Happy Learning! 🎓**
