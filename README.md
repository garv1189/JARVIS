JARVIS AI Assistant
A voice-activated AI assistant inspired by JARVIS from Iron Man, built with open-source tools. It supports 50 tasks, activated by the wake word "Hey Jarvis".
Features

Wake Word: Activates with "Hey Jarvis".
Tasks: Includes weather, stock prices, translations, QR code generation, and more (see full list in jarvis.py).
Interface: Streamlit web app for text-based interaction.

Setup

Clone Repository:git clone <your-repo-url>
cd jarvis


Install Dependencies:pip install -r requirements.txt


Set Up API Keys:
Create a .env file (see .env.example).
Obtain keys from:
OpenWeatherMap
NewsAPI
ExchangeRate-API
OMDB API
Edamam
NASA




Run Locally:streamlit run app.py



Deployment
See deployment instructions below for Streamlit Cloud.
Usage

Local: Run python jarvis.py for voice mode or streamlit run app.py for web mode.
Commands: Examples include "Hey Jarvis, what's the weather?", "Hey Jarvis, generate a password".

Notes

Voice input is limited in Streamlit Cloud; use text input.
Some tasks are simulated (e.g., email, transit) due to API restrictions.

