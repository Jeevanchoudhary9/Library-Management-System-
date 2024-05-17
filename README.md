# Library Management System

## Project Overview

Welcome to the Library Management System, an innovative platform designed to offer users an efficient and secure way to manage and access eBooks. This application focuses on providing a seamless experience for users to view, request, and manage eBook access, while ensuring data security and user privacy. Administrators have comprehensive control over book management, user requests, and notifications.

## Project Goals

The Library Management System aims to achieve the following objectives:

- **Secure Login and Registration:** Implement a secure user authentication system.
- **User Profiles:** Allow users to view and manage their book requests and access history.
- **eBook Management:** Enable users to request access to eBooks for a limited period and manage their requests.
- **Admin Dashboard:** Provide administrators with tools to upload eBooks, manage user requests, and maintain the library.
- **Notifications:** Notify users about the status of their book requests via email.
- **Usage Analytics:** Provide users and admins with insights into book usage and user interests.
- **Responsive Design:** Ensure the platform is accessible across various devices and screen sizes.

## Technology Stack

The Library Management System utilizes the following technologies and tools:

- **Flask:** A robust Python web framework for scalable web applications.
- **VueJs:** A progressive JavaScript framework for building interactive user interfaces.
- **SQLite:** A lightweight and efficient relational database system.
- **HTML:** The standard markup language for structuring web content.
- **Bootstrap:** A powerful CSS framework for designing responsive web pages.
- **Jinja:** A templating engine for Python, integrated with Flask.
- **JavaScript:** A versatile scripting language for adding interactivity and dynamic features.
- **Celery:** An asynchronous task queue for managing background tasks.
- **Redis:** A fast, in-memory data structure store used as a message broker by Celery.
- **Werkzeug:** A comprehensive WSGI web application library used for security and session management.
- **Email Integration:** For sending notifications and updates to users.

## Features

### User Features

- **Secure Registration and Login:** Users can securely register and log in to their accounts.
- **View Books:** Users can browse available eBooks, view details, and request access.
- **Request eBook Access:** Users can request access to up to 5 eBooks at a time for a maximum of one month.
- **Manage Requests:** Users can edit or cancel their requests, and view request history with labels such as returned, revoked, time elapsed, or rejected.
- **Read eBooks:** Users can view eBooks in PDF format and see summaries of their most interested sections.
- **Notifications:** Users receive email notifications for request approval or rejection.
- **Search:** Users can search for books using various criteria.

### Admin Features

- **Dashboard:** Admins have access to a comprehensive dashboard to manage the library.
- **Book Management:** Admins can upload eBook files (PDF), add book images, descriptions, and categorize books.
- **Request Management:** Admins can view, accept, or reject eBook access requests from users.
- **Section Management:** Admins can add and manage book sections.
- **Usage Analytics:** Admins can view summaries of book usage and user interests.

## How to Run the Web App Locally

To run the Library Management System locally on your machine, follow these steps:

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/Jeevanchoudhary9/Library-Management-System-.git
    ```

2. **Go to Api Folder:**
    Go to api using
   ```bash
   cd Library-Management-System-/api
   ```

4. **Run Celery beats and worker:**
    ```bash
    ./celery_beats.sh
    ./celery_worker.sh
    ./run_api.sh
    ```
    if permission denied then do following:
   ```bash
   chmod +x celery_beats.sh
   chmod +x celery_worker.sh
   chmod +x run_api.sh
   ```

6. **Create Database:**
    ```bash
    python3 upload_initial_data.py
    ```

7. **Activate the Virtual Environment:**
    ```bash
    source .venv/bin/activate
    ```

8. **Install Dependencies:**
    Do if required 
    ```bash
    pip install -r requirements.txt
    ```

9. **Run Python App:**
    ```bash
    python3 main.py
    ```

10. **Go To App now:**
    All the above should be carried out in api assuming you are in now api then do following:
    ```bash
    cd ..
    cd app
    ```

11. **Install Node Modules:**
    ```bash
    npm install
    ```
    
12. **Start Vue Server:**
    ```bash
    sudo vue ui
    ```
    then go to web at address given or at localhost:8000 then go to vue manager then to import and then select app folder which is shown as vue then go to Tasks -> serve -> Run task then go to shown website or go to localhost:8080
    
14. **Access the Application:**
    Open your web browser and go to http://localhost:8080 or the URL shown in the terminal.

## Project Structure

```bash
Library-Management-System-/
    ├── api/
    │   ├── instance/
    │   │   └── db.sqlite3
    │   ├── static/
    │   │   └── logo.jpeg
    │   ├── image_directory/
    │   │   └── images.jpg
    │   ├── pdfuploads/
    │   │   └── book.pdf
    │   ├── templates/
    │   │   ├── mail_login.html
    │   │   ├── mail_remainder.html
    │   │   ├── user_report.html
    │   │   └── mail_status.html
    │   ├── celery_beats.sh
    │   ├── celerybeat-schedule
    │   ├── celerywork.py
    │   ├── celery_worker.sh
    │   ├── config.py
    │   ├── main.py
    │   ├── models.py
    │   ├── requirements.txt
    │   ├── run_api.sh
    │   ├── upload_initial_data.py
    │   └── resources.py
    └── app/
        └── Vue js app
