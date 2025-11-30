from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import requests
import logging
import re
import random
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.utils import secure_filename
from flask import Response
import uuid 
from difflib import SequenceMatcher 
import uuid




# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

app.config['SECRET_KEY'] = 'qwpq vneg vbpq aiqz'  # Replace with a strong secret in production
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "postgresql+psycopg2://postgres:lalmatia56"
    "@34.131.0.33:5432/broqbot"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mashdeef@gmail.com'
app.config['MAIL_PASSWORD'] = 'qwpq vneg vbpq aiqz ' 

mail = Mail(app)

serializer = URLSafeTimedSerializer(app.secret_key)

app.secret_key = os.environ.get("SECRET_KEY", "super-secret-key")


def generate_reset_token(email):
    return serializer.dumps(email, salt='password-reset-salt')

def verify_reset_token(token, expiration=1800):	
    try:
    	return serializer.load(token, salt='password-reset-salt', max_age=max_age)
    	return email
    except Exception as e:
    	print("Token error:", e)
    	return None
    	
	


def upload_to_gcs(file_obj, bucket_name='broqbot-assets', folder='logos'):
    credentials = service_account.Credentials.from_service_account_file("/home/fawazm/Downloads/lowbudgetchatbot-21984ee2a071.json")
    client = storage.Client(credentials=credentials)
    bucket = client.bucket(bucket_name)

    filename = f"{folder}/{uuid.uuid4().hex}_{file_obj.filename}"
    blob = bucket.blob(filename)
    
    blob.upload_from_file(file_obj, content_type=file_obj.content_type)
    blob.make_public()
    
    return blob.public_url
    	
# Knowledge base for basic questions
faq_knowledge_base = {
    "how are you": "I'm just a bot, but I'm doing great! How about you?",
    "how old are you": "I don't have an age like humans, but I'm always learning!",
    "where are you from": "I was created by Fawaz, and I'm here to assist you!",
    "who made you": "I was made by Fawaz using Python and various cool APIs.",
    "what is your name": "I'm a chatbot created by Fawaz. You can call me Bot.",
    "what can you do": "I can help with weather updates, jokes, song recommendations, translations, and more!",
    "what is life": "Life is a journey of learning, growth, and experiences. What's your perspective?"
}

#roast
roast_knowledge_base = [
    "You're like a software update… always popping up at the worst time.",
    "Your secrets are safe with me. I never even listen.",
    "You're proof that even evolution has off days.",
    "You bring everyone so much joy — when you leave the room.",
    "You have something on your face… oh wait, that’s just your face."
    "You have something no one else has: my pity.",
    "You're not stupid; you just have a talent for making bad decisions consistently.",
    "You add value to every room… by leaving it.",
    "You're the reason warning labels exist.",
    "You have something special — a complete lack of talent.",
    "You're the kind of person who claps when the plane lands.",
    "You bring everyone together — to talk behind your back.",
    "You're the human version of a typo.",
    "You’d struggle to pour water out of a boot if the instructions were on the heel.",
    "You're like a participation trophy — unnecessary but kind of amusing.",
    "You're not a vibe. You're a warning.",
    "You're the result of ‘Ctrl + C’ and ‘Ctrl + Trash’",
    "You're like Wi-Fi in a basement — no connection.",
    "You're so irrelevant, your birth certificate is an apology letter.",
    "You're not ugly, but your personality sure is.",
    "You're the reason mirrors avoid eye contact.",
    "You make onions cry.",
    "You have something rare: consistent mediocrity.",
    "You have two speeds: slow and slower.",
    "You're the only person I know who can trip over a wireless signal.",
    "You're the kind of person who brings a spoon to a gunfight.",
    "You're like expired milk — people regret getting too close.",
    "You're not even worth the roast… but here we are.",
    "You're so fake, even Barbie's jealous.",
    "You're like a white crayon — nobody knows why you're even here.",
    "You're not toxic, you're radioactive.",
    "You're the poster child for birth control.",
    "You're the reason the gene pool needs a lifeguard.",
    "You're the punchline to your own existence.",
    "You're the kind of person who Googles ‘how to blink.’",
    "You're a full-time clown on a part-time brain.",
    "You're like Netflix with no skip intro button —",
    "You're like a popup ad — annoying",
    "You're the ‘before’ photo in every transformation post.",
    "You're a puzzle — missing all the good pieces.",
    "You're so cold, Antarctica's jealous.",
    "You're not even bad… you're aggressively average.",
    "You're the kind of person who replies to their own stories.",
    "You're so awkward, even your shadow avoids you.",
    "You're not the main character. You’re not even the background."
    "You're like a black hole — nothing good escapes your presence.",
    "You're living proof that karma sometimes forgets.",
    "You're so stupid, even autocorrect gives up.",
    "You're the human version of buffering.",
    "If I had a dollar for every smart thing you said, I’d be broke."
]

