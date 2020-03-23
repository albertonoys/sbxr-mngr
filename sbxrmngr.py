import wx
import wx.adv
from loader import Loader
from operations import Operations
from sandbox import Sandbox

APP_NAME = 'sbxr-mngr'
TRAY_ICON_PATH = 'icons/hamburger.png'
SYMBOL_RELOAD = '\u21BB'
TEXT_STOP_ALL = 'Stop all sandboxes'
TEXT_EXIT = 'Exit '
TEXT_STOP = 'Stop '
TEXT_START = 'Start '


def CreateMenuItem(menu, label, function):
    menu_option = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, function, id=menu_option.GetId())
    menu.Append(menu_option)
    return menu_option


class TaskBarIcon(wx.adv.TaskBarIcon):
    TBMENU_STOPALL = None
    TBMENU_CLOSE = None
    TBMENU_SB1 = None
    TBMENU_REFRESH = None

    def __init__(self, frame):
        wx.adv.TaskBarIcon.__init__(self)
        # Frame of the menu
        self.taskbar_frame = frame
        # Set icon
        icon = wx.Icon(wx.Bitmap(TRAY_ICON_PATH))
        self.SetIcon(icon, APP_NAME)
        # Bind left click to menu
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.onTaskbarLeftClick)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        Loader()
        # TaskBarIcon.TBMENU_REFRESH = CreateMenuItem(menu, (SYMBOL_RELOAD + ' Reload').encode('utf-8'), self.OnMenu)
        # menu.AppendSeparator()
        for sandbox in Sandbox.ListOfSandboxes:
            if sandbox.status:
                menuLabel = TEXT_STOP + sandbox.name
            else:
                menuLabel = TEXT_START + sandbox.name
            index = Sandbox.ListOfSandboxes.index(sandbox)
            menuItem = CreateMenuItem(menu, menuLabel, self.OnMenu)
            Sandbox.setSandboxMenuItem(self, sandbox.name, index, menuItem)
        menu.AppendSeparator()
        TaskBarIcon.TBMENU_STOPALL = CreateMenuItem(menu, TEXT_STOP_ALL, self.OnMenu)
        menu.AppendSeparator()
        TaskBarIcon.TBMENU_CLOSE = CreateMenuItem(menu, TEXT_EXIT + APP_NAME, self.OnMenu)
        return menu

    def OnMenu(self, event):
        if event.Id == TaskBarIcon.TBMENU_CLOSE.GetId():
            self.taskbar_frame.Close()
        elif event.Id == TaskBarIcon.TBMENU_STOPALL.GetId():
            Operations.stop_all_sandboxes(self)
            # TaskBarIcon.ShowBalloon(self, 'Title', 'Text')
        # elif event.Id == TaskBarIcon.TBMENU_REFRESH.GetId():
        #     Loader()
        for sandbox in Sandbox.ListOfSandboxes:
            if event.Id == sandbox.menuItem.GetId():
                Operations.toggle_sandbox(self, sandbox)
            else:
                event.Skip()
        else:
            event.Skip()

    def onTaskbarLeftClick(self, event):
        menu = self.CreatePopupMenu()
        self.PopupMenu(menu)
        menu.Destroy()


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
