# 🛒 Django E-Commerce Website

A full-featured E-Commerce web application built using Django.  
This project includes authentication, cart management, order tracking, stock management, and secure backend implementation.

---

## 🚀 Features

- 🔐 User Authentication (Login / Register / Logout)
- 🛍️ Add to Cart (Session Based)
- 📦 Order History
- 💳 Payment Integration (Razorpay / Stripe Ready)
- 📊 Stock Management System
- 🔎 Product Search & Filter
- 🛡️ Secure REST API (Django REST Framework)
- 👨‍💼 Admin Dashboard
- 🔒 OWASP Security Best Practices Implemented

---

## 🛠️ Tech Stack

- **Backend:** Django, Django REST Framework
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Database:** SQLite (Development)
- **Authentication:** Session / JWT
- **Version Control:** Git & GitHub

---

## 📂 Project Structure

```
ecommerce-website/
│
├── manage.py
├── requirements.txt
├── ecommerce/
│
├── products/
├── cart/
├── orders/
├── users/
│
└── templates/
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/django-ecommerce.git
cd django-ecommerce
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Migrations

```bash
python manage.py migrate
```

### 5️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

### 6️⃣ Run Server

```bash
python manage.py runserver
```

Open:
```
http://127.0.0.1:8000/
```

---

## 🔐 Security Features

- Password Hashing
- CSRF Protection
- SQL Injection Prevention (ORM)
- Role-Based Access Control
- Secure API Authentication
- Input Validation

---

## 📸 Screenshots

---

## 🌍 Future Improvements

- Production Deployment (Render/AWS)
- Docker Support
- Email Notifications
- Advanced Analytics Dashboard

---

## 👨‍💻 Author

**Krishabh Gupta**  
Backend Developer | Django | Cyber Security Enthusiast  

---

## 📜 License

This project is licensed under the MIT License.
