# Loan Management System

This is a Loan Management System built with Django and React. The system manages loans, fund pools, and transactions between customers, loan providers, and bank personnel.

## Features
- User authentication with JWT.
- Role-based access control (Customer, Loan Provider, Bank Personnel).
- Loan management and tracking.
- Real-time transaction processing.

## Installation

Follow these steps to set up the project locally:

### Backend (Django)
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

### Frontend (React)
cd frontend
npm install
npm start
