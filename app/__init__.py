import os
from typing import Text
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import json
import datetime
from playhouse.shortcuts import model_to_dict
from pymysql import Time

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306
    )

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

@app.route('/api/timeline_post', methods=['POST'])
def post_time_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/timeline')
def timeline():
    timelinePosts = get_time_line_post()
    return render_template('timeline.html', userPosts = timelinePosts['timeline_posts'], title="Timeline")

# @app.route('/api/timeline_post/<id>', methods=['DELETE'])
# def delete_time_line_post(id):
#     post = TimelinePost.query.get(id)
#     mydb.session.delete(post)
#     mydb.session.commit()

#     return {
#         'timeline_post_deleted': [
#             model_to_dict(post)
#         ],
#         'timeline_posts': [
#             model_to_dict(p)
#             for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
#         ]
#     }

with open('app/static/profiles.json') as f:
    parsedProfiles = json.load(f)

@app.route('/')
def index():
    return render_template('about.html', profiles = parsedProfiles, url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', profiles = parsedProfiles, url=os.getenv("URL"))

@app.route('/work-experience')
def experience():
    return render_template('work-experience.html', profiles = parsedProfiles, url=os.getenv("URL"))

@app.route('/education')
def education():
    return render_template('education.html', profiles = parsedProfiles, url=os.getenv("URL"))

@app.route('/places')
def places():
    return render_template('places.html', profiles = parsedProfiles, url=os.getenv("URL"))

@app.route('/contact')
def contact():
    return render_template('contact.html', profiles = parsedProfiles, url=os.getenv("URL"))
