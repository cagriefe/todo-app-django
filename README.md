# Django To-Do App

## Description

This is a simple to-do application built with Django. It allows users to create, update, and delete tasks. Users can register, log in, and manage their tasks efficiently.

## Features

- User registration and login
- Create, edit, and delete tasks
- View task details
- Task prioritization (Low, Medium, High)
- Display tasks with completion status

## Requirements

- Python 3.12+
- Django 5.1+
- (Optional) Virtual Environment

## Installation

1. **Clone the repository**

    ```bash
    git clone https://github.com/yourusername/todoapp.git
    cd todoapp
    ```

2. **Create and activate a virtual environment (optional but recommended)**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**

    ```bash
    python manage.py migrate
    ```

5. **Create a superuser (for accessing the admin interface)**

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**

    ```bash
    python manage.py runserver
    ```

7. **Access the application**

    Open your web browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to use the app.

## Usage

- **Register a new account**: Click the "Register" button on the homepage.
- **Log in**: Use the login form to access your account.
- **Manage tasks**: After logging in, you can view, add, edit, and delete tasks.

## Customization

- **Custom User Model**: If using a custom user model, ensure that `AUTH_USER_MODEL` is set in `settings.py`.
- **Custom Form**: Modify `forms.py` to adjust user registration form constraints.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Django Documentation
- Various Django packages and libraries used in the project
