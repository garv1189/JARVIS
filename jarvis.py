import speech_recognition as sr
import pyttsx3
import spacy
import requests
import wikipediaapi
from datetime import datetime
import webbrowser
import re
import yfinance as yf
from googletrans import Translator
import random
import json
import textblob
import qrcode
import streamlit as st

# Initialize components
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()
nlp = spacy.load("en_core_web_sm")
wiki = wikipediaapi.Wikipedia('en')
translator = Translator()

# Set up voice properties
tts_engine.setProperty('rate', 150)
tts_engine.setProperty('volume', 0.9)

def speak(text):
    """Convert text to speech."""
    tts_engine.say(text)
    tts_engine.runAndWait()
    return text

def listen(wake_word="hey jarvis"):
    """Listen for voice input with wake word detection."""
    with sr.Microphone() as source:
        print("Listening for wake word...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=10)
            text = recognizer.recognize_google(audio).lower()
            print(f"Heard: {text}")
            if wake_word in text:
                print("Wake word detected!")
                return text.replace(wake_word, "").strip()
            return None
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return None

def get_intent(text):
    """Extract intent from text using spaCy."""
    doc = nlp(text)
    if any(token.lemma_ in ["weather", "forecast"] for token in doc):
        return "weather"
    elif any(token.lemma_ in ["remind", "reminder", "set"] for token in doc):
        return "reminder"
    elif any(token.lemma_ in ["search", "find", "lookup"] for token in doc):
        return "search"
    elif any(token.lemma_ in ["time", "clock"] for token in doc):
        return "time"
    elif any(token.lemma_ in ["news", "headline"] for token in doc):
        return "news"
    elif any(token.lemma_ in ["email", "mail", "send"] for token in doc):
        return "email"
    elif any(token.lemma_ in ["calendar", "event", "schedule"] for token in doc):
        return "calendar"
    elif any(token.lemma_ in ["convert", "conversion"] for token in doc):
        return "convert"
    elif any(token.lemma_ in ["calculate", "calc", "math"] for token in doc):
        return "calculate"
    elif any(token.lemma_ in ["wiki", "wikipedia", "summary"] for token in doc):
        return "wiki"
    elif any(token.lemma_ in ["stock", "price", "share"] for token in doc):
        return "stock"
    elif any(token.lemma_ in ["currency", "exchange"] for token in doc):
        return "currency"
    elif any(token.lemma_ in ["translate", "translation"] for token in doc):
        return "translate"
    elif any(token.lemma_ in ["joke", "funny"] for token in doc):
        return "joke"
    elif any(token.lemma_ in ["fact", "trivia"] for token in doc):
        return "fact"
    elif any(token.lemma_ in ["movie", "film"] for token in doc):
        return "movie"
    elif any(token.lemma_ in ["book", "novel"] for token in doc):
        return "book"
    elif any(token.lemma_ in ["define", "definition", "dictionary"] for token in doc):
        return "dictionary"
    elif any(token.lemma_ in ["transit", "bus", "train"] for token in doc):
        return "transit"
    elif any(token.lemma_ in ["alarm"] for token in doc):
        return "alarm"
    elif any(token.lemma_ in ["timer", "countdown"] for token in doc):
        return "timer"
    elif any(token.lemma_ in ["recipe", "cook"] for token in doc):
        return "recipe"
    elif any(token.lemma_ in ["fitness", "exercise"] for token in doc):
        return "fitness"
    elif any(token.lemma_ in ["post", "tweet", "social"] for token in doc):
        return "social"
    elif any(token.lemma_ in ["todo", "task"] for token in doc):
        return "todo"
    elif any(token.lemma_ in ["quote", "inspiration"] for token in doc):
        return "quote"
    elif any(token.lemma_ in ["astronomy", "space", "picture"] for token in doc):
        return "apod"
    elif any(token.lemma_ in ["traffic", "road"] for token in doc):
        return "traffic"
    elif any(token.lemma_ in ["event", "local"] for token in doc):
        return "events"
    elif any(token.lemma_ in ["password", "generate"] for token in doc):
        return "password"
    elif any(token.lemma_ in ["flight", "plane"] for token in doc):
        return "flight"
    elif any(token.lemma_ in ["crypto", "bitcoin", "ethereum"] for token in doc):
        return "crypto"
    elif any(token.lemma_ in ["lyrics", "song"] for token in doc):
        return "lyrics"
    elif any(token.lemma_ in ["podcast"] for token in doc):
        return "podcast"
    elif any(token.lemma_ in ["sport", "score", "game"] for token in doc):
        return "sports"
    elif any(token.lemma_ in ["meditate", "meditation"] for token in doc):
        return "meditation"
    elif any(token.lemma_ in ["learn", "phrase", "language"] for token in doc):
        return "language"
    elif any(token.lemma_ in ["history", "historical"] for token in doc):
        return "history"
    elif any(token.lemma_ in ["restaurant", "food", "nearby"] for token in doc):
        return "restaurant"
    elif any(token.lemma_ in ["budget", "finance"] for token in doc):
        return "budget"
    elif any(token.lemma_ in ["file", "organize"] for token in doc):
        return "file"
    elif any(token.lemma_ in ["summarize", "summary", "email"] for token in doc):
        return "email_summary"
    elif any(token.lemma_ in ["meeting", "schedule"] for token in doc):
        return "meeting"
    elif any(token.lemma_ in ["code", "snippet"] for token in doc):
        return "code"
    elif any(token.lemma_ in ["blog", "idea"] for token in doc):
        return "blog"
    elif any(token.lemma_ in ["grammar", "check"] for token in doc):
        return "grammar"
    elif any(token.lemma_ in ["sentiment", "emotion"] for token in doc):
        return "sentiment"
    elif any(token.lemma_ in ["qr", "code"] for token in doc):
        return "qr"
    elif any(token.lemma_ in ["image", "describe"] for token in doc):
        return "image"
    elif any(token.lemma_ in ["memo", "record"] for token in doc):
        return "memo"
    return None

def get_weather(city="London"):
    """Fetch weather data."""
    api_key = st.secrets["OPENWEATHERMAP_API_KEY"]
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url).json()
        if response.get("cod") != 200:
            return "Sorry, I couldn't fetch the weather."
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        return f"The weather in {city} is {desc} with a temperature of {temp}°C."
    except:
        return "Sorry, there was an error fetching the weather."

