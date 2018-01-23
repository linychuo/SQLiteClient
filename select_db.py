# -*- coding=utf-8 -*-
import wx

from evt import ForwardMainEvent
"""
工具中第一个界面：展示所打开过的数据库，同时可选择新的数据库文件
"""


class SelectDBFileFrame(wx.Frame):
    def __init__(self, app):
        super(SelectDBFileFrame, self).__init__(
            parent=None, title=u'SQLiteClient', size=(300, 450))
        self.app = app

        panel = wx.Panel(self)
        main_sizer = wx.GridBagSizer(10, 5)

        # tips
        tip = wx.StaticText(panel, label=u'选择要打开的数据文件')
        main_sizer.Add(tip, pos=(0, 0), span=(0, 3))

        # listbox
        self.history_list = wx.ListBox(panel, style=wx.LB_SINGLE)
        main_sizer.Add(
            self.history_list, pos=(1, 0), span=(1, 3), flag=wx.EXPAND)

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

    def add_history(self, evt):
        pass

    def on_exit(self, evt):
        self.Destroy()

    def on_select_file(self, evt):
        with wx.FileDialog(
                self,
                "Open sqlite db file",
                wildcard="sqlite db files (*.*)|*.*",
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            pathname = fileDialog.GetPath()
            try:
                # forward main page
                self.Destroy()
                wx.PostEvent(self.app, ForwardMainEvent(attr1=pathname))
                # with open(pathname, 'r') as file:
                #     pass
            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)
