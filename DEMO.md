# Swaad - Flavor Profile Recipe Recommendation System

A full-stack application that creates personalized flavor profiles based on your favorite dishes and recommends menu items that match your taste preferences.

---

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.7+** (Python 3.8 or higher recommended)
  - Check your version: `python3 --version` or `python --version`
  - Download from [python.org](https://www.python.org/downloads/) if needed
- **Node.js 16+** and **npm** (Node Package Manager)
  - Check your version: `node --version` and `npm --version`
  - Download from [nodejs.org](https://nodejs.org/) if needed
- **Git** (for cloning the repository)
  - Check your version: `git --version`

### Required Files

Make sure the following file exists in the project root directory:
- `recipes_with_flavour_profiles.csv` - Recipe database with flavor profiles

---

## 📦 Installation

### Step 1: Clone the Repository

If you haven't already, clone or download the project:

```bash
git clone <repository-url>
cd swaad
```

### Step 2: Backend Installation

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a Python virtual environment:**
   ```bash
   python3 -m venv venv
   ```
   
   > **Note:** On Windows, use: `python -m venv venv`

3. **Activate the virtual environment:**
   
   **On macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```
   
   **On Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   > **Tip:** You'll know it's activated when you see `(venv)` at the start of your terminal prompt.

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   This will install all required packages including:
   - FastAPI (web framework)
   - Uvicorn (ASGI server)
   - Pandas (data processing)
   - NumPy (numerical computing)
   - Scikit-learn (machine learning)
   - SQLAlchemy (database ORM)
   - And other dependencies

5. **Verify the CSV file location:**
   ```bash
   # Make sure recipes_with_flavour_profiles.csv is in the project root
   # Path should be: ../recipes_with_flavour_profiles.csv (one level up from backend/)
   ls ../recipes_with_flavour_profiles.csv
   ```

### Step 3: Frontend Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd ../frontend
   ```
   
   (Or from the project root: `cd frontend`)

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```
   
   This will install all required packages including:
   - React (UI framework)
   - Vite (build tool)
   - Axios (HTTP client)
   - Recharts (charting library)
   - And other dependencies

3. **Wait for installation to complete:**
   - This may take a few minutes depending on your internet connection
   - You should see a success message when complete

---

## ▶️ Starting the Application

You have two options for starting the application:

### Option 1: Manual Start (Recommended for Development)

This method gives you more control and better error visibility.

#### Terminal 1 - Start Backend Server

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Activate virtual environment** (if not already activated):
   ```bash
   source venv/bin/activate  # macOS/Linux
   # OR
   venv\Scripts\activate     # Windows
   ```

3. **Start the backend server:**
   ```bash
   python main.py
   ```
   
   You should see output like:
   ```
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

4. **Keep this terminal open** - the backend server must remain running.

✅ **Backend is now running at:** `http://localhost:8000`

#### Terminal 2 - Start Frontend Server

1. **Open a new terminal window/tab**

2. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

3. **Start the frontend development server:**
   ```bash
   npm run dev
   ```
   
   You should see output like:
   ```
   VITE v5.x.x  ready in xxx ms
   
   ➜  Local:   http://localhost:5173/
   ➜  Network: use --host to expose
   ```

4. **Keep this terminal open** - the frontend server must remain running.

✅ **Frontend is now running at:** `http://localhost:5173` (or `http://localhost:3000` depending on your Vite configuration)

#### Access the Application

Open your web browser and navigate to:
- **Frontend:** `http://localhost:5173` or `http://localhost:3000`
- **Backend API:** `http://localhost:8000`
- **API Documentation:** `http://localhost:8000/docs` (FastAPI automatic docs)

### Option 2: Automated Start Script

For convenience, you can use the provided start script:

1. **Make the script executable** (if not already):
   ```bash
   chmod +x start.sh
   ```

2. **Run the start script:**
   ```bash
   ./start.sh
   ```

   This script will:
   - Create a virtual environment if it doesn't exist
   - Install backend dependencies
   - Start the backend server in the background
   - Install frontend dependencies if needed
   - Start the frontend server in the background
   - Display the URLs for both servers

3. **To stop both servers:**
   - Press `Ctrl+C` in the terminal where you ran the script

> **Note:** The automated script is convenient but manual start gives you better visibility into errors and logs.

---

## ✅ Verification Checklist

After starting the application, verify everything is working:

- [ ] Backend server is running (check Terminal 1 for "Uvicorn running" message)
- [ ] Frontend server is running (check Terminal 2 for "Local: http://localhost" message)
- [ ] Can access frontend in browser (no connection errors)
- [ ] Can access backend API docs at `http://localhost:8000/docs`
- [ ] Frontend can communicate with backend (no CORS errors in browser console)

---

## 🧪 Testing the Setup

1. **Open the application** in your browser: `http://localhost:5173` or `http://localhost:3000`

2. **Test the search functionality:**
   - Try searching for dishes like "pizza", "pasta", "chocolate cake"
   - You should see search results from the recipe database

3. **Create a flavor profile:**
   - Add some favorite dishes in each category (appetizers, mains, desserts)
   - Click "Create My Flavor Profile"
   - You should see a radar chart with your flavor preferences

4. **Test menu recommendations:**
   - Upload or paste a menu
   - Click "Get Recommendations"
   - You should see recommended dishes sorted by similarity

---

## 🔧 Troubleshooting

### Backend Issues

**Problem: Backend won't start**
- **Solution 1:** Verify the CSV file exists:
  ```bash
  ls ../recipes_with_flavour_profiles.csv
  ```
  The file must be in the project root, not in the backend directory.

- **Solution 2:** Check if port 8000 is already in use:
  ```bash
  # macOS/Linux
  lsof -i :8000
  # Windows
  netstat -ano | findstr :8000
  ```
  If something is using the port, either stop it or change the port in `main.py`.

- **Solution 3:** Verify virtual environment is activated:
  ```bash
  which python  # Should show path to venv/bin/python
  ```

- **Solution 4:** Reinstall dependencies:
  ```bash
  pip install --upgrade -r requirements.txt
  ```

**Problem: ModuleNotFoundError or ImportError**
- **Solution:** Make sure you're in the virtual environment and dependencies are installed:
  ```bash
  source venv/bin/activate  # macOS/Linux
  pip install -r requirements.txt
  ```

**Problem: Database errors**
- **Solution:** The application will create the database automatically. If you see database errors, check file permissions in the backend directory.

### Frontend Issues

**Problem: Frontend won't start**
- **Solution 1:** Verify Node.js is installed:
  ```bash
  node --version  # Should show v16 or higher
  npm --version
  ```

- **Solution 2:** Clear cache and reinstall:
  ```bash
  rm -rf node_modules package-lock.json
  npm install
  ```

- **Solution 3:** Check if port 3000 or 5173 is already in use:
  ```bash
  # macOS/Linux
  lsof -i :3000
  lsof -i :5173
  ```

**Problem: Cannot connect to backend API**
- **Solution 1:** Verify backend is running first (check Terminal 1)
- **Solution 2:** Check the API URL in `frontend/src/config.js` - it should be `http://localhost:8000`
- **Solution 3:** Check browser console for CORS errors - backend should allow `http://localhost:5173` or `http://localhost:3000`

**Problem: npm install fails**
- **Solution 1:** Clear npm cache:
  ```bash
  npm cache clean --force
  npm install
  ```

- **Solution 2:** Try using a different Node.js version (16+ recommended)

### General Issues

**Problem: Changes not reflecting**
- **Solution:** Both servers support hot-reload. If changes don't appear:
  - Save your files
  - Check terminal for errors
  - Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)

**Problem: OCR/image upload not working**
- **Solution:** OCR features require additional dependencies. Install them:
  ```bash
  cd backend
  source venv/bin/activate
  pip install Pillow easyocr
  # OR
  pip install Pillow pytesseract
  # For pytesseract on macOS: brew install tesseract
  ```

---

## 📖 Usage Guide

### Creating Your Flavor Profile

1. **Enter Favorite Dishes:**
   - Navigate to the profile creation page
   - Enter dishes you like in three categories:
     - **Appetizers/Starters**
     - **Main Courses/Mains**
     - **Desserts**
   - Use the search feature to find dishes from the recipe database
   - You can add multiple dishes in each category

2. **Generate Profile:**
   - Click "Create My Flavor Profile"
   - The system calculates your flavor preferences based on the ingredients in your favorite dishes
   - You'll see a visual radar chart showing your flavor profile

3. **View Your Profile:**
   - See detailed flavor percentages for each category
   - Compare profiles across different meal types
   - Your profile is saved for the current session

### Getting Recommendations

1. **Upload or Enter Menu:**
   - **Option A:** Paste menu text directly into the text area
   - **Option B:** Type dish names (one per line)
   - **Option C:** Upload a menu image (if OCR is enabled)

2. **Process Menu:**
   - The system automatically extracts dish names from the text
   - It recognizes category headers (appetizers, mains, desserts, etc.)
   - Dishes are matched against the recipe database

3. **View Recommendations:**
   - Click "Get Recommendations"
   - Dishes are sorted by flavor similarity to your profile
   - Each recommendation shows:
     - Match percentage
     - Flavor profile comparison
     - Ingredients list (expandable)
   - Higher match percentages indicate better alignment with your preferences

---

## 🏗️ Project Structure

```
swaad/
├── backend/
│   ├── main.py              # FastAPI backend server
│   ├── database.py          # Database models and setup
│   ├── auth.py              # Authentication utilities
│   ├── google_auth.py        # Google OAuth integration
│   ├── requirements.txt     # Python dependencies
│   ├── venv/                # Python virtual environment (created during setup)
│   ├── swaad.db             # SQLite database (created automatically)
│   └── ...
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── DishInput.jsx
│   │   │   ├── FlavorProfile.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── MenuUpload.jsx
│   │   │   ├── Profile.jsx
│   │   │   ├── Recommendations.jsx
│   │   │   └── Signup.jsx
│   │   ├── context/
│   │   │   └── AuthContext.jsx  # Authentication context
│   │   ├── App.jsx          # Main app component
│   │   ├── main.jsx         # Entry point
│   │   ├── config.js        # API configuration
│   │   └── ...
│   ├── package.json         # Node dependencies
│   ├── vite.config.js       # Vite configuration
│   └── ...
├── recipes_with_flavour_profiles.csv  # Recipe database (REQUIRED)
├── start.sh                 # Automated start script
├── README.md                # This file
└── QUICKSTART.md            # Quick reference guide
```

---

## 🔌 API Endpoints

The backend provides the following REST API endpoints:

### Authentication
- `POST /api/signup` - Create a new user account
- `POST /api/login` - Login with email/password
- `POST /api/google-login` - Login with Google OAuth
- `GET /api/me` - Get current user information (protected)

### Profile & Recommendations
- `POST /api/create-profile` - Create user flavor profile from liked dishes
- `POST /api/process-menu` - Extract dish names from menu text
- `POST /api/recommendations` - Get dish recommendations based on profile and menu
- `GET /api/search-recipes` - Search for recipes by name

### Documentation
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

All endpoints are prefixed with `/api` except the documentation endpoints.

---

## 🛠️ Technologies Used

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - ASGI server for running FastAPI
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning (cosine similarity for recommendations)
- **SQLAlchemy** - Database ORM
- **Python-JOSE** - JWT token handling
- **Passlib** - Password hashing
- **Pillow** - Image processing (for OCR)
- **EasyOCR/PyTesseract** - Optical Character Recognition (optional)

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Axios** - HTTP client for API calls
- **Recharts** - Charting library for flavor profile visualization
- **React OAuth Google** - Google authentication integration

### Data
- **CSV-based recipe database** - Recipe data with pre-calculated flavor profiles
- **SQLite** - User database (created automatically)

---

## 🎯 Features

### Core Features
- **Flavor Profile Creation**: Enter your favorite dishes to create a personalized flavor profile
- **Menu Processing**: Upload or paste menu text to extract dish names
- **Smart Recommendations**: Get dish recommendations based on flavor profile similarity matching
- **Visual Flavor Profiles**: Interactive radar charts showing your flavor preferences
- **Recipe Search**: Search the recipe database by dish name

### Advanced Features
- **Menu Image Upload**: Upload photos of menus and automatically extract text using OCR
- **Smart Menu Parsing**: Recognizes category synonyms (appetizers/starters, mains/main course, etc.)
- **User Authentication**: Sign up, login, and Google OAuth integration
- **User Profiles**: Save and manage your flavor preferences
- **Flavor Profile Matching**: Uses cosine similarity to match user preferences with menu items

---

## 📝 Technical Details

### How It Works

1. **Flavor Profile Calculation:**
   - Each recipe has a flavor profile based on its ingredients
   - User's flavor profile is calculated as a weighted average of their favorite dishes
   - Profiles are represented as vectors with flavor dimensions (sweet, salty, sour, bitter, umami, spicy, etc.)

2. **Recommendation Algorithm:**
   - Uses cosine similarity to compare user's flavor profile with menu items
   - Higher similarity scores indicate better matches
   - Recommendations are sorted by match percentage

3. **Menu Processing:**
   - Text input: Uses regex and heuristics to extract dish names
   - Image input: Uses OCR (EasyOCR or Tesseract) to extract text, then processes as text

4. **Recipe Matching:**
   - Uses fuzzy string matching to find recipes by name
   - Handles variations in dish names and spelling

### Data Requirements

- **recipes_with_flavour_profiles.csv**: Must be in the project root directory
  - Contains recipe data with pre-calculated flavor profiles
  - Required columns: recipe name, ingredients, flavor profile vector
  - The system loads this file on startup

---

## 🔐 Environment Variables (Optional)

For production or advanced configuration, you can set these environment variables:

### Backend
- `FRONTEND_URL` - Frontend URL for CORS configuration
- `GOOGLE_CLIENT_ID` - Google OAuth client ID
- `SECRET_KEY` - Secret key for JWT tokens (auto-generated if not set)
- `DATABASE_URL` - Database connection string (defaults to SQLite)

### Frontend
- `VITE_API_URL` - Backend API URL (defaults to `http://localhost:8000`)

Create a `.env` file in the backend directory for environment variables.

---

## 🚀 Deployment

### Backend Deployment

The backend can be deployed to:
- **Railway** - See `backend/railway.json` for configuration
- **Heroku** - See `backend/Procfile` for process configuration
- **Any platform supporting Python/ASGI**

### Frontend Deployment

The frontend can be deployed to:
- **Vercel** - See `frontend/vercel.json` for configuration
- **Netlify** - See `frontend/netlify.toml` for configuration
- **Any static hosting service**

Remember to:
1. Set `VITE_API_URL` environment variable to your backend URL
2. Update CORS settings in backend to allow your frontend domain
3. Ensure `recipes_with_flavour_profiles.csv` is accessible to the backend

---

## 📚 Additional Resources

- **Quick Start Guide**: See `QUICKSTART.md` for a condensed startup guide
- **API Documentation**: Visit `http://localhost:8000/docs` when backend is running
- **FastAPI Docs**: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **React Docs**: [https://react.dev/](https://react.dev/)
- **Vite Docs**: [https://vitejs.dev/](https://vitejs.dev/)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

[Add your license information here]

---

## 🆘 Getting Help

If you encounter issues:

1. Check the **Troubleshooting** section above
2. Review the terminal output for error messages
3. Check browser console for frontend errors
4. Verify all prerequisites are installed correctly
5. Ensure both servers are running
6. Check that `recipes_with_flavour_profiles.csv` is in the correct location

---

## 🎉 Next Steps

Once your application is running:

1. **Explore the UI** - Navigate through the different pages
2. **Create a Profile** - Add your favorite dishes and see your flavor profile
3. **Try Recommendations** - Upload a menu and get personalized suggestions
4. **Check the API** - Visit `http://localhost:8000/docs` to explore the API
5. **Customize** - Modify the code to add new features or improve existing ones

Enjoy using Swaad! 🍽️
