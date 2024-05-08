import csv
import sqlite3

fname1 = "users_1.csv"
fname2 = "log_1.csv"
users_array = []
log_array = []

with open(fname1, encoding = "koi8_r") as fn:
    for string in csv.reader(fn):
        user_id, email, geo = string[0].split("\t")
        if user_id.count("_") > 0:
            user, id = user_id.split("_")
            if user == "User" and id.isdigit() == True:
                users_array.append([user_id, email, geo])

with open(fname2) as fn:
    bet = 0
    win = 0
    for user_id, timein, bet, win in csv.reader(fn):
        if user_id[0] != "#":
            user_id = list(user_id.split())[-1]
            timein = timein.replace("[", "")
            log_array.append([user_id, timein, bet, win])

with sqlite3.connect("bets.s3db") as con:
    cur = con.cursor()
    for user_id, email, geo in users_array:
        cur.execute('INSERT INTO users (user_id, email, geo) VALUES(?, ?, ?)',
            (user_id, email, geo))

    for user_id, timein, bet, win in log_array:
        cur.execute('INSERT INTO log (bet, win, user_id, time) VALUES (?, ?, ?, ?)',
             (bet, win, user_id, timein))
        
    con.commit()
    con.close()