flirt_knowledge_base = [
    "Are you a magician? Because whenever I look at you, everyone else disappears.",
    "Do you believe in love at first chat?",
    "Is your name Wi-Fi? Because I'm feeling a connection.",
    "Are you made of copper and tellurium? Because you're Cu-Te 😘",
    "I must be a snowflake, because I've fallen for you.",
    "Do you have a name, or can I call you mine?",
    "If I were a cat, I’d spend all 9 lives with you."
    "Are you French? Because Eiffel for you.",
    "If I had a star for every time you crossed my mind, I’d have a galaxy.",
    "I’m not a photographer, but I can picture us together.",
    "Do you have a map? Because I just got lost in your eyes.",
    "Your hand looks heavy — can I hold it for you?",
    "Are you a keyboard? Because you’re just my type.",
    "If I were a cat, I’d spend all 9 lives with you.",
    "Do you have a pencil? Because I want to erase your past and write our future.",
    "If kisses were snowflakes, I’d send you a blizzard.",
    "Are you a time traveler? Because I see you in my future.",
    "You're not a snack — you’re the whole meal.",
    "Are we at the airport? Because my heart is taking off.",
    "If you were a song, you'd be the one stuck in my head all day.",
    "Are you sunlight? Because you brighten up my world.",
    "Is your smile legal? Because it’s causing a major distraction.",
    "I must be a snowflake, because I’ve fallen for you.",
    "Are you made of copper and tellurium? Because you’re Cu-Te.",
    "Do you like raisins? No? How about a date?",
    "Even my code crashes when you’re around — you’re too stunning.",
    "If beauty were time, you'd be an eternity.",
    "Are you my phone charger? Because without you, I die.",
    "You must be a bank loan, because you have my interest.",
    "If you were a vegetable, you’d be a cutecumber.",
    "You must be tired — you’ve been running through my mind all day.",
    "I wish I were cross-eyed so I could see you twice.",
    "If I had a dollar for every time I thought of you, I'd be rich.",
    "You’re so sweet, you’d put sugar out of business.",
    "Are you a light bulb? Because you just brightened my day.",
    "I’d never play hide and seek with you, because someone like you is impossible to find.",
    "Are you a campfire? Because you’re hot and I want s’more.",
    "Your beauty made my chatbot lag for a second.",
    "You had me at ‘Hi’.",
    "I must be dreaming, because you’re too perfect to be real.",
    "If looks could code, you’d be a flawless program.",
    "You're like sunshine on a rainy day — warm and unexpected.",
    "Even gravity can’t hold me down when you’re around.",
    "Your voice is my new favorite melody.",
    "I didn’t believe in love at first sight — until I saw you.",
    "You make my heart skip like a bad internet connection.",
    "You’re not just charming — you’re dangerously disarming.",
    "You’re my favorite notification.",
    "You’ve got everything I’ve been Googling for.",
    "If flirting were a crime, I’d be serving life for you.",
    "Your smile is like a bug fix — it just made everything better.",
    "You’re the kind of person poets write about.",
    "If you were a Git repo, I'd fork you instantly.",
    "Are you a sunrise? Because you make my morning brighter.",
    "You make the stars jealous — they’ve lost their shine.",
    "If charm was a currency, you’d be a billionaire.",
    "You're the upgrade I didn't know I needed.",
    "You must be a bug — because you’re stuck in my system.",
    "Your laugh? 10/10 would hear on loop.",
    "If hearts were emojis, mine would be 💘 every time I see you.",
    "You're my favorite notification and my best distraction.",
    "Are you a spell? Because every time I see you, I’m enchanted.",
    "You're like caffeine — I can’t function without you.",
    "I don’t need the stars when I have your smile.",
]


#time-opening

def get_time_of_day_greeting():
    current_hour = datetime.now().hour
    if 6 <= current_hour < 12:
        return "Good morning 🌞 I'm a chatbot made by Fawaz, how can I help you today?"
    elif 12 <= current_hour < 18:
        return "Good afternoon🌻🌇 I'm a chatbot made by Fawaz, how can I help you?"
    elif 18 <= current_hour < 22:
        return "Good evening 🌙 I'm a chatbot made by Fawaz, how can I assist you?"
    else:
        return "Hello there 🌜🌃 I know it’s pretty late, but I’m always here to help!"

def get_motivational_quote():
    try:
        url = "https://zenquotes.io/api/random"
        response = requests.get(url)
        response.raise_for_status()
        quote_data = response.json()
        if quote_data:
            return f'"{quote_data[0]["q"]}" - {quote_data[0]["a"]}'
        else:
            return "Sorry, I couldn't fetch a motivational quote right now."
    except requests.exceptions.RequestException as e:
        logging.error(f"Quote API error: {e}")
        return "Sorry, I couldn't fetch a motivational quote right now."

# Mapping moods to genres
mood_map = {
    "happy": ["pop", "funk", "dance"],
    "sad": ["acoustic", "blues", "folk"],
    "angry": ["metal", "hard rock", "punk"],
    "chill": ["chill", "lofi", "indie"],
    "edm": ["electronic", "house", "trance"],
    "excited": ["pop", "electronic", "dance"],
    "relaxed": ["jazz", "chill", "lofi"],
    "romantic": ["r&b", "soul", "acoustic"],
    "motivated": ["hip-hop", "rock", "pop"],
    "energetic": ["dance", "rock", "pop"],
    "rock": ["rock", "hard rock", "punk"],
    "nostalgic": ["80s", "90s", "classic rock"],
    "focused": ["lofi", "classical", "ambient"],
    "calm": ["ambient", "instrumental", "chill"]
}

