# WashEase – Digital Laundry Service Platform

WashEase is a full-stack, AI-integrated digital laundry management system. It provides users with an easy way to book laundry services with AI-driven upfront price predictions, and gives administrators a dashboard with demand forecasting to manage orders efficiently.

## Core Features
1. **User Authentication:** Secure login and registration using `Flask-Login` and `bcrypt`.
2. **Booking System:** Dynamic order placements with quantity adjustments.
3. **AI Price Predictor:** Machine learning integration to estimate pricing based on historical data patterns (mocked for wide compatibility on Windows without complex C++ build tools).
4. **Order Tracking:** Users can view step-by-step tracking of their orders.
5. **Admin Dashboard:** Overview of total revenue, orders, registered users, and a 7-day AI demand forecast.
6. **Service Management:** Admins can dynamically add or remove available laundry services.
7. **Payment Simulation:** A mock checkout process completing the user journey.
8. **Responsive UI:** Built with modern CSS (glassmorphism, clean typography, CSS grids/flexbox).

## Technology Stack
*   **Frontend:** HTML5, CSS3, JavaScript (Vanilla ES6+).
*   **Backend:** Python 3, Flask.
*   **Database:** SQLite (via Flask-SQLAlchemy).
*   **Machine Learning Integration:** Custom Python mock predictors demonstrating logic without native dependencies.

---

## Folder Structure

```
WashEase/
│
├── app/                        # Main Application Package
│   ├── __init__.py             # App Factory and Initialization
│   ├── models.py               # SQLAlchemy Database Models
│   ├── routes/                 # Blueprints for different modules
│   │   ├── main.py             # Public routes (Home, etc.)
│   │   ├── auth.py             # Login/Register routes 
│   │   ├── user.py             # User dashboard and booking
│   │   ├── admin.py            # Admin management routes
│   │   └── ml.py               # Machine Learning API endpoints
│   │
│   ├── static/                 # Static Assets
│   │   ├── css/style.css       # Core stylesheet
│   │   └── js/main.js          # Core frontend interactions
│   │
│   └── templates/              # HTML Templates (Jinja2)
│       ├── base.html           # Master layout
│       ├── index.html          # Landing page
│       ├── login.html          
│       ├── register.html      
│       ├── admin/              # Admin interface templates
│       └── user/               # User interface templates
│
├── instance/                   # SQLite database storage (auto-created)
│   └── washease.db             
│
├── ml/                         # Machine learning model artifacts
│   └── model_config.json       # Config showing models are ready
│
├── init_db.py                  # Script to seed the DB with initial data
├── requirements.txt            # Python dependencies
├── run.py                      # Development server runner (module-based)
├── wsgi.py                     # Entry point (standard)
└── README.md                   # Project documentation
```

---

## Step-by-Step Setup Instructions

Follow these steps to run the WashEase platform on your local machine.

### Prerequisites
- Python 3.8 or higher installed.
- Git (optional, for version control).

### 1. Extract/Clone the Project
Navigate to your preferred directory and ensure the `WashEase` folder is present.

### 2. Set Up a Virtual Environment (Recommended)
Open your terminal/command prompt inside the `WashEase` directory:
```bash
# Create the virtual environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies
With the virtual environment active, install the required packages:
```bash
pip install -r requirements.txt
```

### 4. Initialize the Database
Run the provided script to create the SQLite database and seed it with default users and laundry services.
```bash
python init_db.py
```
*This will create an Admin user (`admin@washease.com` / `admin123`) and a standard User (`john@example.com` / `user123`).*

### 5. Run the Application
Start the Flask development server:
```bash
python wsgi.py
# OR
flask --app wsgi run
```

### 6. Access the Platform
Open your web browser and navigate to:
**http://127.0.0.1:5000**

---

## Future Improvements for a Major Project
To expand this MCA level project into a full Major Project, consider adding:
- **Real ML Models:** Re-integrate `scikit-learn` models tracking massive CSV datasets for true predictive parity.
- **Payment Gateway:** Replace the simulated screen Stripe/Razorpay APIs.
- **Live Tracking Map:** Add Google Maps API to track delivery drivers in real-time.
- **Email Notifications:** Integrate `Flask-Mail` to send receipts and status updates to users.
- **Production Database:** Migrate from SQLite to PostgreSQL or MySQL for scalability.
