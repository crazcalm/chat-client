import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter.constants import DISABLED, ACTIVE, NORMAL, END, YES
from tkinter.constants import BOTH, TOP, BOTTOM, LEFT, RIGHT, X, Y

from chat_client.gui_parts.window import Window
from chat_client.gui_parts.frame import Frame
from chat_client.gui_parts.nav_bar import NavMenu
from chat_client.gui_parts.nav_bar import NavTab
from chat_client.gui_parts.nav_bar import NavItem
from chat_client.gui_parts.text_box import ChatBox
from chat_client.gui_parts.text_box import UserListView


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
    frame.pack(expand=YES, fill=BOTH, padx=10)

    frame2 = Frame(gui)
    frame2.pack(expand=YES, fill=BOTH, padx=10, pady=10)

    # creating chat box
    text_box = ChatBox(frame)
    text_box.insert_msg("Hello World")
    text_box.insert_msg("\nPlease be on a new line...")
    text_box.config(state="disabled")
    text_box.pack(side=LEFT, expand=YES, fill=BOTH, padx=10)
    # users?
    users = ["\nMarcus", "\nWillock", "\nCrazcalm"]

    # creating user list view
    user_list_view = UserListView(frame, users)
    user_list_view.pack(side=RIGHT, expand=YES, fill=BOTH, padx=10)    

    # creating text entry
    msg = tk.StringVar()
    msg_entry = ttk.Entry(frame2, width=40, textvariable=msg)
    msg_entry.pack(side=LEFT, expand=YES, fill=X, padx=10)


    # This closer idea is not bad.
    # Maybe use lambda?
    def test():
        test_callback(msg)

    action = ttk.Button(frame2, text="Click Me!", command=test)
    action.pack(side=LEFT, padx=10)

    gui.mainloop() 
