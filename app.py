from flask import render_template,request,Flask

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/academic_technical')
def academic():
    return render_template("academic_technical.html", title="Academic & Technical")

@app.route('/projects_certifications')
def projects():
    return render_template("projects_certifications.html",title="Projects & Certifications")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)