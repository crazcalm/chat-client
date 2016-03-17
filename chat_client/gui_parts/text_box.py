import tkinter as tk
from tkinter import scrolledtext
from tkinter.constants import DISABLED, ACTIVE, NORMAL, END, YES


class ChatBox(scrolledtext.ScrolledText):
    def __init__(self, parent, height=10, width=80, state=DISABLED,
            word=tk.WORD):
        super().__init__(parent, height=height, width=width)
        self.height = height
        self.width = width
        self.state = state  # create a getter/setter
    
    def toggle_state(self):
        if self.state == DISABLED:
            self.state = NORMAL
        else:
            self.state = DISABLED
        self.config(state=self.state)
    
    def _insert(self, msg):
        if self.state == DISABLED:
            self.toggle_state()
        self.insert(END, msg)
        self.toggle_state()

    def insert_msg(self, msg):
        self._insert(msg)
        self.yview_moveto('1.0')


class UserListView(ChatBox):
    def __init__(self, parent, user_list, height=20, width=30):
        super().__init__(parent, height=height, width=width)
        self.user_list = user_list

        # create list
        self.create_list(self.user_list)

    def delete_all(self):
        if self.state == DISABLED:
            self.toggle_state()
        self.delete('0.0', END)
        self.toggle_state()

    def create_list(self, user_list):
        for user in user_list:
            self._insert(user)            