# Genre-based song recommendations
genre_songs = {
    "pop": [
        {"name": "360", "artist": "Charli XCX", "url": "https://open.spotify.com/track/4w2GLmK2wnioVnb5CPQeex"},
        {"name": "And The Beat Goes On", "artist": "The Whispers", "url": "https://open.spotify.com/track/42MAEkamRaomzO3UWqGdh3"},
        {"name": "Billie Jean ", "artist": "Michael Jackson", "url": "https://open.spotify.com/track/7J1uxwnxfQLu4APicE5Rnj?si=47675273df2e41d1"},
        {"name": "Like a Prayer ", "artist": "Madonna", "url": "https://open.spotify.com/track/1z3ugFmUKoCzGsI6jdY4Ci?si=533ab1f0ad4a4638"},
        {"name": "I  Wanna Dance with Somebody (Who Loves Me)", "artist": "Whitney Houston", "url": "https://open.spotify.com/track/2tUBqZG2AbRi7Q0BIrVrEj?si=056a913dc02a4999"},
    ],
    "funk": [
        {"name": "Uptown Funk", "artist": "Mark Ronson ft. Bruno Mars", "url": "https://open.spotify.com/track/32OlwWuMpZ6b0aN2RZOeMS"},
        {"name": "Superstition", "artist": "Stevie Wonder", "url": "https://open.spotify.com/track/3wpL0cSc7tvY7uUtHEyW9i"},
    ],
    "dance": [
        {"name": "Titanium", "artist": "David Guetta ft. Sia", "url": "https://open.spotify.com/track/0lHAMNU8RGiIObScrsRgmP"},
        {"name": "Don't Start Now", "artist": "Dua Lipa", "url": "https://open.spotify.com/track/3PfIrDoz19wz7qK7tYeu62"},
    ],
    "acoustic": [
        {"name": "Fast Car", "artist": "Tracy Chapman", "url": "https://open.spotify.com/track/2M9ro2krNb7nr7HSprkEgo?si=d30a55be412a48bd"},
        {"name": "Skinny Love", "artist": "Bon Iver", "url": "https://open.spotify.com/track/3B3eOgLJSqPEA0RfboIQVM?si=8a644c97431a4f39"},
    ],
    "lofi": [
        {"name": "Lofi Chill Beats", "artist": "Lofi Girl", "url": "https://open.spotify.com/track/3qKKfRlxH0JvFfwvO0teay"},
        {"name": "Sleepy Vibes", "artist": "Chillhop Music", "url": "https://open.spotify.com/track/5Rv1r3pJNmmlUop7clu7W1"},
    ],
    "rock": [
        {"name": "Bohemian Rhapsody", "artist": "Queen", "url": "https://open.spotify.com/track/3z8h0TU7ReDPLIbEnYhWZb?si=148eff258b124e30"},
        {"name": "Sweet Child O' Mine", "artist": "Guns N' Roses", "url": "https://open.spotify.com/track/7snQQk1zcKl8gZ92AnueZW?si=2bf2e4fb08ca45e0"},
    ],
    "synthwave": [
        {"name": "Night Call", "artist": "Kavinsky", "url": "https://open.spotify.com/track/0U0ldCRmgCqhVvD6ksG63j?si=3f8ba12e09fb4227"},
        {"name": "Turbo Killer", "artist": "Carpenter Brut", "url": "https://open.spotify.com/track/10qbHF920zH5K8C8IcE5AL?si=3af5efdd407d4154"},
    ],
     "indie rock": [
        {"name": "Fluorescent Adolescent", "artist": "Arctic Monkeys", "url": "https://open.spotify.com/track/2x8evxqUlF0eRabbW2JBJd?si=bade2aad0f064a03"},
        {"name": "Take a Walk", "artist": "Passion Pit", "url": "https://open.spotify.com/track/4Sfa7hdVkqlM8UW5LsSY3F?si=55b0be3d2fa043a2"},
    ],
     "edm": [
        {"name": "Titanium", "artist": "David Guetta ft Sia", "url": "https://open.spotify.com/track/0TDLuuLlV54CkRRUOahJb4?si=7acccb3a3553419c"},
        {"name": "Wake Me Up", "artist": "Avicii", "url": "https://open.spotify.com/track/0nrRP2bk19rLc0orkWPQk2?si=aa8ebed2ad8546c2"},
    ],
     "jazz": [
        {"name": "Take Five", "artist": "The Dave Brubeck Quartet", "url": "https://open.spotify.com/track/1YQWosTIljIvxAgHWTp7KP?si=e8082c9370654596"},
        {"name": "Feeling Good", "artist": "Nina Simone", "url": "https://open.spotify.com/track/6Rqn2GFlmvmV4w9Ala0I1e?si=07a6471578a34f37"},
    ],
     "metal": [
        {"name": "Master of The Puppets", "artist": "Metallica", "url": "https://open.spotify.com/track/2MuWTIM3b0YEAskbeeFE1i?si=71cb9a3c3f7042e8"},
        {"name": "Paranoid (2012 Remaster)", "artist": "Black Sabbath", "url": "https://open.spotify.com/track/2z71jdeVcC782NgsYZ6N8q?si=b7223c636e5e4a8b"},
    ],
     "r&b": [
        {"name": "Blinding Lights", "artist": "The Weeknd", "url": "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b?si=9b3c734ceaf74f96"},
        {"name": "No Scrubs", "artist": "TLC", "url": "https://open.spotify.com/track/1KGi9sZVMeszgZOWivFpxs?si=0fda8ddc11744f1a"},
    ],
     "rap": [
        {"name": "SICKO MODE", "artist": "Travis Scott", "url": "https://open.spotify.com/track/2xLMifQCjDGFmkHkpNLD9h?si=aa70e852ce60477e"},
        {"name": "God's Plan", "artist": "Drake", "url": "https://open.spotify.com/track/6DCZcSspjsKoFjzjrWoCdn?si=5ae14a1374ec4f52"},
    ],
     "hip-hop": [
        {"name": "HUMBLE.", "artist": "Kendrick Lamar", "url": "https://open.spotify.com/track/7KXjTSCq5nL1LoYtL7XAwS?si=3615c9899199490f"},
        {"name": "Flashing Lights", "artist": "Kanye West ft Dwele", "url": "https://open.spotify.com/track/5TRPicyLGbAF2LGBFbHGvO?si=3cd8d913af754491"},
    ],
     "techno": [
        {"name": "Strobe", "artist": "deadmau5", "url": "https://open.spotify.com/track/4kJWtxDDNb9oAk3h7sX3N4?si=5d87ee114fce4475"},
        {"name": "Insomnia-Radio Edit", "artist": "Faithless", "url": "https://open.spotify.com/track/3dX6WDwnHwYzB5t754oB4T?si=9e81d80863f44b8e"},
    ],
     "chill": [
        {"name": "Sunflower", "artist": "Post Malone ft Swae Lee", "url": "https://open.spotify.com/track/3KkXRkHbMCARz0aVfEt68P?si=b741d0d808df4f05"},
        {"name": "Lost in Japan-Remix", "artist": "Shawn Mendex ft Zedd", "url": "https://open.spotify.com/track/575NJxNUVDqwJGdzBrlLbv?si=714437c7a54e49ac"},
    ],
     "classical": [
        {"name": "Clair De Lune", "artist": "Johann Debussy", "url": "https://open.spotify.com/track/6Er8Fz6fuZNi5cvwQjv1ya?si=e7d679f5de7e402d"},
        {"name": "Moonlight Sonata", "artist": "Ludwig Van Beethoven", "url": "https://open.spotify.com/track/1j2M5ekufbxpzGYzuorgKt?si=5414c6b546af489f"},
    ],
     "blues": [
        {"name": "The Thrill is Gone", "artist": "B.B. King", "url": "https://open.spotify.com/track/4NQfrmGs9iQXVQI9IpRhjM?si=538836838b014faa"},
        {"name": "Crossroad Blues", "artist": "Robert Johnson", "url": "https://open.spotify.com/track/1TrGdXSgiBm8W68D2K1COG?si=f08d348818f24e4b"},
    ],
     "ambient": [
        {"name": "Weightless", "artist": "Marconi Union", "url": "https://open.spotify.com/track/6kkwzB6hXLIONkEk9JciA6?si=bd08266a77c2475c"},
        {"name": "An Ending(Ascent)-Remastered 2005", "artist": "Brian Eno", "url": "https://open.spotify.com/track/1vgSaC0BPlL6LEm4Xsx59J?si=26907798208e46e3"},
    ],
     "folk": [
        {"name": "Home", "artist": "Edward Sharpe & The Magnetic Zeros", "url": "https://open.spotify.com/track/2x1jP9BexWtOKudvuUHbaD?si=cd983fab030244c0"},
        {"name": "The Times They Are A-Changin'", "artist": "Bob Dylan", "url": "https://open.spotify.com/track/52vA3CYKZqZVdQnzRrdZt6?si=cd07e537a45d4efc"},
    ],
     "indie": [
        {"name": "Electric Feel", "artist": "MGMT", "url": "https://open.spotify.com/track/3FtYbEfBqAlGO46NUDQSAt?si=948ec72cd9814de4"},
        {"name": "Dog Days Are Over", "artist": "Florence + The Machine", "url": "https://open.spotify.com/track/456WNXWhDwYOSf5SpTuqxd?si=20cd3627feee4cff"},
    ],
     "soft rock": [
        {"name": "Hotel California", "artist": "Eagles", "url": "https://open.spotify.com/track/1rh232CwAy3EDEWFJkwH88?si=f99c016e50b64ff3"},
        {"name": "Africa", "artist": "TOTO", "url": "https://open.spotify.com/track/2374M0fQpWi3dLnB54qaLX?si=7884bca6f3fa40f2"},
    ],
     "electronic": [
        {"name": "Stay Forever", "artist": "Whesthan ft STRFKR ", "url": "https://open.spotify.com/track/3N80kyacf7jzzOkYgLKW3q?si=5db19eec9ed340a2"},
        {"name": "Shelter", "artist": "Porter Robinson ft Madeon", "url": "https://open.spotify.com/track/2ewEh7LuvToYyGHq7yT8N1?si=4eb280e49f1149b9"},
    ],
     "soul": [
        {"name": "A Change Is Gonna Come", "artist": "Sam Cooke", "url": "https://open.spotify.com/track/0D0NwBMfJPoh1sZ61p5Fot?si=6dff3423d5244785"},
        {"name": "Let's Stay Together", "artist": "Al Green", "url": "https://open.spotify.com/track/63xdwScd1Ai1GigAwQxE8y?si=a86f84a5dee44a16"},
    ],
     "retro pop": [
        {"name": "Take on Me", "artist": "a-ha", "url": "https://open.spotify.com/track/2WfaOiMkCvy7F5fcp2zZ8L?si=cc8a9f84b2054a9d"},
        {"name": "Never Gonna Give you Up", "artist": "Rick Astley", "url": "https://open.spotify.com/track/4PTG3Z6ehGkBFwjybzWkR8?si=b351da5c3edc4bb8"},
    ],
     "reggaeton": [
        {"name": "Dákiti", "artist": "Bad Bunny ft JHAYCO", "url": "https://open.spotify.com/track/47EiUVwUp4C9fGccaPuUCS?si=e88f32ff435b4d90"},
        {"name": "Gasolina", "artist": "Daddy Yankee", "url": "https://open.spotify.com/track/5YoITs1m0q8UOQ4AW7N5ga?si=c4a7bb043e344f9b"},
    ],
     "house": [
        {"name": "Losing It", "artist": "FISHER", "url": "https://open.spotify.com/track/6ho0GyrWZN3mhi9zVRW7xi?si=5c6b1f14b57d4b57"},
        {"name": "Show Me Love", "artist": "Robin S", "url": "https://open.spotify.com/track/4t0UsYzmmmZRMTWn77jiGF?si=bad00ef1b6b84932"},
    ],
     "psychaedelic rock": [
        {"name": "Lucy In The Sky With Diamonds", "artist": "The Beatles", "url": "https://open.spotify.com/track/5wLkhxwU7B9DNglfZAIrQ8?si=c0dc59a12c9443b4"},
        {"name": "White Rabbit", "artist": "Jefferson Airplane", "url": "https://open.spotify.com/track/4vpeKl0vMGdAXpZiQB2Dtd?si=4060542327554f49"},
    ],
     "alternative": [
        {"name": "Somebody Else", "artist": "The 1975", "url": "https://open.spotify.com/track/4m0q0xQ2BNl9SCAGKyfiGZ?si=a6945d68d59446fa"},
        {"name": "Creep", "artist": "Radiohead", "url": "https://open.spotify.com/track/70LcF31zb1H0PyJoS1Sx1r?si=4f5991dc7a044197"},
    ],
     "downtempo": [
        {"name": "Teardrop", "artist": "Massive Attack ft Elizabeth Fraser", "url": "https://open.spotify.com/track/67Hna13dNDkZvBpTXRIaOJ?si=b152ce6a511740bd"},
        {"name": "You Wish", "artist": "Nightmares on Wax", "url": "https://open.spotify.com/track/6G6M4fl2I0eqEQnzyTwR8m?si=6ca8f937351b4725"},
    ],
     "darkwave": [
        {"name": "Lucretia My Reflection-Vinyl Version", "artist": "The Sisters of Mercy", "url": "https://open.spotify.com/track/20goDx14UZviYtCPtLbqvs?si=789b21ad22db493c"},
        {"name": "Blue Monday ", "artist": "New Order", "url": "https://open.spotify.com/track/6hHc7Pks7wtBIW8Z6A0iFq?si=dd02001a01a54195"},
    ],
     "industrial": [
        {"name": "Closer", "artist": "Nine Inch Nail", "url": "https://open.spotify.com/track/5mc6EyF1OIEOhAkD0Gg9Lc?si=a4d9b2367fb04c24"},
        {"name": "Du Hast", "artist": "Rammstein", "url": "https://open.spotify.com/track/5awDvzxWfd53SSrsRZ8pXO?si=e828b34b9ab345a7"},
    ],
     "gothic": [
        {"name": "Bela Lugosi’s Dead (Official Version)", "artist": "Bauhaus", "url": "https://open.spotify.com/track/1wyVyr8OhYsC9l0WgPPbh8?si=3bbcd1ed0e734c87"},
        {"name": "Lullaby", "artist": "The Cure", "url": "https://open.spotify.com/track/09OpntwPHuNICsyEt1ETpE?si=1d0e973d78f947b7"},
    ],
     "holiday": [
        {"name": "All I Want for Christmas Is You ", "artist": "Mariah Carey", "url": "https://open.spotify.com/track/0bYg9bo50gSsH3LtXe2SQn?si=d9d997b620b642ca"},
        {"name": "Last Christmas", "artist": "Wham!", "url": "https://open.spotify.com/track/2FRnf9qhLbvw8fu4IBXx78?si=a80049cb326c4838"},
    ],
     "experimental": [
        {"name": "Windowlicker", "artist": "Aphex Twins", "url": "https://open.spotify.com/track/409z4jUHpq7eIkg3N3FzZh?si=c5acefa7353244b7"},
        {"name": "Everything in Its Right Place ", "artist": "Radiohead", "url": "https://open.spotify.com/track/2kRFrWaLWiKq48YYVdGcm8?si=29304e82ebb74554"},
    ],
     "progressive rock": [
        {"name": "2112:Overture / The Temples Of Syrinx / Discovery / Presentation / Oracle / Soliloquy / Grand Finale", "artist": "Rush", "url": "https://open.spotify.com/track/2DMDV9kUEO2WjUHg5acHBY"},
        {"name": "Roundabout", "artist": "Yes", "url": "https://open.spotify.com/track/6KIFja6dizWkI7IpY0vmr8?si=bf18ba620a2c4fed"},
    ],
     "disco": [
        {"name": "Stayin’ Alive ", "artist": "Bee Gees", "url": "https://open.spotify.com/track/4UDmDIqJIbrW0hMBQMFOsM?si=17ff7d261fcb4b41"},
        {"name": "I Will Survive", "artist": "Gloria Gaynor", "url": "https://open.spotify.com/track/7rIovIsXE6kMn629b7kDig?si=6237ef9a69914385"},
    ],
     "dream pop": [
        {"name": "Space Song", "artist": "Beach House", "url": "https://open.spotify.com/track/1ujxjsoNvh4XgS2fUNwkZ2?si=ba8cb2b5988d40f9"},
        {"name": "Cherry-colored Funk ", "artist": "Cocteau Twins", "url": "https://open.spotify.com/track/5Rv1r3pJNmmlUop7clu7W1"},#change
    ],
     "shoe gaze": [
        {"name": "When You Sleep", "artist": "My Bloody Valentine", "url": "https://open.spotify.com/track/2KylN9C0wNbzLgZNTG9oiU?si=a61e96e7d1a2499c"},
        {"name": "Only Shallow ", "artist": "My Bloody Valentine", "url": "https://open.spotify.com/track/1KKuoYESWoUGsau6YYoEMl?si=a0fe6d7d9da743df"},
    ],
     "tropical house": [
        {"name": "Firestone", "artist": "Kygo ft. Conrad Sewell", "url": "https://open.spotify.com/track/1I8tHoNBFTuoJAlh4hfVVE?si=279702304d6342d4"},
        {"name": "Are You with Me", "artist": "Lost Frequencies", "url": "https://open.spotify.com/track/4255amV4enzl28KAn16rUO?si=cc0c6574081e4920"},
    ],
     "soca": [
        {"name": "Savannah Grass", "artist": "Kes", "url": "https://open.spotify.com/track/7omZHNEajQwaO6ApVFrjAy?si=c782a067024040d6"},
        {"name": "Like Ah Boss ", "artist": "Michael Montano", "url": "https://open.spotify.com/track/08uIpFwr0W4XuoJqR7uuQa?si=922e30c1c6bd4560"},
    ],
     "chillhop": [
        {"name": "Jazz Cabbage", "artist": "Strehlow ft Ian Ewing", "url": "https://open.spotify.com/track/1YY4o5H9qROo5Kb0EbfykE?si=d9bad896b9654057"},
        {"name": "Rainy Days ", "artist": "Chillhop Music", "url": "https://open.spotify.com/track/5Rv1r3pJNmmlUop7clu7W1"},#change
    ],
    # Add more genres with song data...
}

