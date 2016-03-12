import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter.constants import DISABLED, ACTIVE, NORMAL, END, YES
from tkinter.constants import BOTH, TOP, BOTTOM, LEFT, RIGHT, X, Y


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("tesing this out!")


class Frame(tk.Frame):
    def __init__(self, parent, height=100, width=50):
        super().__init__(parent, height=height, width=width)

class NavMenu(Menu):
    def __init__(self, parent):
        super().__init__(parent)


class NavTab(Menu):
    def __init__(self, parent, label, nav_items=None, tearoff=0):
        """
        :param: nav_items: list of NavItem instances
        """
        super().__init__(parent, tearoff=tearoff)
        self.parent = parent
        self.nav_items = nav_items
        self.label = label

        # create nav_items
        self.create_nav_items()     

    def create_new_nav_item(self, nav_item):
        self.add_command(label=nav_item.label,
            command=nav_item.label)
    
    def create_nav_items(self):
        for nav_item in self.nav_items:
            self.create_new_nav_item(nav_item)


class NavItem:
    def __init__(self, label, command=None):
        self.label = label
        self.command = command

    def __repr__(self):
        return "label: {}, command:{}".format(
            self.label, self.command)


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


def test_callback(variable):
    print(variable.get())
    variable.set('')

if __name__ == "__main__":
    gui = Window()

    # menu?
    menu_bar = NavMenu(gui)
    gui.configure(menu=menu_bar)

    # creating menu tabs items
    file_tab_nav_items = [NavItem("Quit"), NavItem("Connect"), 
        NavItem("Disconnect")]
    edit_tab_nav_items = [NavItem("Profile"), NavItem("Status")]
    
    # creating menu tabs
    file_tab = NavTab(menu_bar,"File", nav_items=file_tab_nav_items)
    edit_tab = NavTab(menu_bar, "Edit", nav_items=edit_tab_nav_items)

    # adding tabs to menu bar
    menu_bar.add_cascade(label=file_tab.label, menu=file_tab)
    menu_bar.add_cascade(label=edit_tab.label, menu=edit_tab)

    frame = Frame(gui)
    #frame.grid(column=0, row=0)
    frame.pack(expand=YES, fill=BOTH, padx=10)

    frame2 = Frame(gui)
    #frame2.grid(column=0, row=1) 
    frame2.pack(expand=YES, fill=BOTH, padx=10, pady=10)

    # creating chat box
    text_box = ChatBox(frame)
    text_box.insert_msg("Hello World")
    text_box.insert_msg("\nPlease be on a new line...")
    text_box.config(state="disabled")
    #text_box.grid(column=0, row=0)
    text_box.pack(side=LEFT, expand=YES, fill=BOTH, padx=10)
    # users?
    users = ["\nMarcus", "\nWillock", "\nCrazcalm"]

    # creating user list view
    user_list_view = UserListView(frame, users)
    #user_list_view.grid(column=2, row=0)
    user_list_view.pack(side=RIGHT, expand=YES, fill=BOTH, padx=10)    

    # creating text entry
    msg = tk.StringVar()
    msg_entry = ttk.Entry(frame2, width=40, textvariable=msg)
    #msg_entry.grid(column=0, row=1)
    msg_entry.pack(side=LEFT, expand=YES, fill=X, padx=10)


    # This closer idea is not bad.
    # Maybe use lambda?
    def test():
        test_callback(msg)

    action = ttk.Button(frame2, text="Click Me!", command=test)
    #action.grid(column=1, row=1)
    action.pack(side=LEFT, padx=10)

    gui.mainloop() 
