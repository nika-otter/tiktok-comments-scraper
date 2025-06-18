from flask import Flask, request, render_template
from parser import get_comments
import random
import time
import threading

app = Flask(__name__)

all_users = []
processing = False
processing_error = None

def parse_comments_in_background(video_url, no_duplicates):
    global all_users, processing, processing_error
    try:
        comments = get_comments(video_url)
        if no_duplicates:
            seen = set()
            comments = [u for u in comments if u[1] not in seen and not seen.add(u[1])]
        all_users = comments
        processing_error = None
    except Exception as e:
        processing_error = str(e)
    finally:
        processing = False

@app.route('/', methods=['GET', 'POST'])
def index():
    global all_users, processing, processing_error
    winner = None
    error = processing_error

    if request.method == 'POST':
        if 'clear' in request.form:
            all_users = []
            processing_error = None
            return render_template('index.html', users=[], winner=None, error=None, processing=False)

        if 'get_comments' in request.form:
            video_url = request.form['video_url']
            no_duplicates = 'no_duplicates' in request.form
            if not processing:
                processing = True
                threading.Thread(target=parse_comments_in_background, args=(video_url, no_duplicates)).start()

        if 'pick_winner' in request.form:
            time.sleep(3)
            winner = random.choice(all_users) if all_users else None

    return render_template('index.html', users=all_users, winner=winner, error=error, processing=processing)

if __name__ == '__main__':
    from os import environ
    app.run(
        debug=environ.get("FLASK_DEBUG", "0") == "1",
        host='0.0.0.0',
        port=int(environ.get("PORT", 5001))
    )
