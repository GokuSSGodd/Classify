import requests
from bs4 import BeautifulSoup
from app import create_app, db
from app.models import Professor, CourseProfessor
school_id = "1161"
BASE_SEARCH_URL = f"https://www.ratemyprofessors.com/search/professors/{school_id}?q="
BASE_PROFILE_URL = "https://www.ratemyprofessors.com"

def search_professor(professor_name):
    url = f"{BASE_SEARCH_URL}{professor_name}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data for {professor_name}")
        return None
    
    
    soup = BeautifulSoup(response.text, "html.parser")

    header = soup.find("div", class_="SearchResultsPage__SearchResultsPageHeader-vhbycj-3 qJihh")
    header_text = None

    if header:
        header_text = header.get_text(strip=True)

    if header_text and "No professors with" in header_text:
        print(f"No matching professor found for {professor_name}")
        return None

    results = soup.find_all("a", class_="TeacherCard__StyledTeacherCard-syjs0d-0 dLJIlx")
    for result in results:
        name_tag = result.find("div", class_="CardName__StyledCardName-sc-1gyrgim-0 cJdVEK")

        if "href" in result.attrs:
            profile_href = result["href"]
            profile_url = BASE_PROFILE_URL + profile_href
            #print("Profile URL:", profile_url)
        #else:
            #print("No href attribute found for this result")

        name = name_tag.text.strip() if name_tag else "Unknown"
        if name.lower().replace(" ", '') != professor_name.lower().replace(" ", ''):
            #print(name.lower().replace(" ", ''), professor_name.lower().replace(' ', ''))
            continue

        quality_tag = result.find("div", class_="CardNumRating__CardNumRatingNumber-sc-17t4b9u-2 gcFhmN")
        quality_rating = float(quality_tag.text.strip()) if quality_tag else None

        feedback_div = soup.find("div", class_="CardFeedback__StyledCardFeedback-lq6nix-0 frciyA")

        if feedback_div:
            feedback_tags = feedback_div.find_all("div", class_="CardFeedback__CardFeedbackItem-lq6nix-1 fyKbws")
            
            would_take_again = None
            difficulty_level = None

            for tag in feedback_tags:
                if "would take again" in tag.text.lower():
                    would_take_again = tag.find("div", class_="CardFeedback__CardFeedbackNumber-lq6nix-2 hroXqf").text.strip()
                elif "level of difficulty" in tag.text.lower():
                    difficulty_level = tag.find("div", class_="CardFeedback__CardFeedbackNumber-lq6nix-2 hroXqf").text.strip()

            #print(f"Would Take Again: {would_take_again}")
            #print(f"Level of Difficulty: {difficulty_level}")

        return {
            "name": name,
            "profile_url": profile_url,
            "quality_rating": quality_rating,
            "difficulty_level": difficulty_level,
            "would_take_again": would_take_again
        }

    #print(f"No matching professor found for {professor_name}")
    return None

def scrape_professor_profile(profile_url):
    """Scrape the professor's profile to get reviews and ratings."""
    response = requests.get(profile_url)
    if response.status_code != 200:
        print(f"Failed to access profile: {profile_url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    reviews = []

    review_elements = soup.find_all("div", class_="Rating__StyledRating-sc-1rhvpxz-1")

    for review in review_elements:
        try:
            course_div = review.find("div", class_="RatingHeader__StyledClass-sc-1dlkqw1-3")
            course_code = course_div.text.strip() if course_div else "Unknown"
            rating_div = review.find("div", class_="RatingValues__RatingContainer-sc-6dc747-1")
            rating_value = rating_div.find("div", class_="CardNumRating__CardNumRatingNumber-sc-17t4b9u-2").text.strip()
            rating = float(rating_value) if rating_value else None
            review_text_div = review.find("div", class_="Comments__StyledComments-dzzyvm-0")
            review_text = review_text_div.text.strip() if review_text_div else ""

            reviews.append({
                "course_code": course_code,
                "rating": rating,
                "review": review_text
            })
        except Exception as e:
            print(f"Error parsing review: {e}")
            continue

    return reviews

def process_professor_reviews():
    """Fetch reviews for all professors and update the database."""
    app = create_app()
    
    
    with app.app_context():
        professors = Professor.query.all()
        try:
            with db.session.no_autoflush:
                db.session.autoflush = False
                for professor in professors:
                    profile = search_professor(professor.name)
                    if not profile:
                        continue

                    reviews = scrape_professor_profile(profile['profile_url'])
                    if not reviews:
                        continue

                    course_reviews = {}
                    for review in reviews:
                        course_code = review["course_code"]
                        if course_code not in course_reviews:
                            course_reviews[course_code] = {
                                "total_rating": 0,
                                "count": 0,
                                "reviews": []
                            }
                        course_reviews[course_code]["total_rating"] += review["rating"]
                        course_reviews[course_code]["count"] += 1
                        course_reviews[course_code]["reviews"].append(review["review"])

                    for course_code, data in course_reviews.items():
                        avg_rating = data["total_rating"] / data["count"]
                        reviews_list = data["reviews"]

                        course_prof = CourseProfessor.query.join(Professor).filter(
                            CourseProfessor.professor_id == professor.id,
                            CourseProfessor.course.has(course_code=course_code)
                        ).first()

                        if course_prof:
                            course_prof.specific_class_rating = avg_rating
                            course_prof.reviews = reviews_list
                            db.session.commit() 
                            print(f"Updated {course_code} for {professor.name}: Avg {avg_rating}, {len(reviews_list)} reviews")
        except Exception as e:
            print(f"Exception occurred: {e}")
            db.session.rollback()  
        finally:
            db.session.close() 

if __name__ == "__main__":
    process_professor_reviews()