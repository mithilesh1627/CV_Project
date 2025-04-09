from flask import render_template,request,Flask

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/academic&technical')
def academic():
    return render_template("academic.html", title="Academic & Technical")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/projects')
def projects():
    return render_template("projects.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=True)