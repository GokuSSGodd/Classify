from app import db, create_app
from app.models import Course, Professor, CourseProfessor
import json

app = create_app() 

with open("courses.json", "r") as file:
    courses = json.load(file)

with app.app_context(): 
    for course_data in courses:
        professor_name = course_data.pop("professor", None)
        existing_course = Course.query.filter_by(
            course_code=course_data["course_code"],
            section=course_data["section"],
            semester=course_data["semester"]
        ).first()

        if not existing_course:
            new_course = Course(**course_data)
            db.session.add(new_course)
            db.session.commit()
            if professor_name:
                professor = Professor.query.filter_by(name=professor_name).first()
                if not professor:
                    professor = Professor(name=professor_name)
                    db.session.add(professor)
                    db.session.commit()
                course_professor = CourseProfessor(
                    course_id=new_course.id,
                    professor_id=professor.id,
                    semester=new_course.semester
                )
                db.session.add(course_professor)
                db.session.commit()

    print("Courses and professors uploaded successfully.")
