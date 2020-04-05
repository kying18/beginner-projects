from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/index/")
def index():
    return render_template('home.html')

# to run the application
# export FLASK_APP=web.py
# flask run

if __name__ == "__main__":
    app.run(debug=True)
