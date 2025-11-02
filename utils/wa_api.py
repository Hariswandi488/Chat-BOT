import requests
import config
from app import app
from handler import Money

COMMANDS = {
    "/tabung" : "tambah",
    "/simpan" : "tambah",
    "/ambil" : "kurang",
    "/pakai" : "kurang",
    "/cek" : "cek"
}

@app.route("/webhook", methods=["POST"])
def send_message(to, message):
    url = f"https://graph.facebook.com/v22.0/{config.phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {config.whatapps_token}",
        "Content-Type": "application/json"
    }
    data = {
    "messaging_product": "whatsapp",
    "to": to,
    "type": "text",
    "text": {
        "body": message
        }
    }

    r = requests.post(url, headers=headers, json=data)
    print("Status Balas", r.status_code, r.text)

def Prosess_Command(to, message):
    split_text = message.split()
    cmd = split_text[0].lower()
    amount = int(split_text[1])

    if not cmd.startswith("/"):
        send_message(to, f"Pesan Mu Tersampaikan\n\nPesan Mu: {message}")
        return
    
    actions = COMMANDS.get(cmd)
    if not actions:
        send_message(to, f"Perintah Tidak Valid\n\nMungkin Kamu Typo Atau Perintah Tersebut Tidak Tersedia")
        return
    
    if actions == "tambah":
        print(amount)
        Money.add_money(to, amount)