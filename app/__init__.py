from flask import Flask
from app.routes import main

app = Flask(__name__)
app.register_blueprint(main)

# Import other components if needed
from app import resume_evaluator, utils
