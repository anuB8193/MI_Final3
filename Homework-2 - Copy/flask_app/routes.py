# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request
from .utils.database.database import database
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint
import random
import json

# Initialize database
db = database()

# Root route that redirects to home
@app.route('/')
def root():
    return redirect('/home')

# Home route with random fun fact
@app.route('/home')
def home():
    # Generate a random fun fact
    x = random.choice([
        'I have double-jointed fingers.',
        'I have two pet dogs.',
        'I enjoy drawing.'
    ])
    return render_template('home.html', fun_fact=x)

# Resume page route
@app.route('/resume')
def resume():
    # Fetch resume data from the database
    resume_data = db.getResumeData()
    print("Resume Data:", resume_data)  # Debugging output to confirm structure
    return render_template('resume.html', resume_data=resume_data)

# Projects page route
@app.route('/projects')
def projects():
    return render_template('projects.html')

# Piano page route
@app.route('/piano')
def piano():
    return render_template('piano.html')

# Feedback processing route
@app.route('/processfeedback', methods=['POST'])
@app.route('/processfeedback', methods=['POST'])
def processfeedback():
    # Access form data
    feedback_data = {
        'name': request.form['name'],
        'email': request.form['email'],
        'comment': request.form['comment']
    }
    
    # Insert feedback into the database
    db.query("INSERT INTO feedback (name, email, comment) VALUES (%s, %s, %s)", 
             (feedback_data['name'], feedback_data['email'], feedback_data['comment']))
    
    # Fetch all feedback to display
    feedback_entries = db.query("SELECT name, comment FROM feedback")
    
    # Render the processfeedback.html template with all feedback
    return render_template('processfeedback.html', feedback_entries=feedback_entries)