def set_reminder(task, time_str):
    """Set a reminder (simulated)."""
    return f"Reminder set for '{task}' at {time_str}."

def web_search(query):
    """Perform a web search."""
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Searching for {query} on the web."

def get_time():
    """Return the current time."""
    return datetime.now().strftime("The current time is %H:%M.")

def get_news():
    """Fetch news headlines."""
    api_key = st.secrets["NEWSAPI_KEY"]
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    try:
        response = requests.get(url).json()
        articles = response.get("articles", [])[:3]
        if not articles:
            return "Sorry, I couldn't fetch the news."
        news = "Here are the top headlines: "
        for i, article in enumerate(articles, 1):
            news += f"{i}. {article['title']}. "
        return news
    except:
        return "Sorry, there was an error fetching the news."

def send_email(to_email, subject, body):
    """Simulate sending an email."""
    return f"Simulated email sent to {to_email} with subject '{subject}' and body '{body}'."

def add_calendar_event(event, date):
    """Simulate adding a calendar event."""
    return f"Calendar event '{event}' added for {date}."

def unit_conversion(text):
    """Perform unit conversion."""
    match = re.search(r"(\d+\.?\d*)\s*(meters?|m)\s*to\s*(feet|ft)", text)
    if match:
        value = float(match.group(1))
        result = value * 3.28084
        return f"{value} meters is {result:.2f} feet."
    return "Sorry, I couldn't understand the conversion request."

