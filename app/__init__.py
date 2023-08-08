from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'app/database.db'

def get_db():
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        question = request.form['question']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correct_option = request.form['correct_option']

        db = get_db()
        db.execute('INSERT INTO questions (question, option1, option2, option3, option4, correct_option) VALUES (?, ?, ?, ?, ?, ?)',
                   (question, option1, option2, option3, option4, correct_option))
        db.commit()
        return redirect(url_for('view_questions'))

    return render_template('add_question.html')

@app.route('/view')
def view_questions():
    db = get_db()
    questions = db.execute('SELECT * FROM questions').fetchall()
    return render_template('view_questions.html', questions=questions)

@app.route('/edit/<int:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    db = get_db()
    question = db.execute('SELECT * FROM questions WHERE id = ?', (question_id,)).fetchone()

    if request.method == 'POST':
        new_question = request.form['question']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correct_option = request.form['correct_option']

        db.execute('UPDATE questions SET question = ?, option1 = ?, option2 = ?, option3 = ?, option4 = ?, correct_option = ? WHERE id = ?',
                   (new_question, option1, option2, option3, option4, correct_option, question_id))
        db.commit()
        return redirect(url_for('view_questions'))

    return render_template('edit_question.html', question=question)


if __name__ == '__main__':
    app.run(debug=True)
