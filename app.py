from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/users')
def users():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('users.html', data=students)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        conn = get_db_connection()
        conn.execute("INSERT INTO students (name, gender, phone, email, address) VALUES (?, ?, ?, ?, ?)",
                     (name, gender, phone, email, address))
        conn.commit()
        conn.close()
        return redirect(url_for('users'))
    return render_template('create.html')


@app.route('/update_user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        conn.execute('UPDATE students SET name = ?, gender = ?, phone = ?, email = ?, address = ? WHERE id = ?',
                     (name, gender, phone, email, address, id))
        conn.commit()
        conn.close()
        return redirect(url_for('users'))

    conn.close()
    return render_template('update_user.html', student=student)


@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('users'))


@app.route('/view_user/<int:id>')
def view_user(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('view.html', student=student)


if __name__ == '__main__':
    app.run(debug=True)
