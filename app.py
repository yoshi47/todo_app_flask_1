from flask import Flask, request,redirect, url_for, Response,render_template
from db import conn_f
from datetime import datetime as dt

date = dt.now().strftime('%Y:%m:%d %H:%I:%S')

app = Flask(__name__)


def get_all_tasks():
    conn = conn_f()
    cursor = conn.cursor()
    sql = 'select task_id, task_content, done_flag, created_at from todo where done_flag = 0;'
    cursor.execute(sql)
    tasks = cursor.fetchall()

    cursor.close()
    conn.close()
    return tasks


def get_all_done_tasks():
    conn = conn_f()
    cursor = conn.cursor()
    sql = 'select task_id, task_content, done_flag, created_at from todo where done_flag = 1;'
    cursor.execute(sql)
    tasks = cursor.fetchall()

    cursor.close()
    conn.close()
    return tasks


@app.route('/', methods=['GET'])
def index():
    tasks = get_all_tasks()
    done_tasks = get_all_done_tasks()
    return render_template('index.html', tasks=list(tasks), done_tasks=list(done_tasks))


@app.route('/', methods=['GET', 'POST'])
def add():
    conn = conn_f()
    cursor = conn.cursor()
    sql = 'insert into todo(task_content, done_flag, created_at) values("{0}", {1}, "{2}");'.format(
                                            request.form['content'],
                                            0,
                                            date
                                        )
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

    tasks = get_all_tasks()
    done_tasks = get_all_done_tasks()
    return render_template('index.html', tasks=list(tasks), done_tasks=list(done_tasks))


@app.route('/done', methods=['POST'])
def done():
    conn = conn_f()
    cursor = conn.cursor()
    sql = 'UPDATE todo SET done_flag=1 where task_id={0};'.format(
                                                                request.form['task_id']
    )
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('index'))


@app.route('/update', methods=['POST'])
def update():
    conn = conn_f()
    cursor = conn.cursor()
    sql = 'UPDATE todo SET task_content="{0}" where task_id={1};'.format(
                                                                        request.form['content'],
                                                                        request.form['task_id']
    )
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()
    tasks = get_all_tasks()
    done_tasks = get_all_done_tasks()
    return render_template('index.html', tasks=list(tasks), done_tasks=list(done_tasks))


if __name__ == '__main__':
    app.run(port=5000)
