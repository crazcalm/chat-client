import asyncio
import threading
import tkinter as tk
from tkinter import ttk
from tkinter.constants import BOTH, LEFT, RIGHT, X, YES

from chat_client.gui_parts.window import Window
from chat_client.gui_parts.frame import Frame
from chat_client.gui_parts.nav_bar import NavMenu
from chat_client.gui_parts.nav_bar import NavTab
from chat_client.gui_parts.nav_bar import NavItem
from chat_client.gui_parts.text_box import ChatBox
from chat_client.gui_parts.text_box import UserListView


class ThreadLoop(threading.Thread):
    def __init__(self, loop):
        threading.Thread.__init__(self)
        self.loop = loop

    def run(self):
        print("starting Thread")
        self.loop.run_forever()
        print("Ending Thread")


class ClientProtocol(asyncio.Protocol):
    def __init__(self, chat_box, loop):
        self.chat_box = chat_box
        self.loop = loop
        self.trasport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.chat_box.insert_msg("\n{}".format(data.decode()))

    def connection_lost(self, exc):
        self.chat_box.insert_msg("\n disconnected")
        self.transport.close()
        print("transport has closed")
        print("self.loop.stop()")
        print(self.loop.stop())

    def send_msg(self, message):
        self.transport.write(message.encode())


def test_callback(variable):
    print(variable.get())
    variable.set('')


def test_sending_msg_callback(variable, transport=None, loop=None):
    # Re-write later
    msg = variable.get()
    if transport:
        transport.write(msg.encode())
    else:
        print("No transport")
        print(msg)
    variable.set('')


def connect_to_server(chat_box, address=('127.0.0.1', 3333)):
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: ClientProtocol(
                chat_box, loop), '127.0.0.1', 3333)

    transport, protocol = loop.run_until_complete(coro)
    thread = ThreadLoop(loop)
    thread.start()
    return loop, coro, transport, protocol, thread


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
    file_tab = NavTab(menu_bar, "File", nav_items=file_tab_nav_items)
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
    msg_entry.focus_set()

    # try connecting to the server!
    loop, coro, transport, thread, protocal = connect_to_server(text_box)

    # This closer idea is not bad.
    # Maybe use lambda?
    def test():
        test_sending_msg_callback(msg, transport, loop)

    action = ttk.Button(frame2, text="Click Me!", command=test)
    action.pack(side=LEFT, padx=10)

    gui.bind("<Return>", lambda e: test())

    gui.mainloop()
