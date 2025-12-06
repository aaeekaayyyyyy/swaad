# Quick Start Guide

## 🚀 Running the Application

### Method 1: Run Both Servers Manually (Recommended)

#### Terminal 1 - Backend Server

```bash
# Navigate to backend
cd backend

# Create virtual environment (first time only)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Run the backend server
python main.py
```

✅ Backend will be running at: **http://localhost:8000**

#### Terminal 2 - Frontend Server

```bash
# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Run the frontend server
npm run dev
```

✅ Frontend will be running at: **http://localhost:3000**

---

### Method 2: Using the Start Script

```bash
# Make sure the script is executable (already done)
./start.sh
```

This will start both servers automatically.

---

Once you are up and running and you have entered your favorite recipes/dishes we have provided a sample menu in menu.txt for a faster execution.

---

## 📝 First Time Setup Checklist

- [ ] Python 3.7+ installed
- [ ] Node.js and npm installed
- [ ] `recipes_with_flavour_profiles.csv` is in the project root
- [ ] Backend dependencies installed (`pip install -r backend/requirements.txt`)
- [ ] Frontend dependencies installed (`npm install` in frontend directory)

---

## 🧪 Test the Setup

1. Open **http://localhost:3000** in your browser
2. You should see the Swaad welcome screen
3. Try searching for a dish (e.g., "pizza", "pasta", "chocolate cake")
4. Add some dishes and create your profile

---

## ⚠️ Troubleshooting

### Backend won't start?
- Make sure `recipes_with_flavour_profiles.csv` is in the project root (not in backend/)
- Check if port 8000 is already in use
- Verify Python virtual environment is activated

### Frontend won't start?
- Make sure Node.js is installed: `node --version`
- Delete `node_modules` and run `npm install` again
- Check if port 3000 is already in use

### API errors?
- Make sure backend is running first
- Check browser console for CORS errors
- Verify backend is accessible at http://localhost:8000

---

## 🎯 Next Steps

Once both servers are running:
1. Go to http://localhost:3000
2. Enter your favorite dishes
3. Create your flavor profile
4. Upload a menu
5. Get recommendations!

