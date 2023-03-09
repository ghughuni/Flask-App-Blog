from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username, count_like, count_unlike'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id, count_like, count_unlike)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, body, g.user['id'], 0, 0)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, count_like, count_unlike'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
            abort(403)

    return post

def get_post_rate(lu_id, id):
    post_rate = get_db().execute(
            'SELECT r.author_id, r.post_id, liked, unliked'
            ' FROM post p JOIN rate r ON p.id = r.post_id'
            ' WHERE r.author_id = ? and r.post_id=?',
            (lu_id, id)
        ).fetchone()
    
    return post_rate

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

@bp.route('/like_unlike/<int:id>/<int:lu>', methods=('GET', 'POST'))
@login_required
def like_unlike(id,lu):
    db = get_db()
    post = get_post(id, check_author=False)
    lu_id=g.user['id']
    post_rate=get_post_rate(lu_id, id)
    # liked
    if lu==1:
        try:
            if post_rate['post_id']==post_rate['liked']:
                pass
            elif post_rate['post_id']==post_rate['unliked'] and post_rate['liked']==0:
                count_like=post['count_like']+1
                count_unlike=post['count_unlike']-1
                db = get_db()
                db.execute(
                    'UPDATE post SET count_like = ?, count_unlike = ? '
                    'WHERE id = ?',
                    (count_like, count_unlike, id)
                )
                db.commit()
                db.execute(
                    'UPDATE rate SET liked=?, unliked=?'
                    'WHERE author_id=? and post_id = ?',
                    (id, 0, g.user['id'], id)
                )
                db.commit()
        except:
            count_like=post['count_like']+1
            db.execute(
                'UPDATE post SET count_like = ?'
                ' WHERE id = ?',
                (count_like, id)
            )
            db.commit()
            db.execute(
                'INSERT INTO rate (author_id, post_id, liked, unliked)'
                ' VALUES (?, ?, ?, ?)',
                (g.user['id'], id, id, 0)
            )
            db.commit()
    # unliked
    if lu==0:
        try:
            if post_rate['post_id']==post_rate['unliked']:
                pass
            elif post_rate['post_id']==post_rate['liked'] and post_rate['unliked']==0:
                count_like=post['count_like']-1
                count_unlike=post['count_unlike']+1
                db = get_db()
                db.execute(
                    'UPDATE post SET count_like = ?, count_unlike = ? '
                    'WHERE id = ?',
                    (count_like, count_unlike, id)
                )
                db.commit()
                db.execute(
                    'UPDATE rate SET liked=?, unliked=?'
                    'WHERE author_id=? and post_id = ?',
                    (0, id, g.user['id'], id)
                )
                db.commit()
        except:
            count_unlike=post['count_unlike']+1
            db = get_db()
            db.execute(
                'UPDATE post SET count_unlike = ? '
                ' WHERE id = ?',
                (count_unlike,id)
            )
            db.commit()
            db.execute(
                'INSERT INTO rate (author_id, post_id, liked, unliked)'
                ' VALUES (?, ?, ?, ?)',
                (g.user['id'], id, 0, id)
            )
            db.commit()          
    return render_template('blog/index.html', post=post, post_rate=post_rate)
    