def calculate(expression):
    """Perform basic calculations."""
    try:
        result = eval(expression, {"__builtins__": {}})
        return f"The result of {expression} is {result}."
    except:
        return "Sorry, I couldn't perform the calculation."

def get_wiki_summary(topic):
    """Fetch a Wikipedia summary."""
    page = wiki.page(topic)
    if not page.exists():
        return f"Sorry, I couldn't find a Wikipedia page for {topic}."
    summary = page.summary[:500]
    return f"Here's a summary of {topic}: {summary}"

def get_stock_price(symbol):
    """Fetch stock price."""
    try:
        stock = yf.Ticker(symbol)
        price = stock.history(period="1d")["Close"].iloc[-1]
        return f"The current price of {symbol} is ${price:.2f}."
    except:
        return f"Sorry, I couldn't fetch the stock price for {symbol}."

def currency_conversion(amount, from_currency, to_currency):
    """Convert currency."""
    api_key = st.secrets["EXCHANGERATE_API_KEY"]
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"
    try:
        response = requests.get(url).json()
        rate = response["conversion_rates"][to_currency]
        result = amount * rate
        return f"{amount} {from_currency} is {result:.2f} {to_currency}."
    except:
        return "Sorry, I couldn't perform the currency conversion."

def translate_text(text, target_lang="es"):
    """Translate text."""
    try:
        translation = translator.translate(text, dest=target_lang)
        return f"Translation to {target_lang}: {translation.text}"
    except:
        return "Sorry, I couldn't perform the translation."

def tell_joke():
    """Fetch a random joke."""
    url = "https://official-joke-api.appspot.com/random_joke"
    try:
        response = requests.get(url).json()
        return f"{response['setup']} {response['punchline']}"
    except:
        return "Why did the computer go to art school? Because it wanted to learn to draw a better byte!"

def random_fact():
    """Fetch a random fact."""
    url = "https://uselessfacts.jsph.pl/random.json?language=en"
    try:
        response = requests.get(url).json()
        return f"Did you know? {response['text']}"
    except:
        return "Did you know? Honey never spoils."

def get_movie_info(title):
    """Fetch movie info."""
    api_key = st.secrets["OMDB_API_KEY"]
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    try:
        response = requests.get(url).json()
        if response["Response"] == "False":
            return f"Sorry, I couldn't find information for {title}."
        return f"{title}: {response['Plot']} Rated {response['imdbRating']} on IMDb."
    except:
        return "Sorry, I couldn't fetch movie information."

def search_book(title):
    """Search for a book."""
    url = f"https://www.googleapis.com/books/v1/volumes?q={title}"
    try:
        response = requests.get(url).json()
        book = response["items"][0]["volumeInfo"]
        return f"Found {book['title']} by {', '.join(book['authors'])}. Published in {book['publishedDate']}."
    except:
        return f"Sorry, I couldn't find a book titled {title}."

def dictionary_lookup(word):
    """Look up a word's definition."""
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url).json()
        definition = response[0]["meanings"][0]["definitions"][0]["definition"]
        return f"The definition of {word} is: {definition}"
    except:
        return f"Sorry, I couldn't find a definition for {word}."

def get_transit_info():
    """Simulate public transit info."""
    return "Simulated: Next bus arrives in 10 minutes."

def set_alarm(time_str):
    """Simulate setting an alarm."""
    return f"Alarm set for {time_str}."

def set_timer(duration):
    """Simulate setting a timer."""
    return f"Timer set for {duration}."

def search_recipe(dish):
    """Search for a recipe."""
    app_id = st.secrets["EDAMAM_APP_ID"]
    app_key = st.secrets["EDAMAM_APP_KEY"]
    url = f"https://api.edamam.com/search?q={dish}&app_id={app_id}&app_key={app_key}"
    try:
        response = requests.get(url).json()
        recipe = response["hits"][0]["recipe"]
        return f"Recipe for {dish}: {recipe['label']}. Ingredients: {', '.join(recipe['ingredientLines'])}."
    except:
        return f"Sorry, I couldn't find a recipe for {dish}."

