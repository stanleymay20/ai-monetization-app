from fastapi import FastAPI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import firebase_admin
from firebase_admin import credentials, firestore
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Initialize Firebase
cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Initialize OpenAI API
openai = ChatOpenAI(model_name="gpt-4", temperature=0.7)

# Scraping Google Trends
@app.get("/trends")
def get_trending_topics():
    url = "https://trends.google.com/trends/trendingsearches/daily?geo=US"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    trends = [trend.text.strip() for trend in soup.find_all("a", class_="title")]
    return {"trending_topics": trends}

# AI-Powered Content Generation
@app.post("/generate-content")
def generate_content(topic: str):
    prompt = f"Write an SEO-optimized blog post about {topic}."
    ai_response = openai([HumanMessage(content=prompt)])
    doc_ref = db.collection("generated_content").document()
    doc_ref.set({"topic": topic, "content": ai_response.content})
    return {"content": ai_response.content}

@app.get("/")
def home():
    return {"message": "AI Monetization App is Running!"}
