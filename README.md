End user Documentation

# NGO CMS Website

A comprehensive Content Management System (CMS) designed specifically for NGOs to manage their digital presence, donations, volunteers, and content.

## Features

- User Authentication and Authorization
- Content Management
- Donation Management
- Volunteer Management
- Event Management
- Multi-language Support
- SEO Optimization
- Responsive Design
- Blog Management
- Media Gallery

## Tech Stack

- Backend: Django
- Frontend: HTML, CSS, JavaScript, Bootstrap
- Database: SQLite (Development) / PostgreSQL (Production)
- Payment Gateways: Stripe, Razorpay

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

- `ngo_cms/` - Main project directory
  - `core/` - Core application
  - `accounts/` - User authentication
  - `donations/` - Donation management
  - `volunteers/` - Volunteer management
  - `events/` - Event management
  - `blog/` - Blog management
  - `media/` - Media files
  - `static/` - Static files

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License. 

