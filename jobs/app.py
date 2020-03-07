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
        connection = sqlite3.connect(PATH)
        g._connection = sqlite3.connect(PATH)
    
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
    return render_template('index.html')