cd /home/adminvmss
cat > app.py << 'EOF'
from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

words = ["azure", "terraform", "python", "cloud", "network"]
word = random.choice(words)
guessed = []
attempts = 6

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Hangman</title>
</head>
<body style="text-align:center; font-family:Arial;">
<h1>Hangman Game</h1>

<p>Word:
{% for letter in word %}
    {% if letter in guessed %}
        {{letter}}
    {% else %}
        _
    {% endif %}
{% endfor %}
</p>

<p>Attempts left: {{attempts}}</p>

<form method="POST">
<input name="letter" maxlength="1" required>
<button type="submit">Guess</button>
</form>

{% if message %}
<p>{{message}}</p>
{% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    global guessed, attempts, word
    message = ""

    if request.method == "POST":
        letter = request.form["letter"]

        if letter not in guessed:
            guessed.append(letter)
            if letter not in word:
                attempts -= 1

        if all(l in guessed for l in word):
            message = "You Won!"
        elif attempts <= 0:
            message = f"You Lost! Word was {word}"

    return render_template_string(HTML, word=word, guessed=guessed, attempts=attempts, message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
EOF
