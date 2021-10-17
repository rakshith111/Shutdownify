from tkinter import *
from os import system
import tkinter as tk
def submit():
    try:
        hrsms=int(hrs.get())
        minuitsms=int(minuits.get())
        secondsms=int(minuits.get())
        final=hrsms*3600+minuitsms*60+secondsms
        system(f"shutdown -s -t {final}")
    except ValueError:
        hrs.set(int(0))
        minuits.set(int(0))
        seconds.set(int(0))
    root.destroy()


root=tk.Tk()
root.title('SHUTDOWN')
root.geometry("435x70")
hrs=tk.StringVar()
minuits=tk.StringVar()
seconds=tk.StringVar()
hrs.set(int(0))
minuits.set(int(0))
seconds.set(int(0))
Hrs_label = tk.Label(root, text = 'HRS', font=('calibre',10, 'bold'))
Hrs_entry = tk.Entry(root,textvariable = hrs, font=('calibre',10,'normal'))
min_label= tk.Label(root, text = 'Min', font=('calibre',10, 'bold'))
min_entry = tk.Entry(root,textvariable = minuits, font=('calibre',10,'normal'))
sec_label = tk.Label(root, text = 'Sec', font=('calibre',10, 'bold'))
sec_entry = tk.Entry(root,textvariable = seconds, font=('calibre',10,'normal'))
sub_btn=tk.Button(root,text = 'Submit', command = submit)
Hrs_label.grid(row=0,column=0)
Hrs_entry.grid(row=1,column=0)
min_label.grid(row=0,column=1)
min_entry.grid(row=1,column=1)
sec_label.grid(row=0,column=3)
sec_entry.grid(row=1,column=3)
sub_btn.grid(row=2,sticky='e')


root.mainloop()