from flask import Flask, render_template


# port = int(os.environ.get('PORT', 5000))

app = Flask(__name__)
# app.config["DEBUG"] = True


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
