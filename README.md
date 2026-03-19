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
<img width="1886" height="1079" alt="image" src="https://github.com/user-attachments/assets/77850f0f-7073-42a5-87a3-8e42abba0075" />
<img width="1916" height="1079" alt="image" src="https://github.com/user-attachments/assets/b6da619c-62e3-4c6a-a252-b27985dde9e9" />
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/00bf7ce8-3924-458d-bc13-84b271d7e94b" />
<img width="1919" height="941" alt="image" src="https://github.com/user-attachments/assets/ad88e98e-14a8-4320-8215-3bf6936be7e4" />
<img width="1918" height="1079" alt="image" src="https://github.com/user-attachments/assets/eae79b4f-682e-4304-b6e1-e46561ce60bb" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/14ee02bf-ce1a-49b7-8eae-ac90f4948450" />
<img width="1917" height="1079" alt="image" src="https://github.com/user-attachments/assets/9ac351f1-8865-4872-ac82-d60335e9617f" />
<img width="1917" height="1073" alt="image" src="https://github.com/user-attachments/assets/27fa8c76-6618-4023-bdd1-5df6359718a9" />
<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/fb74030c-55c2-4957-a2be-3d9cbdddcf01" />



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
