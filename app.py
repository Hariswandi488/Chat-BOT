from flask import Flask, request, jsonify
import config, os, sqlite3
from utils import wa_api

STORAGE = {
    "money" : "Money.db",
    "uang" : "Money.db",
    "test" : "Test.db",
    "test" : "Test.db"
}

#Path System
path_app = os.path.dirname(os.path.abspath(__file__))
path_data = os.path.join(path_app, "data")
money_data = os.path.join(path_data, "Money.db")

#Connect db File 
storage_db  = sqlite3.connect(money_data, check_same_thread=False)
cur_storage_db = storage_db.cursor()

def storage(to, storages):
    storage_db.close()

    storage = STORAGE.get(storages)
    if not storage:
        wa_api.send_message(to, f"Data Storage Tidak Valid/Tidak Ada")
        return
    
    storage_path = os.path.join(path_data, storage)
    storage_db = sqlite3.connect(storage_path, check_same_thread=False)
    cur_storage_db = storage_db.cursor()
    Setup_data()
    wa_api.send_message(to, f"Berhasil ganti ke data storage {storage} ")



#Setup Data
def Setup_data():
    global storage_db, cur_storage_db
    cur_storage_db.execute("""CREATE TABLE IF NOT EXISTS money(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        before INTEGER,
        amount INTEGER,
        total INTEGER,
        alasan TEXT,
        tanggal TEXT
    )
    """)

    storage_db.commit()

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)