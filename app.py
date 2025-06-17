from flask import Flask, request, render_template
from parser import get_comments
import random
import time

app = Flask(__name__)
all_users = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global all_users
    winner = None
    error = None

    if request.method == 'POST':
        if 'clear' in request.form:
            time.sleep(3)
            all_users = []
            return render_template('index.html', users=[], winner=None)

        video_url = request.form['video_url']
        no_duplicates = 'no_duplicates' in request.form
        if 'get_comments' in request.form:
            try:
                all_users = get_comments(video_url)
                if no_duplicates:
                    seen = set()
                    all_users = [u for u in all_users if u[1] not in seen and not seen.add(u[1])]
            except Exception as e:
                error = str(e)

        if 'pick_winner' in request.form:
            time.sleep(3)
            winner = random.choice(all_users) if all_users else None

    return render_template('index.html', users=all_users, winner=winner, error=error)

if __name__ == '__main__':
    from os import environ
    app.run(
        debug=environ.get("FLASK_DEBUG", "0") == "1",
        host='0.0.0.0',
        port=int(environ.get("PORT", 5001))
    )