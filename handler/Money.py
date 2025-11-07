import app
import datetime, pytz
from utils import formater, wa_api

zona = pytz.timezone("Asia/Jakarta")

HARI = {
    "Monday" : "Hari Senin",
    "Tuesday" : "Hari Selasa", 
    "Wednesday" : "Hari Rabu",
    "Thursday" : "Hari Kamis",
    "Friday" : "Hari Jum'at",
    "Saturday" : "Hari Sabtu",
    "Sunday" : "Hari Minggu"
}

SORT = {
    "terbaru" : "DESC",
    "desc" : "DESC",
    "baru" : "DESC",
    "lama" : "ASC",
    "asc" : "ASC",
    "terlama" : "ASC" 
}

ORDER = {
    "tanggal" : "tanggal",
    "waktu" : "tanggal",
    "id" : "id",
    "total" : "total",
    "penambahan" : "amount",
    "amount" : "amount"
}

def get_date():
    data_now_local = datetime.datetime.now(zona)
    local_now_f = data_now_local.strftime("Tanggal %d-%m-%Y || Jam : %H:%M:%S")
    days= data_now_local.strftime("%A")
    hari = HARI.get(days)
    tanggal = f"{hari} || {local_now_f}"
    return tanggal



def add_money(to, amount: int, alasan: str):
    tanggal = get_date()
    app.cur_storage_db.execute("SELECT total FROM money ORDER BY id DESC lIMIT 1")
    row = app.cur_storage_db.fetchone()
    total_S = row[0] if row else 0
    total = total_S + amount
    app.cur_storage_db.execute("INSERT INTO money (before, amount, total, alasan, tanggal) VALUES (?, ?, ?, ?, ?)", (total_S, amount, total, alasan, tanggal,))
    app.storage_db.commit()
    total_SF, amount_F, total_F = formater.formatter(total_S, amount, total)
    pesan = (
        f"*Data Berhasil Di Eksekusi!!*\n\n"
        f"Kamu Menyimpan Uang Dari :\n"
        f"*Rp {total_SF}* + *Rp {amount_F}*\n\n"
        f"Uang Mu Sekarang Jadi :\n"
        f"*Rp {total_F}*\n\n"
        f"Alasan :\n"
        f"*{alasan}*"
    )
    wa_api.send_message(to, pesan)


def take_money(to, amount: int, alasan: str):
    tanggal = get_date()
    app.cur_storage_db.execute("SELECT total FROM money ORDER BY id DESC LIMIT 1")
    row = app.cur_storage_db.fetchone()
    total_S = row[0] if row else 0
    total = total_S + (-amount)
    app.cur_storage_db.execute("INSERT INTO money (before, amount, total, , tanggal) VALUES (?, ?, ?)", (total_S, amount, total, alasan, tanggal))
    app.storage_db.commit()
    total_SF, amount_F, total_F = formater.formatter(total_S, amount, total)
    pesan = (
        f"*Data Berhasil Di Eksekusi!!*\n\n"
        f"Kamu Mengambil Uang Dari :\n"
        f"*Rp {total_SF}* + *Rp {amount_F}*\n\n"
        f"Uang Mu Sekarang Jadi :\n"
        f"*Rp {total_F}*\n\n"
        f"Alasan :\n"
        f"*{alasan}*"
    )
    wa_api.send_message(to, pesan)


def cek_money_history(to, message):
    split = message.split()
    limit = int(split[1]) if len(split) > 1 else 5
    order_t = split[2] if len(split) > 2 else "unknown"
    sort_t = split[3] if len(split) > 3 else "unknown"
    order_r, sort_r = False, False

    order = ORDER.get(order_t)
    sort = SORT.get(sort_t)

    if not order:
        order = "id"
        order_r = True
        
    
    if not sort:
        sort = "DESC"
        sort_r = True

    query = f"SELECT before, amount, total, alasan, tanggal FROM money ORDER BY {order} {sort} LIMIT ?"
    app.cur_storage_db.execute(query, (limit,))
    rows = app.cur_storage_db.fetchall()

    list_pesan = []
    if order_r and sort_r:
        list_pesan.append(
            f"==============================\n"
            f"Data Sortir dan order pengurutan Tidak Valid !!\n"
            f"AutoReset Ke Default SORT(DESC) ORDER(id) "
            f"=============================="
            )
    elif not order_r and sort_r :
        list_pesan.append(
            f"==============================\n"
            f"Data Sortir Tidak Valid !!\n"
            f"AutoReset Ke Default SORT(DESC)"
            f"=============================="
            )
    elif order_r and not sort_r:
        list_pesan.append(
            f"==============================\n"
            f"Data Order Pengurutan Tidak Valid !!\n"
            f"AutoReset Ke Default ORDER(id)"
            f"=============================="
        )

    if not rows:
        list_pesan.append(
            f"Tidak Ada Data Menyimpan Atau Mengambil Uang"
        )
    else:
        for i, (before, amount, total, alasan, tanggal) in enumerate(rows, start=1):
            total_SF, amount_F, total_F = formater.formatter(before, amount, total)
            print(f"temp var {total_SF}")

            list_pesan.append(
                f"{i}. *Rp {total_SF}* + *Rp {amount_F}* » *Rp {total_F}*\n{alasan} \n {tanggal}"
            )

    pesan = "5 Data Terakhir Menyimpan/Mengambil Uang \n\n" + "\n\n".join(list_pesan)

    wa_api.send_message(to, pesan)