# invoice-fastapi-app

# Invoice FastAPI App

A simple, modular invoice and billing backend built using **FastAPI**, **SQLAlchemy**, and **MySQL**. This app supports JWT-based user authentication, invoice creation, previewing, and direct printing.

---

## 🚀 Features

- 🔐 JWT authentication with `/login`
- 👤 User creation and listing
- 🧾 Invoice creation with smart parsing of quantities and prices
- 🖨️ Invoice preview and direct print support (Linux/macOS)
- 📦 Clean modular structure using FastAPI routers

---

## 🛠️ Tech Stack

- **FastAPI** – High-performance Python web framework
- **SQLAlchemy** – ORM for DB interaction
- **MySQL** – Relational database
- **JWT** – Secure authentication
- **Uvicorn** – ASGI server

---

## 📂 Project Structure

│
├── app/
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
│ ├── auth.py
│ ├── oauth2.py
│ ├── util.py
│ └── routers/
│ ├── user.py
│ └── invoice.py
|  ├── main.py
│
├── requirements.txt
└── README.md




📄 License
This project is licensed under the MIT License — feel free to use and modify.

✨ Author
Macha Sathya
GitHub Profile →
