import wx
import wx.adv
import os
import threading
from loader import Loader
from operations import Operations
from sandbox import Sandbox
from typing import Dict

APP_NAME = 'sbxr-mngr'
TRAY_ICON_PATH = os.path.join(os.path.dirname(__file__), 'icons/sandbox-manager-icon.svg')
SYMBOL_RELOAD = '\u21BB'
TEXT_STOP_ALL = 'Stop all sandboxes'
TEXT_EXIT = 'Exit '
TEXT_STOP = '\u0078   Stop '
TEXT_START = '\u25B6  Start '

def CreateMenuItem(menu: wx.Menu, label: str, function: callable) -> wx.MenuItem:
    menu_option = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, function, id=menu_option.GetId())
    menu.Append(menu_option)
    return menu_option

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame: wx.Frame):
        super().__init__()
        # Frame of the menu
        self.taskbar_frame = frame
        self.set_icon()
        self.menu = wx.Menu()
        self.sandbox_menu_items: Dict[str, wx.MenuItem] = {}
        self.loader = Loader()  # Instantiate Loader once
        # Start a thread to load sandbox data
        threading.Thread(target=self.load_sandbox_data, daemon=True).start()

    def set_icon(self):
        icon = wx.Icon(wx.Bitmap(TRAY_ICON_PATH))
        self.SetIcon(icon, APP_NAME)
        # Bind left click to menu
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_taskbar_left_click)

    def load_sandbox_data(self):
        self.loader.load_data()
        wx.CallAfter(self.update_menu)

    def refresh_sandbox_status(self):
        self.loader.load_data()
        self.update_menu()

    def update_menu(self):
        self.clear_menu()
        self.add_sandbox_items()
        self.add_separator_and_other_items()

    def clear_menu(self):
        # Remove all items from the menu
        for item in self.menu.GetMenuItems():
            self.menu.Remove(item)
        self.sandbox_menu_items.clear()

    def add_sandbox_items(self):
        # Add updated sandbox items
        for sandbox in Sandbox.ListOfSandboxes:
            menu_label = TEXT_STOP + sandbox.name if sandbox.status else TEXT_START + sandbox.name
            menu_item = CreateMenuItem(self.menu, menu_label, self.on_menu)
            self.sandbox_menu_items[sandbox.name] = menu_item
            Sandbox.setSandboxMenuItem(self, sandbox.name, self.menu.GetMenuItemCount() - 1, menu_item)

    def add_separator_and_other_items(self):
        self.menu.AppendSeparator()
        self.stop_all_menu_item = CreateMenuItem(self.menu, TEXT_STOP_ALL, self.on_menu)
        self.menu.AppendSeparator()
        self.exit_menu_item = CreateMenuItem(self.menu, TEXT_EXIT + APP_NAME, self.on_menu)

    def CreatePopupMenu(self) -> wx.Menu:
        self.refresh_sandbox_status()
        return self.menu

    def on_menu(self, event: wx.CommandEvent):
        if event.GetId() == self.exit_menu_item.GetId():
            self.taskbar_frame.Close()
        elif event.GetId() == self.stop_all_menu_item.GetId():
            Operations.stop_all_sandboxes(self)
            self.refresh_sandbox_status()
        else:
            for sandbox in Sandbox.ListOfSandboxes:
                if event.GetId() == self.sandbox_menu_items[sandbox.name].GetId():
                    Operations.toggle_sandbox(self, sandbox)
                    self.refresh_sandbox_status()
                    break
            else:
                event.Skip()

    def on_taskbar_left_click(self, event: wx.CommandEvent):
        self.PopupMenu(self.menu)

class SbxrMngr(wx.Frame):
    def __init__(self):
        super().__init__(None, wx.ID_ANY, "", size=(300, 200))
        panel = wx.Panel(self)
        panel.Show(False)
        self.myapp = TaskBarIcon(self)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, evt: wx.CloseEvent):
        self.myapp.RemoveIcon()
        self.myapp.Destroy()
        self.Destroy()
        evt.Skip()

if __name__ == "__main__":
    MyApp = wx.App()
    SbxrMngr()
    MyApp.MainLoop()
