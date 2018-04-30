from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SelectField, BooleanField, SubmitField
from wtforms.validators import Required
from generator import *

app = Flask(__name__)
Bootstrap(app)
app.secret_key = "xkcd"


class Criteria(FlaskForm):
    min_len = SelectField("Minimum Password Length", choices=[
                          ("15", "15"), ("16", "16"), ("17", "17"), ("18", "18")], default="15")
    max_len = SelectField("Maximum Password Length", choices=[
                          ("27", "27"), ("28", "28"), ("29", "29"), ("30", "30")], default="30")
    min_word_len = SelectField("Minimum Word Length", choices=[
                               ("3", "3"), ("4", "4"), ("5", "5"), ("6", "6")], default="3")
    max_word_len = SelectField("Maximum Word Length", choices=[
                               ("7", "7"), ("8", "8"), ("9", "9"), ("10", "10")], default="10")
    language = SelectField("Language", choices=[("brazilian.txt", "Brazilian"), ("danish.txt", "Danish"), ("dutch.txt", "Dutch"), ("english.txt", "English"), ("french.txt", "French"), (
        "german.txt", "German"), ("irish.txt", "Irish"), ("italian.txt", "Italian"), ("portuguese.txt", "Portuguese"), ("spanish.txt", "Spanish"), ("swedish.txt", "Swedish")], default="english.txt")
    easy_typing = BooleanField("Easy Typing", default=True)
    num_sub = BooleanField("Number Substitutions")
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def index():
    form = Criteria()
    if form.validate_on_submit():
        min_len = int(form.min_len.data)
        max_len = int(form.max_len.data)
        min_word_len = int(form.min_word_len.data)
        max_word_len = int(form.max_word_len.data)
        language = str(form.language.data)
        easy_typing = bool(form.easy_typing.data)
        num_sub = bool(form.num_sub.data)

        words = read("static/languages/"+language)

        if easy_typing:
            words = easy(words)

        passwords = generate(words, min_len, max_len,
                             min_word_len,  max_word_len)

        if num_sub:
            passwords = numbers(passwords)

        return render_template("generated.html", passwords=passwords)

    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