# Function to get song recommendations with randomization
def get_song_recommendation(user_input):
    # Match mood or genre from user input
    match = re.search(r"(happy|sad|chill|edm|angry|pop|excited|relaxed|romantic|motivated|energetic|rock|nostalgic|focused|calm|synthwave|indie rock|jazz|metal|r&b|rap|hip-hop|techno|acoustic|classical|blues|dance|ambient|lofi|funk|folk|indie|electronic|soft rock|soul|retro-pop|reggaeton|house|psychedelic rock|alternative|orchestral|gospel|downtempo|darkwave|industrial|gothic|holiday|christmas|experimental|progressive rock|disco|dream pop|shoegaze|tropical house|soca|soundtrack|chillhop)", user_input.lower())

    if match:
        key = match.group(1)

        # Determine if the key is a mood or a genre
        if key in mood_map:
            possible_genres = mood_map.get(key, [])
            selected_genre = random.choice(possible_genres) if possible_genres else None
        else:
            selected_genre = key  # Directly use genre if detected

        # Get songs from the selected genre
        if selected_genre and selected_genre in genre_songs:
            song_list = genre_songs[selected_genre]
            if song_list:
                random.shuffle(song_list)
                song = random.choice(song_list)
                return f"I recommend the song '{song['name']}' by {song['artist']}! 🎶 You can listen to it 👉 <a href='{song['url']}' target='_blank'>here</a>."
    
    return "Please specify a valid mood or genre 😅 For example, play a happy song or suggest an indie rock song. "

