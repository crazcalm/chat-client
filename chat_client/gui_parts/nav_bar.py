from tkinter import Menu


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
            command=nav_item.command)
    
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
