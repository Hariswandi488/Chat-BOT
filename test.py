import datetime, pytz

HARI = {
    "Monday" : "Hari Senin",
    "Tuesday" : "Hari Selasa", 
    "Wednesday" : "Hari Rabu",
    "Thursday" : "Hari Kamis",
    "Friday" : "Hari Jum'at",
    "Saturday" : "Hari Sabtu",
    "Sunday" : "Hari Minggu"
}


zona = pytz.timezone("Asia/Jakarta")

data_now_local = datetime.datetime.now(zona)
local_now_f = data_now_local.strftime("Tanggal %d-%m-%Y || Jam : %H:%M:%S")
days= data_now_local.strftime("%A")
hari = HARI.get(days)
tanggal = f"{hari} || {local_now_f}"
print(tanggal)
