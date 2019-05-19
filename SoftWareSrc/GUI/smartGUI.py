import os
import sys
from subprocess import call
import subprocess
import threading
from CClient import CClient
import queue
import time

if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk


class SmartGUI(tk.Tk):

    def __init__(self, inP=sys.stdin, outP=sys.stdout):
        tk.Tk.__init__(self)
        self.title('smartConnect')
        self.flag = tk.IntVar()

        canvas = tk.Canvas(self, height=700, width=800)
        canvas.pack()

        # Backgroud image
        background_image = tk.PhotoImage(file='art.png')
        background_space = tk.Label(self, image=background_image)
        background_space.image = background_image
        background_space.place(anchor='nw', x=0, y=0, relwidth=1, relheight=1)

        # Frames
        upper_frame = tk.Listbox(self)
        upper_frame.place(relx=0.5, rely=0.05, relwidth=0.9, relheight=0.8, anchor='n')

        lower_frame = tk.Frame(self, bg='#ccff99', bd=4)
        lower_frame.place(relx=0.5, rely=0.87, relwidth=0.7, relheight=0.2, anchor='n')

        # Labels and Entries
        self.entry = tk.Entry(lower_frame, font=15)
        self.entry.place(relx=0, rely=0, relwidth=0.75, relheight=0.25)

        # Text field
        self.tfield = tk.Text(upper_frame)
        self.tfield.place(relwidth=1, relheight=1)

        # Buttons
        enter_butt = tk.Button(lower_frame, text='enter', font=16, bg='#99ff99',
                               command=lambda: self.user_command())
        clear_console_butt = tk.Button(lower_frame, text='clear console', font=16, bg='#ff9966',
                                    command=self.clear_console)

        enter_butt.place(relx=0.77, rely=0, relwidth=0.2, relheight=0.25)
        clear_console_butt.place(relx=0.3, rely=0.34, relwidth=0.3, relheight=0.25)

        self.outStream=outP
        self.inStream=inP

        self.ginp_q = queue.Queue()
        self.gout_q = queue.Queue()
    
        self.comm2_thread = CClient(ginp_q=self.ginp_q, gout_q=self.gout_q)
        self.comm2_thread.start()

    def display(self, message):
        """Displays output from CClient onto the screen"""
        self.tfield.insert('end', message+'\n')

    def clear_console(self):
        """Clears the console"""
        self.tfield.delete('1.0', tk.END)

    def fetch_user_input(self):
        """Fetches and returns text from entry, and clears the entry"""
        user_text = self.entry.get()
        self.entry.delete(0, 'end')
        return user_text

    def user_command(self):
        """Gets triggered when user clicks the enter button"""
        command_text = self.fetch_user_input()
        self.ginp_q.put(command_text)
        time.sleep(0.05)
        while not self.gout_q.empty():
            try:
                message = self.gout_q.get()
                self.display(message)
            except:
                continue

        # if self.gout_q.empty():
        #     message = self.gout_q.get()
        #     self.display(message)  
    
    def receive(self):
        pass



if __name__ == "__main__":
    app = SmartGUI()
    # message = "nah nah nah"
    # app.display(message)
    # print('username:', app.username)
    # print('password:', app.password)
    app.mainloop()
