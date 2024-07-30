import os
import unittest
from unittest.mock import Mock, patch, MagicMock

import pytest
import wx
import sbxrmngr
import json
from loader import Loader
from sandbox import Sandbox

# Monkey patch loader to do it from file
def GetJsonFromSandboxer(self):
    with open('test/sbxr.json', 'r') as f:
        Loader.SANDBOXES_DICT = json.load(f)

Loader.GetJsonFromSandboxer = GetJsonFromSandboxer

class TestSbxrMngr(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize Sandbox.ListOfSandboxes
        Loader()

    # Skip this test if there's no $DISPLAY until I figure out how to run it in headless mode
    @pytest.mark.skipif(os.getenv('DISPLAY', False) == False, reason="does not run without a DISPLAY")
    def test_create_menu_item(self):
        app = wx.App()
        menu = wx.Menu()
        function = Mock()
        menuItem = sbxrmngr.CreateMenuItem(menu, 'test', function)
        self.assertIsInstance(menu, wx.Menu)
        self.assertIsInstance(menuItem, wx.MenuItem)
        self.assertEqual(menuItem.GetItemLabel(), 'test')
        self.assertEqual(menuItem.GetItemLabelText(), 'test')
        self.assertEqual(menuItem.GetClassName(), 'wxMenuItem')
        self.assertEqual(menu.GetClassName(), 'wxMenu')
        self.assertEqual(menu.GetMenuItemCount(), 1)

    # Skip this test if there's no $DISPLAY until I figure out how to run it in headless mode
    @pytest.mark.skipif(os.getenv('DISPLAY', False) == False, reason="does not run without a DISPLAY")
    def test_create_popup_menu(self):
        app = wx.App()
        frame = wx.Frame(None)
        taskBarIcon = sbxrmngr.TaskBarIcon(frame)
        popupmenu = taskBarIcon.CreatePopupMenu()
        self.assertIsInstance(popupmenu, wx.Menu)
        menu_items_labels = []
        for menu_item in popupmenu.GetMenuItems():
            menu_items_labels.append(menu_item.GetItemLabel())

        expected_labels = [
            sbxrmngr.TEXT_START + 'sb1',
            sbxrmngr.TEXT_STOP + 'sb2',
            sbxrmngr.TEXT_STOP + 'sb99',
            sbxrmngr.TEXT_START + 'sb77',
            sbxrmngr.TEXT_START + 'sb5',
            '',  # Separator
            sbxrmngr.TEXT_STOP_ALL,
            '',  # Separator
            sbxrmngr.TEXT_EXIT + sbxrmngr.APP_NAME
        ]

        self.assertListEqual(menu_items_labels, expected_labels)

if __name__ == '__main__':
    unittest.main()
