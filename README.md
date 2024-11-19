# Classify
Classify was created in under 24 hours during WesHack 2024, Wesleyan University's annual hackathon. The project showcases the power of collaboration, creativity, and technical innovation under tight time constraints. Designed with the goal of solving a real problem for students, Classify combines user-centric design, cutting-edge technologies, and efficient algorithms to deliver an impactful and intuitive solution.

## Features
**Personalized Recommendations**: Matches courses and professors based on your major, interests, and previous classes.

**Smart Matching Algorithm**: Utilizes a weighted scoring system to prioritize the best matches.

**Autocomplete Search**: User-friendly search interface for selecting majors and previous classes.

**Profile Management**: Create and edit your profile with preferences for clubs, interests, and assignment preferences.

**Dynamic Survey**: Auto-fill interests based on an interactive survey during signup.

**Clean and Modern UI**: Responsive, sleek design for an optimal user experience.

**Data-Driven Insights**: Uses a database of professors and courses for accurate recommendations.

## Tech Stack
**Backend**: Python, Flask, Flask-SQLAlchemy

**Frontend**: HTML, CSS, JavaScript

**Database**: SQLite (development)

**Autocomplete**: Custom-built search and selection functionality

## Setup Instructions

### Installation
Clone the repository:
```bash
git clone https://github.com/lucas-svi/classify.git
cd classify
```

### Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

### Install dependencies:

```bash
pip install -r requirements.txt
```

###Set up the database:

```bash
flask db upgrade
python populate_database.py
```
### Run the application: flask run

Open your browser and visit: http://127.0.0.1:5000

## Development Notes
**Environment Variables**: Use a .env file to store sensitive information like secret keys.

**Database URL**: Update SQLALCHEMY_DATABASE_URI in config.py to point to your preferred database.
