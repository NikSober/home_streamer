from flask import Flask, jsonify, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to HomeStreamer!"})

@app.route('/search')
def search():
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)