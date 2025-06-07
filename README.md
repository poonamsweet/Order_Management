

# 🛒 Order Management System

A web-based backend system for managing orders, employees, clients, and attendance using Flask, SQLAlchemy, and MySQL.

---

## 📦 Features

* User and employee management
* Client registration and tracking
* Order assignment and status tracking
* Attendance logging for employees
* JWT-based authentication
* Email configuration for notifications
* CORS enabled for secure cross-origin access
* MySQL database integration

---

## 🧰 Tech Stack

* **Backend**: Python, Flask, SQLAlchemy
* **Authentication**: JWT (JSON Web Tokens)
* **Database**: MySQL
* **Email**: Gmail SMTP
* **Others**: CORS, boto3 (for AWS), dotenv (recommended for env vars)

---

## 🏗️ Project Structure

```
📁 order_management/
│
├── app.py                  # Main Flask app
├
├── send_mail.py            # Utility for sending emails
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
```

---

## 🔑 Environment Configuration

Set up your environment variables (use `.env` or configure directly in `app.py`):

```bash
# .env
RDS_USERNAME=root
RDS_PASSWORD=password
RDS_HOSTNAME=localhost
RDS_DB_NAME=ordermodule
JWT_SECRET_KEY=your_jwt_secret_key
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_email_password
```

Update `app.config[]` in `app.py` accordingly or use `python-dotenv` to load `.env`.

---

## 🔌 Database Configuration

Make sure you have MySQL running and create the `ordermodule` database:

```sql
CREATE DATABASE ordermodule;
```

SQLAlchemy URI (already configured in `app.py`):

```python
'mysql+pymysql://root:password@localhost:3306/ordermodule'
```

---

## 🧪 Installation & Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/poonamsweet/Order_Management.git
   cd order-management
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask App**

   ```bash
   python app.py
   ```

---

## 🧱 Models Overview

### 🔹 `Users`

Stores user credentials and types (admin, staff, etc.).

### 🔹 `Employees`

Links to `Users`, stores employee profile and role.

### 🔹 `EmployeesForm`

Holds extended information about employees (Aadhaar, PAN, emergency contacts, etc.).

### 🔹 `Client`

Client-specific data including contact info and credentials.

### 🔹 `Orders`

Tracks order metadata such as client, expert, deadlines, .

### 🔹 `Attendance`

Stores check-in/out times and daily work stats for employees.

---

## 🔐 Authentication

JWT-based authentication with:

* `create_access_token()`
* `@jwt_required()` decorator

Example:

```python
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
```

---

## 🌐 CORS Support

Configured to allow requests from:

```python
[
 'http://13.202.119.149:3000',
 'http://localhost:3000',
 'https://ordermanagementapp.in',
 'https://api.ordermanagementapp.in',
 'https://www.ordermanagementapp.in'
]
```

Update the list as needed for development or production.

---

## 📧 Email Configuration

Using Gmail SMTP:

```python
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = your_email
MAIL_PASSWORD = your_password
```

Use app password if 2FA is enabled.

---

## 📂 File Uploads

AWS S3 is supported using `boto3`. Ensure you configure:

* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`
* `S3_BUCKET_NAME`



---




