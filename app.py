from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)

cnn = sqlite3.connect('db.sqlite3')
cour = cnn.cursor()
students = cour.execute("""SELECT * FROM students LIMIT 20""")

std_list = []
for row in students:
    std_list.append({
        'id': row[0] + len(std_list),
        'name': row[1],
        'gender': row[2],
        'phone': row[3],
        'email': row[4],
        'address': row[5]
    })
cnn.close()


@app.route('/')
def index():  # put application's code here
    return render_template("master.html")


@app.route('/dashboard')
def dashboard():  # put application's code here
    return render_template("dashboard.html")


@app.route('/users')
def users():  # put application's code here
    return render_template("users.html", data=std_list)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, gender, phone, email, address) VALUES (?, ?, ?, ?, ?)",
                       (name, gender, phone, email, address))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/update_user')
def update_user():
    module = 'user'
    id = request.args.get('id', default=1, type=int)
    current_user = filter(lambda x: x['id'] == id, std_list)
    current_user = list(current_user)
    name = current_user[0]['name']

    return render_template('update_user.html', module=module, user=current_user[0])


if __name__ == '__main__':
    app.run()
