document.addEventListener('DOMContentLoaded', function () {
    console.log("matches.js loaded successfully");

    const modal = document.getElementById('class-modal');
    const closeBtn = document.querySelector('.close-btn');
    const classItems = document.querySelectorAll('.class-item');

    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    classItems.forEach(item => {
        const matchScore = item.getAttribute('data-score');
        const gradientBar = item.querySelector('.gradient-bar');

        if (matchScore && gradientBar) {
            gradientBar.style.width = `${matchScore}%`;
            gradientBar.style.background = `linear-gradient(90deg, red, yellow, green)`;
        }

        item.addEventListener('click', () => {
            const courseId = item.getAttribute('data-id');
            fetchClassDetails(courseId);
        });
    });

    function fetchClassDetails(courseId) {
        console.log(`Fetching details for course ID: ${courseId}`);
        fetch(`/class_details/${courseId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch class details');
                }
                return response.json();
            })
            .then(data => {
                populateModal(data);
                modal.style.display = 'block';
            })
            .catch(error => console.error('Error:', error));
    }

    function populateModal(data) {
        const modalClassName = document.getElementById('modal-class-name');
        const modalCourseCode = document.getElementById('modal-course-code');
        const modalProfessorName = document.getElementById('modal-professor-name');
        const modalSemester = document.getElementById('modal-semester');
        const sectionsList = document.getElementById('modal-sections-list');
    
        if (!modalClassName || !modalCourseCode || !modalProfessorName || !modalSemester || !sectionsList) {
            console.error('One or more modal elements are missing.');
            return;
        }
    
        modalClassName.textContent = data.course_name || "N/A";
        modalCourseCode.textContent = `Course Code: ${data.course_code || "N/A"}`;
        modalProfessorName.textContent = `Professor: ${data.clicked_professor.professor_name || "N/A"}`;
        modalSemester.textContent = `Semester: ${data.clicked_professor.semester || "N/A"}`;
    
        sectionsList.innerHTML = '';
        data.sections.forEach(section => {
            const li = document.createElement('li');
            li.textContent = `Professor: ${section.professor_name} | Semester: ${section.semester} | Rating: ${section.specific_class_rating}`;
            sectionsList.appendChild(li);
        });
    }
});
