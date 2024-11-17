import requests
from bs4 import BeautifulSoup
import json
BASE_URL = "https://owaprod-pub.wesleyan.edu/reg/"

def save_to_json(data, filename="courses.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")

def format_professor_name(professor_name):
    """Reformat professor names from 'lastname,firstname middleinitial' to 'Firstname Lastname'."""
    if "," in professor_name:
        lastname, firstname = professor_name.split(",", 1)
        firstname_parts = firstname.strip().split()
        firstname = firstname_parts[0]
        formatted_name = f"{firstname} {lastname.strip()}"
        return formatted_name
    return professor_name.strip()

def get_categories(main_url):
    """Fetch all subject categories from the main WesMaps page."""
    response = requests.get(main_url)
    soup = BeautifulSoup(response.text, "html.parser")
    categories = []

    for link in soup.find_all("a", href=True):
        if "subj_page" in link["href"]:
            categories.append({
                "name": link.text.strip(),
                "url": BASE_URL + link["href"]
            })
    return categories

def get_courses_offered(category_url):
    """Fetch the 'Courses Offered' link for a subject category."""
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    courses_offered_link = None
    for link in soup.find_all("a", href=True):
        if "Courses Offered" in link.text:
            courses_offered_link = BASE_URL + link["href"]
            break
    return courses_offered_link

def get_course_links(courses_offered_url):
    """Get all individual course links from the 'Courses Offered' page."""
    response = requests.get(courses_offered_url)
    soup = BeautifulSoup(response.text, "html.parser")
    course_links = []

    for row in soup.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) < 3:
            continue
        course_link_tag = cols[0].find("a")
        if course_link_tag and course_link_tag.has_attr("href"):
            course_href = course_link_tag["href"]
            course_url = BASE_URL + course_href
            course_code_with_section = course_link_tag.text.strip()
            if '-' in course_code_with_section:
                course_code, section = course_code_with_section.split('-', 1)
            else:
                course_code = course_code_with_section
                section = ''
            course_links.append({
                'url': course_url,
                'course_code': course_code.strip(),
                'section': section.strip()
            })
    return course_links

def get_course_details(course_url, course_code, section):
    """Scrape detailed information from an individual course page."""
    response = requests.get(course_url)
    soup = BeautifulSoup(response.text, "html.parser")
    course_name = soup.find("span", class_="title").text.strip() if soup.find("span", class_="title") else "Unknown"

    semester = "Not Available"
    course_info = soup.find("td", valign="top")
    if course_info:
        info_text = course_info.get_text(separator='\n', strip=True).split('\n')
        if len(info_text) == 3:
            semester = info_text[2].split(' ')[0].strip()

    description = "No description available."
    title_tag = soup.find("span", class_="title")
    if title_tag:
        description_td = title_tag.find_next("td", {"colspan": "3"})
        if description_td:
            description = description_td.get_text(separator=' ', strip=True)
    examinations_assignments = 'Unavailable'
    examinations_assignments_b = soup.find('b', string='Examinations and Assignments: ')
    if examinations_assignments_b:
        examinations_assignments = examinations_assignments_b.next_sibling.get_text(strip=True).replace(":", '')
        if not examinations_assignments:
            examinations_assignments = 'Unavailable'
    credit_b = soup.find('b', string=lambda x: x and "Credit:" in x)
    if credit_b and credit_b.next_sibling:
        credit = credit_b.next_sibling.strip()
    else:
        credit = "Not Available"

    prerequisites_b = soup.find('b', string=lambda x: x and "Prerequisites:" in x)
    if prerequisites_b and prerequisites_b.next_sibling:
        prerequisites = prerequisites_b.next_sibling.strip()
    else:
        prerequisites = "Not Available"

    professor = "Not Available"
    instructor_b = soup.find('b', string='Instructor(s):')
    if instructor_b:
        professor_tag = instructor_b.find_next_sibling('a')
        if professor_tag:
            professor = format_professor_name(professor_tag.get_text(strip=True))

    time = "TBA"
    times_b = instructor_b.find_next('b', string='Times:') if instructor_b else None
    if times_b and times_b.next_sibling:
        time_text = times_b.next_sibling
        if isinstance(time_text, str):
            time = time_text.strip().rstrip(';')

    location = 'Not Available'
    location_b = soup.find('b', string='Location:')
    if location_b and location_b.next_sibling:
        location_text = location_b.next_sibling.strip()
        locations_list = [loc.strip() for loc in location_text.split(";") if loc.strip()]
        location = ", ".join(locations_list) if locations_list else 'Not Available'

    return {
        "course_name": course_name,
        "course_code": course_code,
        "section": str(int(section)),
        "semester": semester,
        "description": description,
        "examinations_assignments": examinations_assignments,
        "credit": credit,
        "prerequisites": prerequisites,
        "professor": professor,
        "time": time,
        "location": location
    }

def main():
    main_url = BASE_URL + "!wesmaps_page.html"

    print("Fetching subject categories...")
    categories = get_categories(main_url)

    all_courses = []

    for category in categories:
        print(f"Processing category: {category['name']}")
        courses_offered_url = get_courses_offered(category["url"])
        if not courses_offered_url:
            print(f"No 'Courses Offered' link found for {category['name']}")
            continue
        print(f"Fetching courses from: {courses_offered_url}")
        course_links = get_course_links(courses_offered_url)
        for course_info in course_links:
            course_url = course_info['url']
            course_code = course_info['course_code']
            section = course_info['section']
            course_details = get_course_details(course_url, course_code, section)
            #print(course_details)
            all_courses.append(course_details)
    print(f"Total Courses Scraped: {len(all_courses)}")
    save_to_json(all_courses)
if __name__ == "__main__":
    main()