def track_fitness(activity):
    """Simulate fitness tracking."""
    return f"Simulated: Logged {activity} for 30 minutes."

def post_social_media(message):
    """Simulate posting to social media."""
    return f"Simulated post: {message}."

def manage_todo(task):
    """Manage a todo list (simulated)."""
    return f"Added '{task}' to your todo list."

def get_quote():
    """Fetch a quote of the day."""
    url = "https://quotes.rest/qod.json"
    try:
        response = requests.get(url).json()
        quote = response["contents"]["quotes"][0]
        return f"Quote of the day: {quote['quote']} by {quote['author']}"
    except:
        return "Stay curious, stay foolish. - Steve Jobs"

def get_apod():
    """Fetch NASA's Astronomy Picture of the Day."""
    api_key = st.secrets["NASA_API_KEY"]
    url = f"https://api.nasa.gov/planetary/apod?apiKey={api_key}"
    try:
        response = requests.get(url).json()
        return f"Astronomy Picture of the Day: {response['title']}. {response['explanation'][:200]}..."
    except:
        return "Sorry, I couldn't fetch the astronomy picture."

def get_traffic_info():
    """Simulate traffic info."""
    return "Simulated: Traffic is moderate on your route."

def get_local_events():
    """Simulate local events."""
    return "Simulated: Local concert this weekend at 7 PM."

def generate_password():
    """Generate a random password."""
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    password = "".join(random.choice(chars) for _ in range(12))
    return f"Generated password: {password}"

def check_flight_status(flight_number):
    """Simulate flight status lookup."""
    return f"Simulated: Flight {flight_number} is on time."

def get_crypto_price(symbol):
    """Fetch cryptocurrency price."""
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    try:
        response = requests.get(url).json()
        price = response[symbol]["usd"]
        return f"The current price of {symbol} is ${price}."
    except:
        return f"Sorry, I couldn't fetch the price for {symbol}."

def search_lyrics(song):
    """Search for song lyrics."""
    url = f"https://api.lyrics.ovh/v1/{song}"
    try:
        response = requests.get(url).json()
        lyrics = response["lyrics"][:200]
        return f"Lyrics for {song}: {lyrics}..."
    except:
        return f"Sorry, I couldn't find lyrics for {song}."

def search_podcast(topic):
    """Search for podcasts."""
    url = f"https://itunes.apple.com/search?term={topic}&media=podcast"
    try:
        response = requests.get(url).json()
        podcast = response["results"][0]
        return f"Found podcast: {podcast['trackName']} by {podcast['artistName']}."
    except:
        return f"Sorry, I couldn't find podcasts for {topic}."

def get_sports_scores():
    """Simulate sports scores."""
    return "Simulated: Team A won 3-2 against Team B."

def meditation_guide():
    """Provide a meditation guide."""
    return "Close your eyes, take a deep breath, and focus on your breathing for 5 minutes."

def language_phrase(phrase, lang="spanish"):
    """Provide a language learning phrase."""
    return translate_text(phrase, lang)

def historical_event(date):
    """Fetch historical events."""
    url = f"https://history.muffinlabs.com/date/{date}"
    try:
        response = requests.get(url).json()
        event = response["data"]["Events"][0]["text"]
        return f"On {date}: {event}"
    except:
        return f"Sorry, I couldn't find historical events for {date}."

def find_restaurants():
    """Simulate nearby restaurants."""
    return "Simulated: Nearby restaurants include Italian Bistro and Sushi Haven."

def track_budget(amount, category):
    """Simulate budget tracking."""
    return f"Simulated: Added ${amount} to {category} budget."

def organize_files():
    """Simulate file organization."""
    return "Simulated: Files organized into folders."

