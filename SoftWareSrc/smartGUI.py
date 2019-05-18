import os
import sys
from subprocess import Popen, PIPE, STDOUT
import subprocess
from CClient import CClient

if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk


class SmartGUI(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title('smartConnect')
        self.flag = tk.IntVar()

        canvas = tk.Canvas(self, height=700, width=800)
        canvas.pack()

        # Backgroud image
    #    background_image = tk.PhotoImage(file='niggah.png')
   #     background_space = tk.Label(self, image=background_image)
   #     background_space.image = background_image
   #     background_space.place(anchor='nw', x=0, y=0, relwidth=1, relheight=1)

        # Frames
        upper_frame = tk.Frame(self)
        upper_frame.place(relx=0.5, rely=0.05, relwidth=0.9, relheight=0.6, anchor='n')

        lower_frame = tk.Frame(self, bg='#a7dee2', bd=4)
        lower_frame.place(relx=0.5, rely=0.67, relwidth=0.8, relheight=0.3, anchor='n')

        # Labels and Entries
        self.entry = tk.Entry(lower_frame, font=15)
        label_1 = tk.Label(lower_frame, text='Login to Remote User', font=16)
        label_2 = tk.Label(lower_frame, text='Show current user', font=16)
        label_3 = tk.Label(lower_frame, text='Create new user', font=16)
        label_4 = tk.Label(lower_frame, text='Change remote serverr', font=16)

        self.entry.place(relx=0, rely=0, relwidth=0.75, relheight=0.15)
        label_1.place(relx=0.1, rely=0.2, relwidth=0.4, relheight=0.15)
        label_2.place(relx=0.1, rely=0.4, relwidth=0.4, relheight=0.15)
        label_3.place(relx=0.1, rely=0.6, relwidth=0.4, relheight=0.15)
        label_4.place(relx=0.1, rely=0.8, relwidth=0.4, relheight=0.15)

        # Text field
        self.tfield = tk.Text(upper_frame)
        self.tfield.place(relwidth=1, relheight=1)

        # Buttons
        enter_butt = tk.Button(lower_frame, text='enter', font=16, bg='#ffffcc',
                               command=self.user_input)
       
        enter_butt.place(relx=0.77, rely=0, relwidth=0.2, relheight=0.15)
        

    def user_input(self):
        print('fff')
    def show_current_user(self):
        """Display current user"""
        pass

    def create_new_user(self):
        """Invokes CClient to add new user"""
        pass

    def change_remote_server(self):
        """Instructs CClient to change remote server"""
        pass

    def display(self, message):
        """Displays output from CClient on to the screen"""
        self.tfield.insert('end', message+'\n')

    def fetch_user_input(self):
        """Fetches and returns text from entry, and clears the entry"""
        user_text = self.entry.get()
        self.entry.delete(0, 'end')
        self.pipe_in_1("user_text")
        return user_text
    
    def receive(self):
        
        pass



if __name__ == "__main__":
    app = SmartGUI()
    # message = "nah nah nah"
    # app.display(message)
    # print('username:', app.username)
    # print('password:', app.password)
    app.mainloop()