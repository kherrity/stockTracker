#!/usr/bin/env python

from Tkinter import *
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

    print "Running..."
    #text = Text(top, bd=5)
    #text.insert(INSERT, "Running...")
    #text.pack()

def callback_stop():
    #text = Text(top, bd=5)
    #text.insert(INSERT, "Stopped...")
    #text.pack()

    stockTracker.stop()
    b_run.config(state=NORMAL)

    print "Stopped..."

b_run = Button(top, text="Run", command=callback_run)
b_run.pack()
b_stop = Button(top, text="Stop", command=callback_stop)
b_stop.pack()

top.mainloop()
top.quit()