def summarize_email(text):
    """Simulate email summarization."""
    return f"Simulated: Summary of email: {text[:50]}..."

def schedule_meeting(time):
    """Simulate meeting scheduling."""
    return f"Simulated: Meeting scheduled for {time}."

def generate_code_snippet(lang):
    """Generate a code snippet."""
    snippets = {
        "python": "def hello():\n    print('Hello, World!')",
        "javascript": "console.log('Hello, World!');"
    }
    return snippets.get(lang.lower(), "Sorry, I don't have a snippet for that language.")

def blog_ideas(topic):
    """Generate blog post ideas."""
    return f"Blog ideas for {topic}: 1. Top 5 {topic} trends, 2. How to start with {topic}, 3. {topic} myths debunked."

def check_grammar(text):
    """Check grammar using TextBlob."""
    blob = textblob.TextBlob(text)
    return f"Grammar check: {blob.correct()}"

def sentiment_analysis(text):
    """Perform sentiment analysis."""
    blob = textblob.TextBlob(text)
    polarity = blob.sentiment.polarity
    return f"Sentiment: {'Positive' if polarity > 0 else 'Negative' if polarity < 0 else 'Neutral'}"

def generate_qr_code(data):
    """Generate a QR code."""
    qr = qrcode.QRCode()
    qr.add_data(data)
    qr.make(fit=True)
    return f"Simulated: QR code generated for {data}."

def describe_image():
    """Simulate image description."""
    return "Simulated: The image shows a scenic mountain landscape."

def record_memo():
    """Simulate voice memo recording."""
    return "Simulated: Voice memo recorded."

