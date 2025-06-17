import secrets
import uuid

from flask import Flask, request, render_template, session
from parser import get_comments
import random
import time
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
@app.route('/', methods=['GET', 'POST'])
def index():
    all_users = []
    winner = None
    error = None
    tmp_path = session.get('csv_path')
    if tmp_path and os.path.exists(tmp_path):
        try:
            df = pd.read_csv(tmp_path)
            all_users = df.values.tolist()
        except Exception as e:
            error = f"Помилка при зчитуванні з файлу: {e}"

    if request.method == 'POST':
        if 'clear' in request.form:
            time.sleep(3)
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)
            session.pop('csv_path', None)
            return render_template('index.html', users=[], winner=None)

        video_url = request.form['video_url']
        no_duplicates = 'no_duplicates' in request.form
        if 'get_comments' in request.form:
            try:
                users = get_comments(video_url)
                if no_duplicates:
                    seen = set()
                    users = [u for u in all_users if u[1] not in seen and not seen.add(u[1])]
                df = pd.DataFrame(users, columns=['comment_text', 'user_id', 'nickname', 'profile_url'])
                tmp_filename = f"/tmp/{uuid.uuid4().hex}.csv"
                df.to_csv(tmp_filename, index=False)
                session['csv_path'] = tmp_filename
                all_users = users
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