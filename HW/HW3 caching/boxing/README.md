# 🥊 CS411 Final Project – Boxing Web API

## 📌 Project Overview

This is a Flask-based web API that simulates a boxing gym management system. Users can:

- Create accounts, log in/out, and manage passwords  
- Add boxers and simulate matches between them  
- Track win/loss records and view a leaderboard  
- Use an in-memory ring structure to manage fights  
- Fetch data from an external API (random dog images) for fun

The app uses:
- Flask + SQLAlchemy  
- SQLite for user accounts  
- In-memory Python objects for boxing ring and boxers  
- Docker for containerization  
- External RESTful API: [Dog CEO API](https://dog.ceo)

---

## ⚙️ API Endpoints

### 🧪 Health Check

**GET** `/api/health`  
**Returns:**

```json
{
  "status": "success",
  "message": "Service is running"
}
```

---

## 👤 Account Management

### 🆕 Create Account

**PUT** `/api/create-user`  
**Request Body:**

```json
{
  "username": "david",
  "password": "1234"
}
```

---

### 🔐 Login

**POST** `/api/login`  
**Request Body:**

```json
{
  "username": "david",
  "password": "1234"
}
```

---

### 🚪 Logout

**POST** `/api/logout`

---

### 🔑 Change Password

**POST** `/api/change-password`  
**Request Body:**

```json
{
  "new_password": "newpass123"
}
```

---

## 🥊 Boxer Routes

### ➕ Add Boxer

**POST** `/api/add-boxer`  
**Request Body:**

```json
{
  "name": "Tyson",
  "weight": 220,
  "height": 72,
  "reach": 78,
  "age": 32
}
```

---

### ❌ Delete Boxer

**DELETE** `/api/delete-boxer/<boxer_id>`

---

### 🔍 Get Boxer by ID

**GET** `/api/get-boxer-by-id/<boxer_id>`

---

### 🔍 Get Boxer by Name

**GET** `/api/get-boxer-by-name/<boxer_name>`

---

### 🥇 Leaderboard

**GET** `/api/leaderboard?sort=wins`  
**GET** `/api/leaderboard?sort=win_pct`

---

## 🥊 In-Memory Ring Routes

### 🚪 Enter Ring

**POST** `/api/enter-ring`  
**Request Body:**

```json
{
  "name": "Tyson"
}
```

---

### 🧼 Clear Ring

**POST** `/api/clear-boxers`

---

### 📊 Get Boxers in Ring

**GET** `/api/get-boxers`

---

### 🆚 Fight

**GET** `/api/fight`

---

### 🔢 Get Ring Count

**GET** `/api/get-ring-count`  
**Returns:**

```json
{
  "status": "success",
  "count": 2
}
```

---

## 🐶 External API Integration

### 📸 Get Random Dog Image

**GET** `/api/dog-image`  
**Returns:**

```json
{
  "status": "success",
  "image_url": "https://images.dog.ceo/breeds/hound-afghan/n02088094_1003.jpg"
}
```

---

## 🧪 Testing

- `pytest` is used for unit tests in `/tests/`
- `smoketest.py` tests create-user, login, add-boxer, and logout
- Logging is implemented throughout the application

---

## 🐳 Docker Instructions

### 🔨 Build the image:

```bash
docker build -t cs411-final .
```

### 🚀 Run the container:

```bash
docker run -p 5010:5000 cs411-final
```

Then visit:  
- `http://localhost:5010/api/health`  
- `http://localhost:5010/api/dog-image`

---

## 🔐 Environment Variables

Use a `.env` file in your root directory with:

```
SECRET_KEY=dev-secret
DATABASE_URL=sqlite:///db/app.db
```

---
