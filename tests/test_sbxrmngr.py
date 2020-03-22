import unittest
from unittest.mock import Mock, patch, MagicMock
import wx
import sbxrmngr
import sandbox
import json

from loader import Loader


# Monkey patch loader to do it from file
def GetJsonFromSandboxer(self):
    with open('sbxr.json', 'r') as f:
        Loader.SANDBOXES_DICT = json.load(f)


Loader.GetJsonFromSandboxer = GetJsonFromSandboxer


class TestSbxrMngr(unittest.TestCase):
    app = wx.App()

    def test_create_menu_item(self):
        menu = wx.Menu()
        function = Mock()
        menuItem = sbxrmngr.CreateMenuItem(menu, 'test', function)
        self.assertIsInstance(menu, wx.Menu)
        self.assertIsInstance(menuItem, wx.MenuItem)
        self.assertEqual(menuItem.ItemLabel, 'test')
        self.assertEqual(menuItem.ItemLabelText, 'test')
        self.assertEqual(menuItem.ClassName, 'wxMenuItem')
        self.assertEqual(menu.ClassName, 'wxMenu')
        self.assertEqual(menu.EvtHandlerEnabled, True)
        self.assertEqual(menu.MenuItemCount, 1)

    def test_create_popup_menu(self):
        separator = ''
        TaskBarIcon = Mock()
        popupmenu = sbxrmngr.TaskBarIcon.CreatePopupMenu(TaskBarIcon)
        self.assertIsInstance(popupmenu, wx.Menu)
        menu_items_labels = []
        for menu_item in popupmenu.MenuItems:
            menu_items_labels.append(menu_item.ItemLabel)
        self.assertListEqual(menu_items_labels, [sbxrmngr.TEXT_START + 'sb1',
                                                 sbxrmngr.TEXT_STOP + 'sb2',
                                                 sbxrmngr.TEXT_STOP + 'sb99',
                                                 sbxrmngr.TEXT_START + 'sb77',
                                                 sbxrmngr.TEXT_START + 'sb5',
                                                 separator,
                                                 sbxrmngr.TEXT_STOP_ALL,
                                                 separator,
                                                 sbxrmngr.TEXT_EXIT + sbxrmngr.APP_NAME])


if __name__ == '__main__':
    unittest.main()
