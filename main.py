from flask import Flask, redirect, render_template, url_for, request
from tika import parser # pip install tika
import docx
import pytesseract
from PIL import Image


blacklist = [
    "small"
]

app = Flask(__name__)

#raw = parser.from_file('https://firebasestorage.googleapis.com/v0/b/resell-page.appspot.com/o/my-cv.pdf?alt=media&token=9cfe75f4-3c72-4135-9086-65dda81b582f')
#print(raw['content'])

def checkDocument(fileUrl):
    if ".pfd" in fileUrl:
        raw = parser.from_file(f"https://firebasestorage.googleapis.com/v0/b/emails-28257.appspot.com/o/proiectTic%2F{fileUrl}?alt=media&token=df275199-8a34-4bf0-8496-1b1143565bbc")
        #print(raw['content'])
        return raw["content"]
    elif ".png" or ".jpg" or ".jpeg":
        im = Image.open("sample1.png")
        pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'
        text = pytesseract.image_to_string(im, lang='eng')

        print(text)


def sepellcheckText(text):
    for word in text:
        print(word)

@app.route("/", methods=["POST", "GET"])
def home():
    if(request.method == "POST"):
        pdf_file = request.form["file"]
        return redirect(f"/rezultat?file={pdf_file}")
    else:
        return render_template("index.html")

@app.route("/rezultat")
def result():
    correctedText = ""
    bad_words = [

    ]

    pdf_file = checkDocument(request.args.get("file")).split()

    for word in blacklist:
        if word in pdf_file:
            bad_words.append(word)

    if(len(bad_words) != 0):
        return render_template("verificare.html")
    else:
        return render_template("curat.html")

if (__name__ == "__main__"):
    app.debug = True
    app.run()