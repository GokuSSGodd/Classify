from flask import Blueprint, redirect, render_template, request, url_for, session
from .models import Student, Professor, CourseProfessor, Course
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def main_page():
    return render_template('index.html')

@main.route('/profile', methods=['GET'])
def student_profile():
    student_id = session.get('student_id')
    if not student_id:
        print("No student ID in session. Redirecting to login.")
        return redirect('/login')

    student = Student.query.get(student_id)
    print("Loaded student major: ", student.major)
    if not student:
        print(f"Student with ID {student_id} not found in database. Redirecting to login.")
        return redirect('/login')
    return render_template('profile.html', student=student)

major_abbreviations = {
    "Alternative Language Study Options": "LANG",
    "American Sign Language and Deaf Studies": "ASLD",
    "Arabic": "ARAB",
    "Art History": "ARHA",
    "Art Studio": "ARST",
    "Chinese": "CHIN",
    "Classical Studies": "CLST",
    "College of Film and the Moving Image": "FILM",
    "College of Letters": "COL",
    "Dance": "DANC",
    "English": "ENGL",
    "French": "FREN",
    "German Studies": "GRST",
    "Greek": "GRK",
    "Hebrew": "HEBR",
    "Hindi-Urdu": "HIUR",
    "Italian": "ITAL",
    "Japanese": "JAPN",
    "Korean": "KREA",
    "Latin": "LAT",
    "Music": "MUSC",
    "Portuguese": "PORT",
    "Romance Lang & Lit In Eng": "RL&L",
    "Russian": "REES",
    "Russian Literature in English": "RULE",
    "Spanish": "SPAN",
    "Theater": "THEA",
    "World Literature in Translation": "WLIT",
    "African American Studies": "AFAM",
    "American Studies": "AMST",
    "Anthropology": "ANTH",
    "College of Social Studies": "CSS",
    "Economics": "ECON",
    "Global South Asian Studies": "GSAS",
    "Government": "GOVT",
    "History": "HIST",
    "Philosophy": "PHIL",
    "Religion": "CJST",
    "Russian, East European, and Eurasian Studies": "REES",
    "Sociology": "SOC",
    "Astronomy": "ASTR",
    "Biology": "BIOL",
    "Chemistry": "CHEM",
    "College of Integrative Sciences": "ASTR",
    "Computer Science": "COMP",
    "Earth and Environmental Sciences": "E&ES",
    "Mathematics": "MATH",
    "Molecular Biology and Biochemistry": "MB&B",
    "Neuroscience and Behavior Program": "NS&B",
    "Physics": "PHYS",
    "Psychology": "PSYC",
    "Asian American Studies": "AMST",
    "Christianity Studies": "ARHA",
    "Community-Engaged Learning": "AFAM",
    "Disability Studies": "AMST",
    "Health Studies": "AMST",
    "Queer Studies": "AFAM",
    "Sustainability and Environmental Justice": "ARCP",
    "Archaeology Program": "ARCP",
    "Center for Global Studies": "CGST",
    "Center for Jewish Studies": "CJST",
    "Center for the Humanities": "CHUM",
    "Center for the Study of Public Life": "CSPL",
    "College of Design and Engineering Studies": "IDEA",
    "College of East Asian Studies": "CEAS",
    "College of Education Studies": "EDST",
    "College of Science and Technology Studies": "STS",
    "College of the Environment": "COE",
    "Digital Design Commons": "DDC",
    "Feminist, Gender, and Sexuality Studies Program": "FGSS",
    "Latin American Studies Program": "LAST",
    "Medieval Studies Program": "MDST",
    "Quantitative Analysis Center": "QAC",
    "Writing Center": "ANTH",
    "Calderwood Seminars in Public Writing": "MUSC",
    "Courses Related to Design": "ARST",
    "Graduate Planetary Science Concentration": "BIOL",
    "Physical Education": "PHED"
}


@main.route('/matches/<int:student_id>')
def matches(student_id):
    student = Student.query.get_or_404(student_id)
    all_courses = CourseProfessor.query.join(Professor).all()
    major_abbreviation = major_abbreviations.get(student.major)
    unique_matches = {}
    
    for course_prof in all_courses:
        course = course_prof.course
        professor = course_prof.professor
        course_name = course.course_name
        
        major_match = 1 if major_abbreviation and major_abbreviation in course.course_code else 0
        interest_match = any(
            interest.lower() in course.description.lower() or 
            interest.lower() in course.course_name.lower() 
            for interest in student.interests.split(",")
        )
        course_rating = course_prof.specific_class_rating or 0
        match_score = (
            40 * major_match +
            55 * interest_match +
            5 * course_rating
        )
        
        if course_name not in unique_matches or match_score > unique_matches[course_name]['match_score']:
            unique_matches[course_name] = {
                "course_name": course.course_name,
                "professor_name": professor.name,
                "course_code": course.course_code,
                "match_score": round(match_score, 2),
                "semester": course_prof.semester,
                "course_rating": round(course_rating, 2),
                "course_id": course.id,
            }
    
    matches = sorted(unique_matches.values(), key=lambda x: x["match_score"], reverse=True)[:20]
    return render_template('matches.html', student=student, matches=matches)