```

## Screenshots

### User Interface

![Login](https://github.com/Jeevanchoudhary9/Library-Management-System-/blob/d8570cd6db621ada55c35c7155c98a4f7a3a889f/screenshots/login%20.png)
*Caption: Login Screen*

![User Register](https://github.com/Jeevanchoudhary9/Library-Management-System-/blob/d8570cd6db621ada55c35c7155c98a4f7a3a889f/screenshots/register.png)
*Caption: Registration Screen*

![User Dashboard](https://github.com/Jeevanchoudhary9/Library-Management-System-/blob/d8570cd6db621ada55c35c7155c98a4f7a3a889f/screenshots/user%20dashboard.png)
*Caption: Dashboard*

![Book View](https://github.com/Jeevanchoudhary9/Library-Management-System-/blob/d8570cd6db621ada55c35c7155c98a4f7a3a889f/screenshots/book%20view.png)
*Caption: Book View*

![Request Book](https://github.com/Jeevanchoudhary9/Library-Management-System-/blob/d8570cd6db621ada55c35c7155c98a4f7a3a889f/screenshots/book%20view%20card.png)
*Caption: Request Book View*

![Requested Books List](https://github.com/Jeevanchoudhary9/Library-Management-System-/blob/d8570cd6db621ada55c35c7155c98a4f7a3a889f/screenshots/user%20requested%20books.png)
*Caption: Requested Books List*

![User My Book View](https://github.com/Jeevanchoudhary9/Library-Management-System-/blob/d8570cd6db621ada55c35c7155c98a4f7a3a889f/screenshots/user%20my%20books.png)
*Caption: My Books View*

![User History](https://github.com/Jeevanchoudhary9/Library-Management-System-/blob/d8570cd6db621ada55c35c7155c98a4f7a3a889f/screenshots/user%20history.png)
*Caption: History*

![User Summary](https://github.com/Jeevanchoudhary9/Library-Management-System-/blob/d8570cd6db621ada55c35c7155c98a4f7a3a889f/screenshots/user%20summary.png)
*Caption: Summary*

![Email to User](https://github.com/Jeevanchoudhary9/Library-Management-System-/blob/d8570cd6db621ada55c35c7155c98a4f7a3a889f/screenshots/email.png)
*Caption: Notification to User using Email*

### Admin Interface

![Admin Dashboard](https://github.com/Jeevanchoudhary9/Library-Management-System-/blob/d8570cd6db621ada55c35c7155c98a4f7a3a889f/screenshots/admin%20dashboard.png)
*Caption: Admin Dashboard*

![Requested Books](https://github.com/Jeevanchoudhary9/Library-Management-System-/blob/d8570cd6db621ada55c35c7155c98a4f7a3a889f/screenshots/admin%20requested%20book.png)
*Caption: Requested Books by User*

![Admin Summary](https://github.com/Jeevanchoudhary9/Library-Management-System-/blob/d8570cd6db621ada55c35c7155c98a4f7a3a889f/screenshots/admin%20summary.png)
*Caption: Summary*

## Conclusion

With its secure authentication, efficient eBook management, and robust notification system, the Library Management System offers a streamlined and user-friendly experience for both users and administrators. The platform's comprehensive features ensure easy access to eBooks and effective management of user requests, making it an ideal solution for modern digital libraries.

## Document Author

Jeevan Choudhary
