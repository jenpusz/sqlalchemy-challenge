


from flask import Flask

app = Flask(__name__)

def home():
    print("home() function called.")
    return "Welcome to my 'home' page."

def about():
    print("about() function called.")
    return "Welcome to my 'about' page."

home()
about()