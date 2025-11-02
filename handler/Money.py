import app
from utils import formater, wa_api

Total_Money_S: int = 0

def add_money(to, amount: int):
    global Total_Money_S
    last_id = app.cur_money_db.lastrowid
    app.cur_money_db.execute("SELECT total FROM money WHERE id = ?", (last_id,))
    if app.cur_money_db.fetchone():
        Total_Money_S = app.cur_money_db.fetchone()
        print(f"data money {Total_Money_S}")
        Total_Money_S = 10000
    if Total_Money_S:
        Total = Total_Money_S + amount
        total_F, total_SF, amount_F = formater.formatter(Total_Money_S, amount, Total)
    wa_api.send_message(to, f"Data Berhasil Di Eksekusi\n\nKamu Menyimpan Uang Dari:\n*Rp {total_SF}* + *Rp {amount_F}*\n\n Uang Mu Sekarang Jadi:\n*Rp {total_F}*")