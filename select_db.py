# -*- coding=utf-8 -*-
import wx
from os.path import isfile, getsize

from evt import ForwardMainEvent
"""
工具中第一个界面：展示所打开过的数据库，同时可选择新的数据库文件
"""


def is_sqlite3_db(filename):
    if not isfile(filename):
        return False
    if getsize(filename) < 100:  # SQLite database file header is 100 bytes
        return False

    with open(filename, 'rb') as fd:
        header = fd.read(100)

    return header[:15] == b'SQLite format 3'


class SelectDBFileFrame(wx.Frame):
    def __init__(self, app):
        super(SelectDBFileFrame, self).__init__(
            parent=None, title=app.get_app_name(), size=(300, 450))
        self.app = app

        panel = wx.Panel(self)
        main_sizer = wx.GridBagSizer(10, 5)

        # tips
        tip = wx.StaticText(panel, label=u'选择要打开的数据文件')
        main_sizer.Add(tip, pos=(0, 0), span=(0, 3))

        # listbox
        history_list = wx.ListBox(
            panel, choices=self.app.read_file_history(), style=wx.LB_SINGLE)
        history_list.Bind(wx.EVT_LISTBOX_DCLICK, self.on_item_click)
        main_sizer.Add(history_list, pos=(1, 0), span=(1, 3), flag=wx.EXPAND)

        btn1 = wx.Button(panel, label=u'选择...', size=(80, 30))
        btn1.Bind(wx.EVT_BUTTON, self.on_select_file)
        main_sizer.Add(btn1, pos=(2, 0))

        btn2 = wx.Button(panel, label=u'确定', size=(60, 30))
        main_sizer.Add(btn2, pos=(2, 1))

        btn3 = wx.Button(panel, label=u'退出', size=(60, 30))
        btn3.Bind(wx.EVT_BUTTON, self.on_exit)
        main_sizer.Add(btn3, pos=(2, 2))

        main_sizer.AddGrowableRow(1)
        main_sizer.AddGrowableCol(0)

        root_sizer = wx.BoxSizer(wx.HORIZONTAL)
        root_sizer.Add(
            main_sizer, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        panel.SetSizer(root_sizer)

        self.Center()

    def on_exit(self, evt):
        self.Destroy()

    def on_item_click(self, evt):
        selected_item = evt.GetString()
        self.forward_next_frame(selected_item)

    def on_select_file(self, evt):
        with wx.FileDialog(
                self,
                "Open sqlite db file",
                wildcard="sqlite db files (*.*)|*.*",
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            pathname = fileDialog.GetPath()
            self.forward_next_frame(pathname)

    def forward_next_frame(self, pathname):
        try:
            if is_sqlite3_db(pathname):
                self.app.write_file_history(pathname)
                self.Destroy()
                wx.PostEvent(
                    self.app, ForwardMainEvent(selected_file=pathname))
            else:
                wx.MessageBox(u'选择的文件不是sqlite3数据文件，请重新选择!', u'错误',
                              wx.OK | wx.ICON_ERROR)
        except IOError as e:
            print(e)
            wx.LogError("Cannot open file '%s'." % pathname)
