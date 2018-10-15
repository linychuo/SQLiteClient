# -*- coding=utf-8 -*-
"""
Main frame
"""

import wx
from wx import aui

from db import DBUtils
from events import EVT_CREATE_MAIN_EVENT, CreateTabEvent
from sql_editor import SQLEditor


class TableMetaPanel(wx.Panel):
    def __init__(self, parent, data_list):
        wx.Panel.__init__(self, parent=parent)

        meta_data_list_ctrl = wx.ListCtrl(self, style=wx.LC_REPORT)
        meta_data_list_ctrl.InsertColumn(0, "")
        meta_data_list_ctrl.InsertColumn(1, "PK")
        meta_data_list_ctrl.InsertColumn(2, "Name")
        meta_data_list_ctrl.InsertColumn(3, "Type")
        meta_data_list_ctrl.InsertColumn(4, "Null?")
        meta_data_list_ctrl.InsertColumn(5, "Default Value")

        for item in data_list:
            meta_data_list_ctrl.Append(
                (item.idx, item.pk_field, item.column_name, item.column_type, item.allow_null, item.default_value))
        meta_data_list_ctrl.SetColumnWidth(0, 20)
        meta_data_list_ctrl.SetColumnWidth(1, 40)
        meta_data_list_ctrl.SetColumnWidth(2, 150)
        meta_data_list_ctrl.SetColumnWidth(5, 150)
        root_sizer = wx.BoxSizer(wx.VERTICAL)
        root_sizer.Add(meta_data_list_ctrl, 1, wx.EXPAND)

        self.SetSizer(root_sizer)


class SideBar(wx.Panel):
    def __init__(self, parent, db_fp):
        super(SideBar, self).__init__(
            parent, style=wx.TAB_TRAVERSAL | wx.CLIP_CHILDREN)
        self.db_fp = db_fp
        self.db_utils = DBUtils(self.db_fp)
        self.parent = parent

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
        for item in self.db_utils.get_object_type():
            self.tree.AppendItem(root, item, 0, data=item.upper())
        self.tree.Expand(root)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.tree, 1, wx.EXPAND)
        self.SetSizer(main_sizer)

    def on_node_activated(self, evt):
        selected_item_data = self.tree.GetItemData(evt.GetItem())
        if selected_item_data in ['TABLE', 'INDEX', 'TRIGGER', 'VIEW']:
            for name in self.db_utils.get_object_list(selected_item_data.lower()):
                self.tree.AppendItem(evt.GetItem(), name, 1, data='EACH-%s' % selected_item_data)
            self.tree.Expand(evt.GetItem())
        elif 'EACH-TABLE' == selected_item_data:
            selected_item_text = self.tree.GetItemText(evt.GetItem())
            table_metadata = self.db_utils.get_meta_of_table(selected_item_text)
            wx.PostEvent(self.parent, CreateTabEvent(table_metadata=table_metadata,
                                                     tab_name="Table %s" % selected_item_text))


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
        self.left = SideBar(self.main_panel, self.db_fp)
        self.right = aui.AuiNotebook(self.main_panel, -1, style=wx.CLIP_CHILDREN)
        self.right.AddPage(SQLEditor(self.right, self), "Welcome")
        self.logger = wx.TextCtrl(self.main_panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

        self.mgr = aui.AuiManager()
        self.mgr.SetManagedWindow(self.main_panel)
        self.mgr.AddPane(self.right,
                         aui.AuiPaneInfo().CenterPane().Name("Notebook"))
        self.mgr.AddPane(self.left,
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
        self.main_panel.Bind(EVT_CREATE_MAIN_EVENT, self.on_create_new_tab)

    def on_create_new_tab(self, evt):
        has_created = False
        for i in xrange(0, self.right.GetPageCount()):
            if self.right.GetPageText(i) == evt.tab_name:
                self.right.ChangeSelection(i)
                has_created = True
                break
        if not has_created:
            self.right.AddPage(TableMetaPanel(self.right, evt.table_metadata), caption=evt.tab_name, select=True)

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
