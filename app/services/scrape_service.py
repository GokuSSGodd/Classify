import requests
from bs4 import BeautifulSoup

def get_professor_reviews(professor_name):
    url = f"https://www.ratemyprofessors.com/search/teachers?query={professor_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract reviews (simplified example)
    reviews = [review.text for review in soup.find_all(class_="ReviewText")]
    return reviews