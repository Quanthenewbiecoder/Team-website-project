# The Divine Jewelry - E-commerce Website

The Divine Jewelry is a full-featured e-commerce platform for a jewelry store, built with Python Flask and MongoDB. This responsive web application provides a seamless shopping experience with features like product browsing, user authentication, shopping cart, order management, and admin dashboard.

## Live Demo

The application is hosted at: [http://cs2team20.cs2410-web01pvm.aston.ac.uk/](http://cs2team20.cs2410-web01pvm.aston.ac.uk/)

## Features

- **User Authentication**: Register, login, and profile management
- **Product Management**: Browse products by category, collection, and search
- **Shopping Cart**: Add items to cart, adjust quantities, and checkout
- **Order Tracking**: Real-time order status tracking for both guests and registered users
- **Admin Dashboard**: Comprehensive product, user, and order management
- **Responsive Design**: Seamless experience across desktop and mobile devices
- **Email Notifications**: Order confirmations and transactional emails
- **Wishlist**: Save favorite items for later

## Collections

The jewelry is organized into distinctive collections:
- **Crystal Collection**: Brilliant pieces featuring crystal designs
- **Leaf Collection**: Nature-inspired jewelry with elegant leaf motifs
- **Pearl Collection**: Timeless elegance with lustrous pearls

## Tech Stack

- **Backend**: Python Flask
- **Database**: MongoDB Atlas
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Flask-Login
- **Email**: Flask-Mail
- **Form Processing**: Flask-WTF
- **Deployment**: Linux server

## Setup & Installation

To run this project on the server, follow these steps:

1. SSH into the server:
   ```
   ssh cs2team20@cs2410-web01pvm.aston.ac.uk
   ```
   Password: `NMfpRb6mThfW+q3e`

2. Navigate to the project directory:
   ```
   cd Team-website-project
   ```

3. Create a virtual environment:
   ```
   python3 -m venv venv
   ```

4. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```

5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

6. Run the application:
   ```
   python run.py
   ```

7. The website will be available at: [http://cs2team20.cs2410-web01pvm.aston.ac.uk/](http://cs2team20.cs2410-web01pvm.aston.ac.uk/)

## Project Structure

- `app/`: Core application directory
  - `static/`: Static files (CSS, JS, images)
  - `templates/`: HTML templates
  - `models.py`: Database models
  - `routes.py`: Request handlers and routes
  - `forms.py`: Form definitions
  - `database.py`: Database connection setup
- `config.py`: Application configuration
- `run.py`: Application entry point

## Admin Access

To access the admin dashboard:
1. Log in using admin credentials (Email: Admin123@Admin.com Password: Admin123)
2. Navigate to `/admin` or use the Admin Dashboard link in the navigation

## Local Development

For local development:

1. Clone the repository
2. Create a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Set up MongoDB connection in `config.py`
5. Run with: `python run.py`

## License

This project is developed by Team 20.

## Credits

- Team 20 Members