def process_command(text):
    """Process the voice command."""
    if not text:
        return "No command detected."
    intent = get_intent(text)
    if intent == "weather":
        city = "London"
        return get_weather(city)
    elif intent == "reminder":
        return set_reminder("task", "later")
    elif intent == "search":
        return web_search(text)
    elif intent == "time":
        return get_time()
    elif intent == "news":
        return get_news()
    elif intent == "email":
        return send_email("example@email.com", "Test", "Hello!")
    elif intent == "calendar":
        return add_calendar_event("Meeting", "tomorrow")
    elif intent == "convert":
        return unit_conversion(text)
    elif intent == "calculate":
        expression = re.search(r"(calculate|calc)\s+(.+)", text)
        if expression:
            return calculate(expression.group(2))
    elif intent == "wiki":
        topic = re.search(r"(wiki|wikipedia|summary)\s+(.+)", text)
        if topic:
            return get_wiki_summary(topic.group(2))
    elif intent == "stock":
        symbol = re.search(r"(stock|price|share)\s+(.+)", text)
        if symbol:
            return get_stock_price(symbol.group(2).upper())
    elif intent == "currency":
        match = re.search(r"(\d+\.?\d*)\s*(\w+)\s*to\s*(\w+)", text)
        if match:
            return currency_conversion(float(match.group(1)), match.group(2).upper(), match.group(3).upper())
    elif intent == "translate":
        match = re.search(r"translate\s+(.+)\s+to\s+(\w+)", text)
        if match:
            return translate_text(match.group(1), match.group(2))
    elif intent == "joke":
        return tell_joke()
    elif intent == "fact":
        return random_fact()
    elif intent == "movie":
        title = re.search(r"(movie|film)\s+(.+)", text)
        if title:
            return get_movie_info(title.group(2))
    elif intent == "book":
        title = re.search(r"(book|novel)\s+(.+)", text)
        if title:
            return search_book(title.group(2))
    elif intent == "dictionary":
        word = re.search(r"(define|definition|dictionary)\s+(.+)", text)
        if word:
            return dictionary_lookup(word.group(2))
    elif intent == "transit":
        return get_transit_info()
    elif intent == "alarm":
        time_str = re.search(r"alarm\s+(.+)", text)
        if time_str:
            return set_alarm(time_str.group(1))
    elif intent == "timer":
        duration = re.search(r"timer\s+(.+)", text)
        if duration:
            return set_timer(duration.group(1))
    elif intent == "recipe":
        dish = re.search(r"(recipe|cook)\s+(.+)", text)
        if dish:
            return search_recipe(dish.group(2))
    elif intent == "fitness":
        activity = re.search(r"(fitness|exercise)\s+(.+)", text)
        if activity:
            return track_fitness(activity.group(2))
    elif intent == "social":
        message = re.search(r"(post|tweet|social)\s+(.+)", text)
        if message:
            return post_social_media(message.group(2))
    elif intent == "todo":
        task = re.search(r"(todo|task)\s+(.+)", text)
        if task:
            return manage_todo(task.group(2))
    elif intent == "quote":
        return get_quote()
    elif intent == "apod":
        return get_apod()
    elif intent == "traffic":
        return get_traffic_info()
    elif intent == "events":
        return get_local_events()
    elif intent == "password":
        return generate_password()
    elif intent == "flight":
        flight = re.search(r"(flight|plane)\s+(.+)", text)
        if flight:
            return check_flight_status(flight.group(2))
    elif intent == "crypto":
        symbol = re.search(r"(crypto|bitcoin|ethereum)\s+(.+)", text)
        if symbol:
            return get_crypto_price(symbol.group(2).lower())
    elif intent == "lyrics":
        song = re.search(r"(lyrics|song)\s+(.+)", text)
        if song:
            return search_lyrics(song.group(2))
    elif intent == "podcast":
        topic = re.search(r"podcast\s+(.+)", text)
        if topic:
            return search_podcast(topic.group(1))
    elif intent == "sports":
        return get_sports_scores()
    elif intent == "meditation":
        return meditation_guide()
    elif intent == "language":
        match = re.search(r"(learn|phrase)\s+(.+)\s+(spanish|french|etc)", text)
        if match:
            return language_phrase(match.group(2), match.group(3))
    elif intent == "history":
        date = re.search(r"(history|historical)\s+(.+)", text)
        if date:
            return historical_event(date.group(2))
    elif intent == "restaurant":
        return find_restaurants()
    elif intent == "budget":
        match = re.search(r"(budget|finance)\s+(\d+\.?\d*)\s+(.+)", text)
        if match:
            return track_budget(match.group(2), match.group(3))
    elif intent == "file":
        return organize_files()
    elif intent == "email_summary":
        text = re.search(r"(summarize|summary)\s+(.+)", text)
        if text:
            return summarize_email(text.group(2))
    elif intent == "meeting":
        time = re.search(r"(meeting|schedule)\s+(.+)", text)
        if time:
            return schedule_meeting(time.group(2))
    elif intent == "code":
        lang = re.search(r"(code|snippet)\s+(.+)", text)
        if lang:
            return generate_code_snippet(lang.group(2))
    elif intent == "blog":
        topic = re.search(r"(blog|idea)\s+(.+)", text)
        if topic:
            return blog_ideas(topic.group(2))
    elif intent == "grammar":
        text = re.search(r"(grammar|check)\s+(.+)", text)
        if text:
            return check_grammar(text.group(2))
    elif intent == "sentiment":
        text = re.search(r"(sentiment|emotion)\s+(.+)", text)
        if text:
            return sentiment_analysis(text.group(2))
    elif intent == "qr":
        data = re.search(r"(qr|code)\s+(.+)", text)
        if data:
            return generate_qr_code(data.group(2))
    elif intent == "image":
        return describe_image()
    elif intent == "memo":
        return record_memo()
    else:
        return "Sorry, I don't understand that command."

def main():
    """Main loop for voice command processing."""
    speak("JARVIS online. Say 'Hey Jarvis' to activate.")
    while True:
        text = listen()
        if text:
            result = process_command(text)
            speak(result)