# Function to get weather
def get_weather(city):
    try:
        api_key = os.getenv("WEATHER_API_KEY", "f43fe0ae7a4ae800c6b66c74e48d3c01")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()

        if weather_data["cod"] != 200:
            return f"Sorry, I couldn't find weather data for {city}."

        description = weather_data["weather"][0]["description"]
        temp = weather_data["main"]["temp"]
        feels_like = weather_data["main"]["feels_like"]
        humidity = weather_data["main"]["humidity"]

        return (f"The weather in {city} is currently {description} with a temperature of {temp}°C, "
                f"feels like {feels_like}°C, and humidity of {humidity}%.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Weather API error: {e}")
        return "Sorry, I couldn't retrieve the weather information right now."

# Function to get jokes
def get_joke():
    try:
        url = "https://v2.jokeapi.dev/joke/Any"
        response = requests.get(url)
        response.raise_for_status()
        joke_data = response.json()

        if joke_data["type"] == "single":
            return joke_data["joke"]
        else:
            return f'{joke_data["setup"]} - {joke_data["delivery"]}'
    except requests.exceptions.RequestException as e:
        logging.error(f"Joke API error: {e}")
        return "Sorry, I couldn't fetch a joke right now."

# Function to convert currency
def convert_currency(amount, from_currency, to_currency):
    try:       
        api_key = os.getenv("CURRENCY_API_KEY", "your_currency_api_key")
        url = f"https://open.er-api.com/v6/latest/{from_currency}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "rates" in data and to_currency in data["rates"]:
            rate = data["rates"][to_currency]
            converted_amount = round(amount * rate, 2)
            return f"{amount} {from_currency} is {converted_amount} {to_currency}."
        else:
            return "Sorry, I couldn't process the currency conversion."
    except requests.exceptions.RequestException as e:
        logging.error(f"Currency Conversion API error: {e}")
        return "I couldn't retrieve currency conversion information right now."