@main.route('/save-match/<int:student_id>/<int:course_id>', methods=['POST'])
def save_match(student_id, course_id):
    student = Student.query.get_or_404(student_id)
    course_prof = CourseProfessor.query.get_or_404(course_id)
    if not student.saved_matches:
        student.saved_matches = ""

    saved_matches = student.saved_matches.split(",")
    if str(course_prof.id) not in saved_matches:
        saved_matches.append(str(course_prof.id))
        student.saved_matches = ",".join(saved_matches)
        db.session.commit()

    return redirect(url_for('main.matches', student_id=student_id))

@main.route('/search')
def search():
    query = request.args.get('q')
    results = Professor.query.filter(Professor.name.ilike(f'%{query}%')).all()
    return render_template('search.html', results=results)

@main.route('/save_profile', methods=['POST'])
def save_profile():
    student_id = session.get('student_id')
    if not student_id:
        return redirect('/login')

    student = Student.query.get(student_id)
    if not student:
        return redirect('/signup')
    try:
        student.name = request.form.get('name')
        student.class_year = request.form.get('class_year')
        student.major = request.form.get('majors', '')
        student.interests = request.form.get('interests')
        student.clubs = request.form.get('clubs', '')
        student.previous_classes = request.form.get('previous_classes', '')
        assignment_prefs = request.form.getlist('assignment_preferences')
        class_time_prefs = request.form.getlist('class_time_preferences')
        student.assignment_preferences = ', '.join(assignment_prefs)
        student.class_time_preferences = ', '.join(class_time_prefs)
        print(student.major)
        db.session.commit()
        return redirect('/profile')

    except Exception as e:
        print(f"Error saving profile: {e}")
        return "An error occurred while saving your profile.", 500

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        if not student_id or not student_id.isdigit():
            return "Invalid Student ID. Please enter a numeric ID.", 400

        student_id = int(student_id)
        student = Student.query.get(student_id)

        if student:
            session['student_id'] = student_id
            return redirect('/profile')
        else:
            return redirect(url_for('main.signup', student_id=student_id))

    return render_template('login.html')
from flask import Blueprint, redirect, render_template, request, url_for, session, jsonify


@main.route('/signup/<int:student_id>', methods=['GET', 'POST'])
def signup(student_id):
    if request.method == 'GET':
        return render_template('signup.html', student_id=student_id)

    elif request.method == 'POST':
        try:
            name = request.form.get('name')
            class_year = request.form.get('class_year')
            majors = request.form.get('majors', '') 
            previous_classes = request.form.get('previous_classes', '')
            clubs = request.form.get('clubs', '')
            interests = request.form.get('interests', '')
            assignment_preferences = request.form.getlist('assignment_preferences')
            class_time_preferences = request.form.getlist('class_time_preferences')

            print(f"Form Data Received: name={name}, class_year={class_year}, majors={majors}, previous_classes={previous_classes}, clubs={clubs}, interests={interests}, assignment_preferences={assignment_preferences}, class_time_preferences={class_time_preferences}")

            if not name or not class_year or not majors:
                print("Missing required fields detected!")
                return "Missing required fields", 400

            assignment_prefs_str = ', '.join(assignment_preferences)
            class_time_prefs_str = ', '.join(class_time_preferences)

            new_student = Student(
                id=student_id,
                name=name,
                class_year=class_year,
                major=majors,
                interests=interests,
                clubs=clubs,
                previous_classes=previous_classes,
                assignment_preferences=assignment_prefs_str,
                class_time_preferences=class_time_prefs_str
            )

            db.session.add(new_student)
            db.session.commit()
            session['student_id'] = student_id
            return redirect(url_for('main.student_profile'))

        except Exception as e:
            print(f"Error during signup: {e}")
            return "An error occurred during account creation", 500


@main.route('/is_logged_in', methods=['GET'])
def is_logged_in():
    if 'student_id' in session:
        return {'loggedIn': True}, 200
    else:
        return {'loggedIn': False}, 200
    
@main.route('/class_details/<int:course_id>')
def class_details(course_id):
    course = Course.query.get_or_404(course_id)
    course_professor = CourseProfessor.query.filter_by(course_id=course_id).first()
    clicked_professor = {
        "professor_name": course_professor.professor.name if course_professor and course_professor.professor else "N/A",
        "semester": course_professor.semester if course_professor and course_professor.semester else "N/A",
    }
    matching_courses = Course.query.filter_by(course_name=course.course_name).all()
    sections = []
    for match in matching_courses:
        course_professors = CourseProfessor.query.filter_by(course_id=match.id).all()
        for cp in course_professors:
            sections.append({
                "professor_name": cp.professor.name if cp.professor else "N/A",
                "semester": cp.semester if cp.semester else "N/A",
                "specific_class_rating": f"{cp.specific_class_rating:.2f}" if cp.specific_class_rating is not None else "N/A",
                "course_code": match.course_code
            })

    response_data = {
        "course_name": course.course_name,
        "course_code": course.course_code,
        "clicked_professor": clicked_professor, 
        "sections": sections,
    }

    return jsonify(response_data)



