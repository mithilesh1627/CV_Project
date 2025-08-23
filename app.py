from flask import Flask, render_template
import os
from routes import routes  # Import the blueprint

app = Flask(__name__)
app.config['RECAPTCHA_SITE_KEY'] = os.getenv('RECAPTCHA_SITE_KEY')

# Register the blueprint
app.register_blueprint(routes)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/academic_technical')
def academic():
    return render_template("academic_technical.html", title="Academic & Technical")

@app.route('/projects_certifications')
def projects():
    return render_template("projects_certifications.html", title="Projects & Certifications")

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

