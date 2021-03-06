#!/usr/bin/env python

from Tkinter import *
import tkMessageBox
import threading
import stockTracker

top = Tk()

l1 = Label(top, text="Phone Number:")
l1.pack(fill=X)
e1 = Entry(top, bd=5)
e1.pack(fill=X)
e1.focus()

l2 = Label(top, text="Stocks:")
l2.pack(fill=X)
e2 = Entry(top, bd=5)
e2.pack(fill=X)

l3 = Label(top, text="percent:")
l3.pack(fill=X)
e3 = Entry(top, bd=5)
e3.pack(fill=X)

def onClose():
    stockTracker.stop()
    top.destroy()

def callback_run():
    number = e1.get()
    stocks = e2.get()
    percent = e3.get()

    data = ['stockTracker','-s',stocks,'-n',number,'-p',percent]
    worker = getattr(stockTracker, 'main')

    t = threading.Thread(target=worker, args=[data])
    t.start()

    # grey out 'Run' button
    b_run.config(state=DISABLED)

def callback_stop():
    stockTracker.stop()
    b_run.config(state=NORMAL)

b_run = Button(top, text="Run", command=callback_run)
b_run.pack()
b_stop = Button(top, text="Stop", command=callback_stop)
b_stop.pack()

top.protocol("WM_DELETE_WINDOW", onClose)
top.mainloop()
