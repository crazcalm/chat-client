import asyncio
import threading
import tkinter as tk
from tkinter import ttk
from tkinter.constants import BOTH, LEFT, X, YES, RIGHT
from time import sleep

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
    def __init__(self, chat_box, user_list, loop):
        self.chat_box = chat_box
        self.user_list = user_list
        self.loop = loop
        self.trasport = None

    def get_user_list(self):
        sleep(1)
        self.transport.write("/CLIENT**: USER LIST".encode())

    def connection_made(self, transport):
        self.transport = transport
        self.get_user_list()

    def data_received(self, data):
        msg = data.decode()

        if msg.startswith("CLIENT**:"):
            client_info = msg.split(":", 1)[1].strip()
            self.user_list.delete_all()
            self.user_list.create_list(client_info.split(","))

        else:
            self.chat_box.insert_msg("\n{}".format(msg))

    def connection_lost(self, exc):
        self.transport.close()
        print("transport has closed")
        print(self.loop.stop())
        print("stopping the loop")

    def send_msg(self, message):
        self.transport.write(message.encode())


def test_callback(variable):
    print(variable.get())
    variable.set('')


def test_sending_msg_callback(variable, transport=None, loop=None,
                              thread=None):
    # Re-write later
    msg = variable.get()
    if transport:
        transport.write(msg.encode())
    else:
        print("No transport")
        print(msg)
    variable.set('')


def connect_to_server(chat_box, user_list, address=('127.0.0.1', 3333)):
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: ClientProtocol(
                chat_box, user_list, loop), '127.0.0.1', 3333)

    transport, protocol = loop.run_until_complete(coro)
    thread = ThreadLoop(loop)
    thread.start()
    return loop, coro, transport, protocol, thread


def _disconnect(gui, transport, loop):
    if loop.is_running():
        transport.write("/disconnect".encode())


class App:
    def __init__(self, window=Window, chatbox=ChatBox, frame=Frame,
                 nav_menu=NavMenu, nav_item=NavItem, nav_tab=NavTab,
                 user_list_view=UserListView):
        # Variables that will be needed
        self.loop = None

        # Main gui
        self.gui = window()

        # Frame in charge of chatbox?
        self.frame1 = frame(self.gui)
        self.frame1.pack(expand=YES, fill=BOTH, padx=10)

        # Frame in charge of user list box?
        self.frame2 = frame(self.gui)
        self.frame2.pack(expand=YES, fill=BOTH, padx=10, pady=10)

        # Look into adding state to the init
        self.textbox = chatbox(self.frame1)
        self.textbox.config(state="disabled")
        self.textbox.pack(side=LEFT, expand=YES, fill=BOTH, padx=10)

        # creating user list view
        self.user_list = user_list_view(self.frame1)
        self.user_list.pack(side=RIGHT, expand=YES, fill=BOTH, padx=10)

        # Testing: connect to server immediately
        self.connect_to_server()

        # menu bar is next
        self.menu_bar = NavMenu(self.gui)
        self.gui.configure(menu=self.menu_bar)

        # creating menu tabs items
        file_tab_nav_items = [nav_item("Connect", self.connect_to_server),
                              nav_item("Disconnect", self.disconnect)]
        edit_tab_nav_items = [nav_item("Profile"),
                              nav_item("Status")]

        # creating menu tabs
        file_tab = nav_tab(self.menu_bar, "File", nav_items=file_tab_nav_items)
        edit_tab = nav_tab(self.menu_bar, "Edit", nav_items=edit_tab_nav_items)

        # adding tabs to menu bar
        self.menu_bar.add_cascade(label=file_tab.label, menu=file_tab)
        self.menu_bar.add_cascade(label=edit_tab.label, menu=edit_tab)

        # creating text entry
        self.msg = tk.StringVar()
        self.msg_entry = ttk.Entry(self.frame2, width=40,
                                   textvariable=self.msg)
        self.msg_entry.pack(side=LEFT, expand=YES, fill=X, padx=10)
        self.msg_entry.focus_set()

        self.action = ttk.Button(self.frame2, text="Click Me!",
                                 command=self.send_msg_callback)
        self.action.pack(side=LEFT, padx=10)

        self.gui.bind("<Return>", lambda e: self.send_msg_callback())

        self.gui.mainloop()

    def connect_to_server(self):
        if not self.loop:
            self.loop, self.coro, self.transport, self.protocol,\
                self.thread = connect_to_server(self.textbox, self.user_list)

    def disconnect(self):
        _disconnect(self.gui, self.transport, self.loop)
        self.loop = None

    def send_msg_callback(self):
        test_sending_msg_callback(self.msg, self.transport, self.loop)


if __name__ == "__main__":
    test = App()
