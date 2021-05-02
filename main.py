import sqlite3 
import os
from prettytable import PrettyTable
import stringenc
from getpass import getpass

f = os.path.exists("./data.db")
conn = sqlite3.connect("data.db")
cur = conn.cursor()
enc = stringenc.stringenc()


if not f:
    print("Setting up...")
    cur.execute(""" CREATE TABLE passwords (
        id INTEGER PRIMARY KEY,
        url TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
        )""")
    while True:
        pwd = getpass("Enter new Master password: ")
        repwd = getpass("Re-enter Master password: ")
        if(pwd==repwd):
            cur.execute("insert into passwords(url,username,password) values(?,?,?)",["none","none",enc.encrypted(pwd)])
            conn.commit()
            break
        
    conn.commit()

def showCmds():
    print("1. Add password")
    print("2. Show password")
    print("3. Update password")
    print("4. Delete password")
    print("5. Exit")

def checkPwd():
    while True:
        pwd = getpass("Master Password: ")
        cur.execute("select * from passwords where id = ?",[1])
        if pwd ==enc.decrypted(cur.fetchall()[0][-1]):
            break 

def byId(typeCmd):
    userId = input("Enter the id: ")
    checkPwd()
    if typeCmd == 2:
        table = PrettyTable(["ID","URL","USERNAME/MAIL","PASSWORD"])
        cur.execute("select * from passwords where id = ?",[userId])
        for i in cur.fetchall():
            i = list(i)
            i[-1] = enc.decrypted(i[-1])
            table.add_row(i)
        print(table)         
    elif typeCmd == 3:
        while True:
            updatePwd = getpass("Enter new password: ")
            updateRepwd = getpass("Re-enter new password: ")
            if(updatePwd == updateRepwd):
                break
            else:
                print("Password does not match. Try Again!")
        cur.execute("update passwords set password=? where id=?",[enc.encrypted(updatePwd),userId])
        conn.commit()
        print("Password Updated Sucessfully.")
    else:
        cur.execute("delete from passwords where id = ?",[userId])
        conn.commit()
        print("Deleted Sucessfully.")

def byMail(typeCmd):
    searchUrl = input("Enter the url: ")
    searchMail = input("Enter the mail/username: ")
    checkPwd()
    if typeCmd == 2:
        table = PrettyTable(["ID","URL","USERNAME/MAIL","PASSWORD"])
        cur.execute("select * from passwords where url = ? AND username = ?",[searchUrl,searchMail])
        for i in cur.fetchall():
            i = list(i)
            i[-1] = enc.decrypted(i[-1])
            table.add_row(i)
        print(table)         
    elif typeCmd == 3:
        while True:
            updatePwd = getpass("Enter new password: ")
            repwd = getpass("Re-enter new password: ")
            if updatePwd == repwd:
                break
            else:
                print("Password does not match. Try Again!")
        cur.execute("update passwords set password=? where url = ? AND username = ?",[enc.encrypted(updatePwd),searchUrl,searchMail])
        conn.commit()
        print("Password Updated Sucessfully.")
    else:
        cur.execute("delete from passwords where url = ? AND username = ?",[searchUrl,searchMail])
        conn.commit()
        print("Deleted Sucessfully.")
        

def addPwd():
    url = input("Enter the url: ")
    userName = input("Enter the username/mail: ")
    while True:
        pwd = getpass("Enter the password: ")
        repwd = getpass("Re-enter the password: ")
        if pwd == repwd:
            cur.execute("insert into passwords(url,username,password) values(?,?,?)",[url,userName,enc.encrypted(pwd)])
            conn.commit()
            print("Password added.")
            break


def restPwd(temp):
    while True:
        print("1.Show by id")
        print("2.Show by url and username/mail")
        choiceFn = int(input("Enter the choice: "))
        if choiceFn in [1,2]:
            break
    byId(temp) if choiceFn == 1 else byMail(temp) 

showCmds()
while True:
    choice = int(input())
    if(choice==1):
        addPwd()
    elif(choice==2):
        restPwd(choice)
    elif(choice==3):
        restPwd(choice)
    elif(choice==4):
        restPwd(choice)
    elif(choice==5):
        break
    else:
        showCmds()

conn.close()
