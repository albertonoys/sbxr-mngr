import wx
import wx.adv
import os
import threading
from loader import Loader
from operations import Operations
from sandbox import Sandbox

APP_NAME = 'sbxr-mngr'
TRAY_ICON_PATH = os.path.join(os.path.dirname(__file__), 'icons/sandbox-manager-icon.svg')
SYMBOL_RELOAD = '\u21BB'
TEXT_STOP_ALL = 'Stop all sandboxes'
TEXT_EXIT = 'Exit '
TEXT_STOP = '\u0078   Stop '
TEXT_START = '\u25B6  Start '

def CreateMenuItem(menu, label, function):
    menu_option = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, function, id=menu_option.GetId())
    menu.Append(menu_option)
    return menu_option

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        wx.adv.TaskBarIcon.__init__(self)
        # Frame of the menu
        self.taskbar_frame = frame
        # Set icon
        icon = wx.Icon(wx.Bitmap(TRAY_ICON_PATH))
        self.SetIcon(icon, APP_NAME)
        # Bind left click to menu
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.onTaskbarLeftClick)

        self.menu = wx.Menu()
        self.sandbox_menu_items = {}

        # Start a thread to load sandbox data
        threading.Thread(target=self.loadSandboxData, daemon=True).start()

    def loadSandboxData(self):
        Loader()
        wx.CallAfter(self.updateMenu)

    def refreshSandboxStatus(self):
        Loader()  # Refresh sandbox statuses
        self.updateMenu()

    def updateMenu(self):
        # Remove all existing menu items
        for item in self.menu.GetMenuItems():
            self.menu.Remove(item)
        self.sandbox_menu_items.clear()

        # Add updated sandbox items
        for sandbox in Sandbox.ListOfSandboxes:
            menuLabel = TEXT_STOP + sandbox.name if sandbox.status else TEXT_START + sandbox.name
            menuItem = CreateMenuItem(self.menu, menuLabel, self.OnMenu)
            self.sandbox_menu_items[sandbox.name] = menuItem
            Sandbox.setSandboxMenuItem(self, sandbox.name, self.menu.GetMenuItemCount() - 1, menuItem)

        # Add separator and other items
        self.menu.AppendSeparator()
        self.stopAllMenuItem = CreateMenuItem(self.menu, TEXT_STOP_ALL, self.OnMenu)
        self.menu.AppendSeparator()
        self.exitMenuItem = CreateMenuItem(self.menu, TEXT_EXIT + APP_NAME, self.OnMenu)

    def CreatePopupMenu(self):
        self.refreshSandboxStatus()  # Refresh sandbox statuses before showing menu
        return self.menu

    def OnMenu(self, event):
        if event.GetId() == self.exitMenuItem.GetId():
            self.taskbar_frame.Close()
        elif event.GetId() == self.stopAllMenuItem.GetId():
            Operations.stop_all_sandboxes(self)
            self.refreshSandboxStatus()
        else:
            for sandbox in Sandbox.ListOfSandboxes:
                if event.GetId() == self.sandbox_menu_items[sandbox.name].GetId():
                    Operations.toggle_sandbox(self, sandbox)
                    self.refreshSandboxStatus()
                    break
            else:
                event.Skip()

    def onTaskbarLeftClick(self, event):
        self.PopupMenu(self.menu)

class SbxrMngr(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "", size=(300, 200))
        panel = wx.Panel(self)
        panel.Show(False)
        self.myapp = TaskBarIcon(self)
        self.Bind(wx.EVT_CLOSE, self.onClose)

    def onClose(self, evt):
        # Destroy the taskbar icon and the frame
        self.myapp.RemoveIcon()
        self.myapp.Destroy()
        self.Destroy()
        evt.Skip()

if __name__ == "__main__":
    MyApp = wx.App()
    SbxrMngr()
    MyApp.MainLoop()
