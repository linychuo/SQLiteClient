# -*- coding=utf-8 -*-

import wx
import sqlite3
from wx import aui

from body_right import SQLEditor


class LeftBar(wx.Panel):
    def __init__(self, parent, db_fp):
        super(LeftBar, self).__init__(
            parent, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN)
        self.db_fp = db_fp

        self.tree = wx.TreeCtrl(self, -1, wx.Point(0, 0), wx.Size(160, 250),
                                wx.TR_DEFAULT_STYLE | wx.NO_BORDER)
        img_list = wx.ImageList(16, 16, True, 2)
        img_list.Add(
            wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER,
                                     wx.Size(16, 16)))
        img_list.Add(
            wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER,
                                     wx.Size(16, 16)))
        self.tree.AssignImageList(img_list)
        self.tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.on_node_activated)

        root = self.tree.AddRoot(self.db_fp, 0)
        self.tree.AppendItem(root, u'表', 0, data='TABLES')
        self.tree.Expand(root)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.tree, 1, wx.EXPAND)
        self.SetSizer(main_sizer)

    def on_node_activated(self, evt):
        selected_item_data = self.tree.GetItemData(evt.GetItem())
        if 'TABLES' == selected_item_data:
            with sqlite3.connect(self.db_fp) as conn:
                for row in conn.execute(
                        "select name from sqlite_master where type = 'table'"):
                    self.tree.AppendItem(
                        evt.GetItem(), row[0], 1, data='TABLE')
                self.tree.Expand(evt.GetItem())
        elif 'TABLE' == selected_item_data:
            selected_item_text = self.tree.GetItemText(evt.GetItem())
            # open tab page


class MainFrame(wx.Frame):
    def __init__(self, app, db_fp):
        super(MainFrame, self).__init__(
            parent=None, title=app.get_app_name(), size=(800, 600))
        self.db_fp = db_fp
        self.app = app

        self.SetMinSize((640, 480))
        self.allowAuiFloating = False

        self.create_menu_bar()
        self.CreateStatusBar()
        self.SetStatusText("Welcome!")

        self.main_panel = wx.Panel(self)
        self.left_bar = LeftBar(self.main_panel, self.db_fp)
        self.right_body = aui.AuiNotebook(
            self.main_panel, -1, style=wx.CLIP_CHILDREN)
        self.right_body.AddPage(SQLEditor(self.right_body, self), "Welcome")
        self.logger = wx.TextCtrl(
            self.main_panel,
            -1,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

        self.mgr = aui.AuiManager()
        self.mgr.SetManagedWindow(self.main_panel)
        self.mgr.AddPane(self.right_body,
                         aui.AuiPaneInfo().CenterPane().Name("Notebook"))
        self.mgr.AddPane(self.left_bar,
                         aui.AuiPaneInfo().Left().Layer(2).BestSize(
                             (240, -1)).MinSize((240, -1)).Floatable(
                                 self.allowAuiFloating).FloatingSize(
                                     (240, 700)).Caption("DB")
                         .CloseButton(False).Name("Tree"))
        self.mgr.AddPane(self.logger,
                         aui.AuiPaneInfo().Bottom().BestSize(
                             (-1, 150)).MinSize((-1, 140)).Floatable(
                                 self.allowAuiFloating).FloatingSize(
                                     (500, 160)).Caption("Log Messages")
                         .CloseButton(False).Name("LogWindow"))
        self.Center(wx.BOTH)
        self.mgr.Update()
        self.Bind(wx.EVT_CLOSE, self.on_exit)

    def create_menu_bar(self):
        fileMenu = wx.Menu()
        exitItem = fileMenu.Append(wx.ID_EXIT)
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.on_exit, exitItem)
        self.Bind(wx.EVT_MENU, self.on_about, aboutItem)

    def on_exit(self, event):
        self.mgr.UnInit()
        self.Destroy()

    def on_about(self, event):
        wx.MessageBox("This is a wxPython Hello World sample",
                      "About Hello World 2", wx.OK | wx.ICON_INFORMATION)

    def log(self, message):
        self.logger.AppendText(message + "\n")
