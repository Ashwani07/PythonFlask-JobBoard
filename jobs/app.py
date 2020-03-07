from flask import Flask, render_template

# Create an instance
app = Flask(__name__)

@app.route('/')
@app.route('/jobs')
def jobs():
    return render_template('index.html')