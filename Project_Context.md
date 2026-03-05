I am building an e-commerce website using Django and MySQL. The development is being done step-by-step starting from project setup and gradually building the backend structure before implementing business logic.

So far, the following work has been completed.

Project Initialization

A Django project named "pcify" was created. The project uses Python 3.12 inside a Conda environment. MySQL 8.0 Community Edition is used as the database and connected to Django using PyMySQL.

The Django project structure was initialized with the main configuration inside the "pcify" project folder and manage.py at the root.

Database Setup

A MySQL database named "pcify" was created and configured inside Django settings. Django migrations were run successfully to create the initial Django tables such as auth, admin, sessions, and contenttypes.

Custom User Model

Instead of using the default Django User model, a custom user model was implemented inside the "accounts" app.

The custom authentication system includes:

User model using email as the login field
Customer model linked with User
Staff model linked with User
Role model for staff roles

This structure allows the system to differentiate between customers and staff users.

Authentication App

An "accounts" Django app was created to manage authentication logic and user models. The custom user model was registered in Django settings using:

AUTH_USER_MODEL = 'accounts.User'

Migrations were created and applied successfully, generating the following tables:

accounts_user
accounts_customer
accounts_staff
accounts_role

Template Organization

HTML templates for the project already existed and were reorganized into a cleaner structure.

The templates directory now contains:

templates/accounts/
login.html
signup.html

templates/dashboard/
admin_login.html
analytics.html
brands.html
categories.html
compatibility.html
customers.html
employee_management.html
employees.html
home.html
inventory.html
orders.html
prebuilt_pc.html
products.html
settings.html
suppliers.html
trending.html

templates/home/
home.html

This structure separates customer authentication pages, dashboard pages, and public pages.

Dashboard System

A Django app named "dashboard" was created to handle the custom admin dashboard interface. The dashboard templates include multiple pages for managing different parts of the e-commerce system such as products, suppliers, inventory, employees, and analytics.

The dashboard login page is implemented using:

templates/dashboard/admin_login.html

After login, users are redirected to the dashboard home page:

templates/dashboard/home.html

Public Site App

A Django app named "main" was created to handle public-facing pages such as the homepage.

Static Files

Static files are stored inside the static directory. Currently a JavaScript file exists for login functionality:

static/js/login.js

Project Structure

The project now has the following main structure:

accounts – authentication system
dashboard – admin dashboard interface
main – public pages
templates – HTML templates
static – static assets
_resources – SQL schema reference

Database Schema Reference

The project includes an SQL schema file named pcify.sql located inside the _Resources folder. This schema will later be used to implement Django models for the e-commerce system such as products, categories, inventory, suppliers, and orders.

Current Development Stage

The foundational setup of the Django project is complete. Authentication infrastructure, template organization, and application structure have been established.

The next development step will involve implementing the core business models for the e-commerce system based on the provided SQL schema.
