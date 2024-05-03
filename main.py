from data import languages, W, B
from translate_video import *
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import pytube.exceptions
import threading
import os
from ttkthemes import ThemedTk


class MyGUI:

    def __init__(self):

        root = ThemedTk(theme="black")
        root.geometry('650x300')

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N + W + E + S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        ttk.Label(mainframe, text='get translated video',
                  font=('Arial', 14)).grid(column=2, row=1)
        ttk.Label(mainframe, text='Language from:',
                  font=('Arial', 12)).grid(column=1, row=1, sticky=S)
        ttk.Label(mainframe, text='Language to:',
                  font=('Arial', 12)).grid(column=3, row=1, sticky=S)
        s = 'video speed will be changed for comfort audio listening'
        ttk.Label(mainframe, text=s).grid(column=2, row=3, sticky=W+E)

        choicesvar1 = StringVar(value=list(languages))
        self.lbox1 = Listbox(mainframe, listvariable=choicesvar1,
                             exportselection=0, height=12, width=24)
        self.lbox1.configure(background="grey", foreground='white', selectbackground='DarkGoldenrod')
        self.lbox1.selection_set(10)
        self.lbox1.grid(column=1, row=2, rowspan=6, sticky=W + N)
        s1 = ttk.Scrollbar(mainframe, orient=VERTICAL,
                           command=self.lbox1.yview)
        s1.grid(column=1, row=2, rowspan=6, sticky=E + N + S)
        self.lbox1.configure(yscrollcommand=s1.set)

        def on_entry_click(event):
            if url_entry.get() == "enter URL...":
                url_entry.delete(0, tk.END)

        def on_focus_out(event):
            if url_entry.get() == "":
                url_entry.insert(0, "enter URL...")

        self.url = StringVar()
        def_url = 'enter URL...'
        url_entry = ttk.Entry(mainframe, width=50, textvariable=self.url)
        url_entry.insert(0, def_url)
        url_entry.bind("<FocusIn>", on_entry_click)
        url_entry.bind("<FocusOut>", on_focus_out)
        url_entry.grid(column=2, row=4, sticky=S)
        self.url.trace_add("write", self.estimate_time)

        choicesvar2 = StringVar(value=list(languages))
        self.lbox2 = Listbox(mainframe, listvariable=choicesvar2,
                             exportselection=0, height=12, width=24)
        self.lbox2.configure(background="grey", foreground='white', selectbackground='DarkGoldenrod')
        self.lbox2.selection_set(52)
        self.lbox2.grid(column=3, row=2, rowspan=6, sticky=W+N)
        s2 = ttk.Scrollbar(mainframe, orient=VERTICAL,
                           command=self.lbox2.yview)
        s2.grid(column=3, row=2, rowspan=6, sticky=E+N+S)
        self.lbox2.configure(yscrollcommand=s2.set)

        self.only_audio = BooleanVar()
        ttk.Checkbutton(mainframe, text='get only translated audio',
                        variable=self.only_audio,
                        onvalue=True,
                        offvalue=False).grid(column=2, row=2, sticky=W+E)

        button = ttk.Button(mainframe, text="Go!", command=self.start)
        button.grid(column=2, row=5, sticky=W + E)

        self.estimate = IntVar()
        self.p = ttk.Progressbar(mainframe, orient=HORIZONTAL, length=200,
                                 mode='determinate')
        self.p.grid(column=2, row=6, sticky=W + E)

        self.est_text = StringVar()
        est_label = ttk.Label(mainframe, textvariable=self.est_text)
        est_label.grid(column=2, row=7, sticky=W)

        self.status_var = StringVar()
        statusbar = ttk.Label(mainframe, textvariable=self.status_var)
        statusbar.grid(column=2, row=8, sticky=W)

        self.dirname = ''
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
        root.bind("<Return>", lambda event: self.start())

        root.mainloop()

    def translate_video(self):
        lang1 = self.lbox1.get(self.lbox1.curselection())
        lang2 = self.lbox2.get(self.lbox2.curselection())

        gen = translate(self.url.get(), languages[lang1], languages[lang2], self.only_audio.get(), self.dirname)
        while True:
            try:
                self.status_var.set(next(gen))
            except StopIteration as result:
                self.p.stop()
                self.p['value'] = self.estimate.get()
                self.status_var.set(f'file destination: {self.dirname}')
                messagebox.showinfo(message=result.value)
                self.p['value'] = 0
                break

    def start(self):
        self.dirname = filedialog.askdirectory()
        if not self.dirname:
            self.dirname = os.getcwd()
        self.p.configure(maximum=self.estimate.get())
        self.p.start(interval=1000)
        thread = threading.Thread(target=self.translate_video)
        thread.start()

    def estimate_time(self, *args):
        try:
            yt = YouTube(self.url.get())
            self.estimate.set(round(1.3 * (yt.length * W + B), 2))
            self.est_text.set(f'Estimated time: {self.estimate.get()} sec / {self.estimate.get()/60:.2f} min')
            print(yt.length, self.estimate.get())
        except pytube.exceptions.RegexMatchError:
            pass


if __name__ == '__main__':
    MyGUI()