# Google Translate API function
def translate_text_with_google_translate(text, target_language='zh'):  # Default to Chinese
    api_key = "AIzaSyDG8B8r9RqfBqu6Aao_ctXDIwrOPpdWGBY"  # Replace with your actual API key
    url = f"https://translation.googleapis.com/language/translate/v2"
    params = {
        'q': text,
        'target': target_language,
        'key': api_key
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        translation = response.json()

        if 'data' in translation and 'translations' in translation['data']:
            return translation['data']['translations'][0]['translatedText']
        else:
            return "Translation error occurred."
    except requests.exceptions.RequestException as e:
        logging.error(f"Translation API error: {e}")
        return "Translation error occurred."
        

# Intent classification function
def classify_intent(user_input):
    user_input_lower = user_input.lower()
   
    if user_input_lower in faq_knowledge_base:
        return "faq"
    if user_input_lower in ["hi", "hello", "hey", "hey there", "howdy", "greetings"]:
        return "greeting"
    elif "weather" in user_input_lower:
        return "weather"
    elif "joke" in user_input_lower or "tell me a joke" in user_input_lower:
        return "joke"
    elif "convert" in user_input_lower:
        return "currency"
    elif "roast me" in user_input_lower:
    	return "roast"
    elif "flirt with me" in user_input_lower:
    	return "flirt"
    elif "translate" in user_input_lower:
        return "translate"
    elif any(keyword in user_input_lower for keyword in ["recommend a song", "suggest a song", "tell me a song", "recommend a", "suggest a", "i need a song", "play a"]):
        return "song_recommendation"
    elif "motivate me!" in user_input_lower:
        return "motivation"
    else:
        return "unknown"
# Chat Route
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    logging.info(f"User: {user_input}")
    

    # Intent classification based on user input
    intent = classify_intent(user_input)

    response = ""

    # Respond based on detected intent
    if intent == "greeting":
        response = random.choice(["Hello #1! How can I assist you today?", 
                                  "Hi there! What can I help you with?", 
                                  "Greetings! What would you like to know?"])
    elif intent == "faq":
    	response= faq_knowledge_base.get(user_input.lower(), "Sorry,I don't know :(")
    elif intent == "weather":
        city_match = re.search(r"weather in (\w+)", user_input)
        if city_match:
            city = city_match.group(1)
            response = get_weather(city)
        else:
            response = "Please specify the city for weather information. For example, weather in Dhaka or weather in Tokyo"
    elif intent == "joke":
        response = get_joke()
    elif intent == "currency":
        match = re.match(r"convert (\d+(?:\.\d+)?) (\w+) to (\w+)", user_input)
        if match:
            amount, from_currency, to_currency = match.groups()
            amount = float(amount)
            response = convert_currency(amount, from_currency.upper(), to_currency.upper())
        else:
            response = "Please enter the currency conversion in the correct format: For example, convert 56 USD to EUR or convert 20983 AUD to GBP."
    elif intent == "translate":
        translate_match = re.match(r"translate (.+) in (.+)", user_input, re.IGNORECASE)
        if translate_match:
            text_to_translate = translate_match.group(1).strip()
            target_language = translate_match.group(2).strip().lower()
           
            language_map = {
                "afrikaans": "af", "albanian": "sq", "arabic": "ar", "armenian": "hy", 
                "azerbaijani": "az", "basque": "eu", "belarusian": "be", "bangla": "bn", 
                "bosnian": "bs", "bulgarian": "bg", "catalan": "ca", "cebuano": "ceb", 
                "chinese": "zh", "croatian": "hr", "czech": "cs", "danish": "da", "dutch": "nl", 
                "english": "en", "esperanto": "eo", "estonian": "et", "filipino": "tl", 
                "finnish": "fi", "french": "fr", "galician": "gl", "georgian": "ka", 
                "german": "de", "greek": "el", "gujarati": "gu", "haitian creole": "ht", 
                "hebrew": "iw", "hindi": "hi", "hungarian": "hu", "icelandic": "is", 
                "indonesian": "id", "irish": "ga", "italian": "it", "japanese": "ja", 
                "javanese": "jv", "kannada": "kn", "kazakh": "kk", "khmer": "km", "korean": "ko", 
                "kurdish": "ku", "kyrgyz": "ky", "lao": "lo", "latvian": "lv", "lithuanian": "lt", 
                "luxembourgish": "lb", "macedonian": "mk", "malagasy": "mg", "malay": "ms", 
                "maltese": "mt", "maori": "mi", "marathi": "mr", "mongolian": "mn", "myanmar": "my", 
                "nepali": "ne", "norwegian": "no", "pashto": "ps", "persian": "fa", "polish": "pl", 
                "portuguese": "pt", "punjabi": "pa", "romanian": "ro", "russian": "ru", 
                "samoan": "sm", "serbian": "sr", "sesotho": "st", "shona": "sn", "sindhi": "sd", 
                "sinhala": "si", "slovak": "sk", "slovenian": "sl", "somali": "so", 
                "spanish": "es", "sundanese": "su", "swahili": "sw", "swedish": "sv", 
                "tajik": "tg", "tamil": "ta", "telugu": "te", "thai": "th", "turkish": "tr", 
                "ukrainian": "uk", "urdu": "ur", "uzbek": "uz", "vietnamese": "vi", "welsh": "cy", 
                "xhosa": "xh", "yiddish": "yi", "yoruba": "yo", "zulu": "zu"
            }
            if target_language in language_map:
                target_language_code = language_map[target_language]
                response = translate_text_with_google_translate(text_to_translate, target_language_code)
            else:
                response = "Sorry, I don't support translation to that language."
        else:
            response = "Please specify the language for translation. For example, translate I love you in Spanish or translate Good morning in Korean"
    elif intent == "song_recommendation":
        response = get_song_recommendation(user_input)
    elif intent == "roast":
    	response = random.choice(roast_knowledge_base)
    elif intent == "flirt":
    	response = random.choice(flirt_knowledge_base)
    elif intent == "motivation":
    	response = get_motivational_quote()    
    else:
        response = random.choice([
            "I'm still learning! What else can I help you with?", 
            "That's interesting! Can you tell me more?", 
            "I'm not quite sure about that. What else would you like to discuss?",
            "Let's talk about something else! How about a joke or the weather?"
        ])

    return jsonify({"response": response})
    

@app.route('/')
def index():
    
    opening_message = get_time_of_day_greeting()
    
    return render_template('index.html', opening_message=opening_message)

@app.route('/quick_action', methods=['POST'])
def quick_action():
    data = request.json
    action = data.get('action')



from flask import request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename



import traceback
import logging


@app.route('/chatbot/ask', methods=['POST'])
def chatbot_ask_faq():
    data = request.get_json()
    user_message = data.get('message')
    client_id = data.get('client_id')

    if not user_message or not client_id:
        return jsonify({'response': "Invalid request."}), 400

    faqs = FAQ.query.filter_by(client_id=client_id).all()

    # Simple keyword match (you can replace with fuzzy search later)
    for faq in faqs:
        if faq.question.lower() in user_message.lower():
            return jsonify({'response': faq.answer})

    return jsonify({'response': "Sorry, I don't have an answer for that yet."})



@app.route('/business')
def business():
    return render_template('business.html')

@app.route('/chatbot/ask', methods=['POST'])
def chatbot_ask():
    data = request.json
    user_input = data.get("message", "").lower()
    brand_id = data.get("brand_id")

    faqs = FAQ.query.filter_by(brand_id=brand_id).all()

    if not faqs:
        return jsonify({'answer': "Sorry, no FAQs available."})

    best_match = None
    best_score = 0

    for faq in faqs:
        score = SequenceMatcher(None, user_input, faq.question.lower()).ratio()
        if score > best_score:
            best_score = score
            best_match = faq

    if best_score > 0.6:
        return jsonify({'answer': best_match.answer})
    else:
        return jsonify({'answer': "Sorry, I don't have an answer to that."})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)