# Jarnam Symphony Restaurant Website

Welcome to the official repository for **Jarnam Symphony**, a full-featured restaurant website designed to enhance user engagement and streamline business operations. This project was developed using the **Django** framework, with deployment on an **AWS EC2 instance** powered by **Apache HTTP Server**.

Link to the website: [http://13.59.247.27/restaurant/home](http://13.59.247.27/restaurant/home)

## Features

- **Responsive Web Design**: Enjoy a friendly interface created with HTML, CSS, JavaScript, and Bootstrap for optimal user experience on any device.
- **Dynamic User Interactions**:
  - **Reservations**: Book tables directly from the website, with real-time availability status updates.
  - **Food Comments**: Leave reviews on dishes, enabled with AJAX for smooth, dynamic updates without page reloads.
  - **Interactive Map**: Locate Jarnam Symphony easily with an embedded **Bing Maps** feature.
- **Database**: User and reservation data are stored in a **MySQL database** to ensure data persistence and organization.
- **Email Notifications**: Get reservation and order confirmations instantly via **SendGrid API** email notifications.
- **Business Logic and Data Consistency**: Features atomic transactions to maintain data integrity across all processes.

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Python Django
- **Database**: MySQL
- **Deployment**: AWS EC2 (Apache HTTP Server)
- **APIs & Integrations**:
  - **Bing Maps** for interactive location services
  - **SendGrid API** for automated email notifications

## Deployment

- **Server**: Apache HTTP Server on an AWS EC2 instance
- **Domain**: Access the website here: [http://13.59.247.27/restaurant/home](http://13.59.247.27/restaurant/home)

## Functionality Overview

The **Jarnam Symphony** website offers an engaging and seamless experience for users and administrators through the following modules:

### 1. Home Page Module
- **Welcome Message**: Displays a greeting or introductory message to welcome visitors.
- **Restaurant Vision**: Highlights the restaurant’s mission and vision, creating a connection with guests.
- **Restaurant Photo**: Features a high-quality image to establish a welcoming atmosphere.

### 2. About Page Module
- **Restaurant Photo**: Showcases an additional image of the restaurant, different from the home page.
- **Restaurant Information**: Introduces the restaurant’s background, history, and cuisine style.
- **Location Map**: Includes an interactive map with the restaurant’s address on Carnegie Street, and the contact number for inquiries.
- **Operational Details**: Provides information about the restaurant's open hours, location, and contact details, integrated with Google Maps.

### 3. User Account Module
- **Login Page**: Allows users to log in with their credentials securely.
- **Registration Page**: Provides a form for new users to create an account.
- **Customer Profile Page**: Displays the user’s information, profile picture (default or uploaded), and reservation details. Users can modify or delete their reservations and update personal information.

### 4. Reservation Module
- **Reservation Page**: Shows available tables, allows filtering by time, and enables users to reserve tables by selecting an available option.

### 5. Menu Module
- **Menu Display**: Lists all dishes, including names, prices, and descriptions for easy browsing.
- **Dish Description**: Features each dish name prominently, accompanied by a brief, enticing description.
- **Average Rating Display**: Calculates and displays the average rating dynamically from reviews, with a visual star rating updated in real-time.
- **Review Submission Form**: Allows users to submit reviews with a text field and star-based rating system (1-5 stars).
- **User Reviews Section**: Lists reviews with reviewer names, comments, star ratings, and timestamps for when reviews were posted.

### 6. Administration Module
- **Admin Page**: Displays all reservations and offers the administrator tools to update the menu.
