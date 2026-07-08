# Glow Salon Management System

A desktop Salon Management System built with **Python (Tkinter)** for the interface and **Microsoft SQL Server** for the database. The system currently implements a secure, role-based login module, with salon management features planned as the project grows.

## Features

- 🎨 Custom-designed Tkinter login screen with a salon-themed UI
- 🔐 Secure authentication using **bcrypt** password hashing (passwords are never stored or compared in plain text)
- 🗄️ Live connection to a SQL Server database (Windows Authentication)
- 👥 Role-based access — **Admin** and **Receptionist** users are routed to different dashboards after login
- 🧱 Clean project structure separating UI, database connection, and authentication logic

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Python, Tkinter |
| Database | Microsoft SQL Server |
| DB Connector | pyodbc (ODBC Driver 18 for SQL Server) |
| Password Security | bcrypt |

## Project Structure

```
salon-management-system/
│
├── login.py               # Tkinter login screen (UI) + role-based navigation
├── db_connection.py       # Handles the SQL Server database connection
├── auth.py                # Verifies login credentials using bcrypt
├── create_test_users.py   # One-time script to seed test Admin/Receptionist users
└── README.md
```

## Database Setup

The system expects a SQL Server database named `Salon_managment_system` with a `Users` table:

```sql
CREATE TABLE Users (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,   -- stores bcrypt hash, not plain text
    Role VARCHAR(20) NOT NULL CHECK (Role IN ('Admin', 'Receptionist'))
);
```

## Getting Started

### Prerequisites
- Python 3.10+
- Microsoft SQL Server (local instance is fine)
- ODBC Driver 17 or 18 for SQL Server

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/<your-username>/salon-management-system.git
   cd salon-management-system
   ```

2. Install the required Python packages:
   ```
   pip install pyodbc bcrypt
   ```

3. Create the `Users` table in your SQL Server database (see the SQL above).

4. Update the connection details in `db_connection.py` if your server or database name is different from the default.

5. (Optional) Seed test users:
   ```
   python create_test_users.py
   ```

6. Run the application:
   ```
   python login.py
   ```

## How Login Works

1. The user enters their username and password in the Tkinter login screen.
2. `auth.py` fetches the matching user's hashed password and role from the `Users` table.
3. `bcrypt.checkpw()` verifies the entered password against the stored hash.
4. If valid, the user is routed to their role-specific dashboard (Admin or Receptionist). If invalid, an error message is shown.

## Roadmap

- [ ] Build out full Admin Dashboard (staff, services, reports management)
- [ ] Build out full Receptionist Dashboard (appointments, customer check-in)
- [ ] Add customer and appointment management modules
- [ ] Add input validation and improved error handling

## Author

Built as part of an ongoing internship/learning project — Salon Management System (Python + SQL Server).
