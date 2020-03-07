from flask import Flask, render_template, g
import sqlite3

# Path to database
PATH = "db/jobs.sqlite"

# Create an instance
app = Flask(__name__)


# Global Database Attribute
def open_connection():
    connection = getattr(g, '_connection', None)
    if connection is None:
        connection = g._connection = sqlite3.connect(PATH)
    
    # All rows returned from the database will be named tuples
    connection.row_factory = sqlite3.Row
    return connection


# Query Database Function
def execute_sql(sql , values=(), commit=False, single=False):
    connection = open_connection()
    cursor = connection.execute(sql, values)

    if commit:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()
    cursor.close()
    return results


# Close the connection
@app.teardown_appcontext
def close_connection(exception):
    connection = getattr(g, '_connection', None)
    if connection is not None:
        connection.close()


@app.route('/')
@app.route('/jobs')
def jobs():
    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id')
    return render_template('index.html', jobs=jobs)


@app.route('/job/<job_id>')
def job(job_id):
    job = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id WHERE job.id = ?', [job_id], single=True)
    return render_template('job.html', job=job)


@app.route('/employer/<employer_id>')
def employer(employer_id):
    employer = execute_sql('SELECT * FROM employer WHERE id=?', [employer_id], single=True)
    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary FROM job JOIN employer ON employer.id = job.employer_id WHERE employer.id = ?', [employer_id])
    reviews = execute_sql('SELECT review, rating, title, date, status FROM review JOIN employer ON employer.id = review.employer_id WHERE employer.id = ?', [employer_id])
    return render_template('employer.html', employer=employer, jobs=jobs, reviews=reviews)