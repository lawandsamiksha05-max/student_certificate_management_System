from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello"

print("Before")
app.run(host="127.0.0.1", port=8000)
print("After")