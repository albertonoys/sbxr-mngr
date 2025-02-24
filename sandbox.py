import wx

RUNNING = 'Running'

class Sandbox(object):
    ListOfSandboxes = []

    def __init__(self, name, status, eventid=None, menuitem=None):
        self.name = name
        if status == RUNNING:
            self.status = True
        else:
            self.status = False
        self.eventId = eventid
        self.menuItem = menuitem
        # For future features:
        #
        # self.directory = directory
        # self.mountpoint = mountpoint
        # self.ip = ip
        # self.traits = traits
        # self.branch = branch

    def setSandboxMenuItem(self, sb_name, index, menu_item):
        for sandbox in Sandbox.ListOfSandboxes:
            if sandbox.name == sb_name:
                Sandbox.ListOfSandboxes[index].menuItem = menu_item
