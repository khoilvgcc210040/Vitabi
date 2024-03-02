#Project name: Vitabi

#Start fast

This guide will help you install and run the project on your machine for development and testing. Make sure you have installed all the necessary requirements before starting.

#Request

List all the requirements needed to install and run your project, for example:

- Python 3.8+
- Django 3.2+
- A Google Cloud account with Google Maps API enabled

#Setting

Description of installation procedure:

Open terminal in project folder
git clone https://github.com/khoilvgcc210040/Vitabi.git
cd yourproject
pip install -r requirements.txt
cp .env.example .env

Open the .env file and fill in the necessary values:
GOOGLE_MAPS_API_KEY=<Your_Google_Maps_API_Key_Here>

Use this command to run the project:
python manage.py runserver

The project will run on http://localhost:8000 (or another port if you have configured it).
