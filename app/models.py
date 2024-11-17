from . import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    class_year = db.Column(db.String(10))
    major = db.Column(db.String(100))
    interests = db.Column(db.Text)
    clubs = db.Column(db.Text)
    previous_classes = db.Column(db.Text, nullable=True)
    saved_matches = db.Column(db.Text)
    assignment_preferences = db.Column(db.String(200), nullable=True)
    class_time_preferences = db.Column(db.String(200), nullable=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), nullable=False, index=True)
    course_name = db.Column(db.String(200), nullable=False)
    credits = db.Column(db.Float, nullable=True)
    description = db.Column(db.Text, nullable=False)
    examinations_assignments = db.Column(db.Text, nullable=True)
    prerequisites = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            "course_name": self.course_name,
            "course_code": self.course_code,
            "description": self.description,
            "examinations_assignments": self.examinations_assignments,
            "credits": self.credits,
            "prerequisites": self.prerequisites,
        }

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    average_rating = db.Column(db.Float, nullable=True)
    total_reviews = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            "name": self.name,
            "average_rating": self.average_rating,
            "total_reviews": self.total_reviews
        }

class CourseProfessor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    specific_class_rating = db.Column(db.Float, nullable=True)

    course = db.relationship('Course', backref='course_professors')
    professor = db.relationship('Professor', backref='professor_courses')

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "professor_id": self.professor_id,
            "semester": self.semester,
            "specific_class_rating": self.specific_class_rating,
            "course": self.course.to_dict() if self.course else None,
            "professor": self.professor.to_dict() if self.professor else None,
        }

from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    profile_data = db.Column(db.JSON, nullable=True)
