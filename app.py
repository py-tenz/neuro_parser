import os
import time
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for, g

from classifier import analyze_comments
import youtube_parser as ytp
import vk_parser as vkp

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', os.urandom(24))


@app.context_processor
def inject_now():
    return {'now': datetime.now()}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    source = request.form.get('source', 'youtube')
    query  = request.form.get('query', '').strip()

    comments = []
    try:
        if source == 'youtube':
            tags = query.split()
            h1 = tags[0] if tags else '#python'
            h2 = tags[1] if len(tags) > 1 else ''
            ytp.post_vids(h1, h2)
            time.sleep(2)
            ytp.get_all_yt_video_comments(ytp.get_all_video_ids())
            time.sleep(2)
            comments = ytp.get_comments_as_list()
        else:
            domain = query or 'wildberries'
            vkp.save_data_to_json(vkp.get_all_posts(domain), 'data/vk_posts.json')
            owner_id = vkp.get_id('data/vk_posts.json')
            vkp.get_all_comments(domain, owner_id)
            comments = vkp.get_comments_as_list()
    except Exception as exc:
        return render_template('index.html', error=str(exc))

    if not comments:
        return render_template('index.html', error='Комментарии не найдены. Попробуйте другой запрос.')

    stats = analyze_comments(comments)
    per_comment = stats.pop('per_comment')

    stats['source'] = 'YouTube' if source == 'youtube' else 'VK'
    stats['query']  = query
    stats['date']   = datetime.now().strftime('%d.%m.%Y в %H:%M')

    session['results']  = stats
    session['comments'] = per_comment[:100]

    return redirect(url_for('results'))


@app.route('/results')
def results():
    data     = session.get('results')
    comments = session.get('comments', [])
    if not data:
        return redirect(url_for('index'))
    return render_template('results.html', data=data, comments=comments)


@app.route('/report')
def report():
    data     = session.get('results')
    comments = session.get('comments', [])
    if not data:
        return redirect(url_for('index'))
    return render_template('report.html', data=data, comments=comments)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
