import requests
import config
from app import app
from app import storage
from handler import Money

COMMANDS = {
    "/tabung" : "tambah",
    "/simpan" : "tambah",
    "/ambil" : "kurang",
    "/pakai" : "kurang",
    "/cek" : "cek",
    "/c" : "cek",
    "/histori" : "histori",
    "/history" : "histori",
    "/storage" : "storage",
    "/db" : "storage"
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
    cmd, _, _ = prosess_chat(message)

    if not cmd.startswith("/"):
        send_message(to, f"Pesan Mu Tersampaikan\n\nPesan Mu: {message}")
        return
    
    actions = COMMANDS.get(cmd)
    if not actions:
        send_message(to, f"Perintah Tidak Valid\n\nMungkin Kamu Typo Atau Perintah Tersebut Tidak Tersedia")
        return
    
    if actions == "tambah":
        _, amount, alasan = prosess_chat(message)
        Money.add_money(to, amount, alasan)
    
    elif actions == "kurang":
        _, amount, alasan = prosess_chat(message)
        Money.take_money(to, amount, alasan)

    elif actions == "histori":
        Money.cek_money_history(to, message)
    
    elif actions == "storage":
        split = message.split()
        storages = split[1]
        storage(to, storages)


def prosess_chat(message):
    split_text = message.split()
    cmd = split_text[0].lower()
    if len(split_text) > 1:
        if isinstance(split_text[1], int):
            amount = int(split_text[1]) if len(split_text) > 1 else 0
        else:
            amount = int(split_text[1]) if len(split_text) > 1 else "not amout"
    else:
        amount = "unknown"

    alasan = " ".join(split_text[2:]) if len(split_text) > 2 else "Tanpa Alasan"
    return cmd, amount, alasan