from flask import Flask, request, jsonify
import config, os, sqlite3
from utils import wa_api

#Path System
path_app = os.path.dirname(os.path.abspath(__file__))
path_data = os.path.join(path_app, "data")
money_data = os.path.join(path_data, "Money.db")

#Connect db File 
Money_db = sqlite3.connect(money_data, check_same_thread=False)
cur_money_db = Money_db.cursor()

#Setup Data
def Setup_data():
    global Money_db, cur_money_db
    cur_money_db.execute("""CREATE TABLE IF NOT EXISTS money(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amout INTEGER,
        total INTEGER,
        alasan TEXT
    )
    """)

    Money_db.commit()

app = Flask(__name__)
print("app terbuat")
#Get Webhook
@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == config.verify_token:
        print("WEBHOOK Verified")
        wa_api.send_message(config.wa_phone_number_H, f"Webhook Terverifikasi")
        return challenge, 200
    else:
        return "Verified Failed", 403
    

#Terima pesan User
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print(f"Data Masuk {data}")

    if data and data.get("entry"):
        try:
            msg = data["entry"][0]["changes"][0]["value"]["messages"][0]
            sender = msg["from"]
            text = msg["text"]["body"]
            print(f"Pesan dari {sender} : {text}")

            wa_api.Prosess_Command(sender, text)

        except Exception as e:
            print("Error parsing pesan", e)

    return jsonify({"status" : "ok"}), 200

if __name__ == "__main__":
    Setup_data()
    app.run(port=5000)