# BE WYSE Assignment

# Django Custom Token-Based Authentication

This is a Django project that demonstrates custom token-based authentication for user registration, login, and accessing protected views. It also includes custom middleware to secure protected views.

## Features

- User registration with optional fields (username, first name, last name).
- User registration with required fields (email, password).
- User login with custom token generation.
- Custom middleware to protect views with custom tokens using firebase authentication.
- User profile view and editing.
- MongoDB database used for user data storage.

## Prerequisites

Before you start using this project, make sure you have the following set up:

- Python installed on your system.
- Django and Django REST framework installed.
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup) for token verification.
- MongoDB server running locally or accessible via the specified connection URL.

## Getting Started

1. Clone this repository:

   ```bash
   git clone https://github.com/your/repo.git
   cd django-custom-token-auth

2. Install the required packages:

3. Configure Firebase Admin SDK:

    Set up a Firebase project on the Firebase Console.  
    Download the service account key file.
    Update the Firebase Admin SDK initialization in settings.py with your service account key file.
  
4. Run the Django development server:
    python manage.py runserver
   

## Usage
### Register

To register a new user, make a POST request to the /register/ endpoint with the following data in the request body:

- username: (optional) Username for the new user. If not provided, a unique username will be generated.
- email: Email address of the new user.
- password: Password for the new user.
- first_name: (optional) First name of the new user.
- last_name: (optional) Last name of the new user.

### Login

To log in as a user, make a POST request to the /login/ endpoint with the following data in the request body:

- username: Username of the user.
- password: Password of the user.

Upon successful login, you will receive a custom token that you can use for further authentication(By generating id_token which will be used for viewing other views).

#### Protected Views
This project includes a sample protected view (protected_view) as an example. These views are accessible only with a valid custom token.

##### Edit Profile
To edit the user's profile, make a POST request to the /edit_profile/ endpoint with a valid custom token in the Authorization header. You can update the first_name, last_name, and username fields.

##### View Profile
To view the user's profile, make a GET request to the /view_profile/ endpoint with a valid custom token in the Authorization header. This endpoint displays the user's profile information.

