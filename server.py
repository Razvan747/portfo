from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)
print(__name__)  # Afișează "__main__" dacă scriptul rulează direct

# Ruta principală - încarcă pagina index.html
@app.route("/")
def my_home():
    return render_template("index.html")

# Ruta dinamică pentru alte pagini HTML
@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)

# Funcție pentru scrierea în fișier text
def write_to_file(data):
    try:
        with open("database.txt", mode="a") as file:
            email = data.get("email", "")
            subject = data.get("subject", "")
            message = data.get("message", "")
            file.write(f"{email}, {subject}, {message}\n")
        print("Scriere reușită în database.txt!")
    except Exception as e:
        print(f"Eroare la scrierea în database.txt: {e}")

# Funcție pentru scrierea în CSV
def write_to_csv(data):
    try:
        with open("database.csv", mode="a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([data.get("email", ""), data.get("subject", ""), data.get("message", "")])
        print("Scriere reușită în database.csv!")  # Confirmare vizuală
    except Exception as e:
        print(f"Eroare la scrierea în database.csv: {e}")

# Ruta pentru procesarea formularului
@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()  # Convertim datele într-un dicționar
            print("Date primite:", data)  # Afișează datele în consolă pentru debugging

            write_to_file(data)  # Scrie în database.txt
            write_to_csv(data)   # Scrie în database.csv

            return redirect('/thankyou.html')  # Redirecționează la pagina de mulțumire
        except Exception as e:
            print(f"Eroare la procesarea formularului: {e}")
            return 'Eroare! Încearcă din nou.'
    else:
        return 'Ceva nu a funcționat. Încearcă din nou!'

# Rulează aplicația Flask
if __name__ == "__main__":
    app.run(debug=True)
