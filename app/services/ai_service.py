#import openai
import os

#openai.api_key = os.getenv("OPENAI_API_KEY")

def get_match_score(class_name, description):
    prompt = f"Student wants to take '{class_name}'. How well does this class match their interests? Description: {description}"
    #response = openai.Completion.create(
    #    engine="text-davinci-003",
    #    prompt=prompt,
    #    max_tokens=50
    #)
    #match_score = response.choices[0].text.strip()
    return None
#maybe we should utilize a free huggingface model instead? openapi is cheap though for demo so might as well use my api key
