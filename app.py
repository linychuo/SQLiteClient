# -*- coding=utf-8 -*-
import os
import wx

from evt import EVT_FORWARD_MAIN_EVENT
from main import MainFrame
from select_db import SelectDBFileFrame


class Application(wx.App):
    __VERSION__ = '1.0.0'

    def __init__(self):
        super(Application, self).__init__()
        self.Bind(EVT_FORWARD_MAIN_EVENT, self.on_forward_main)

    def OnInit(self):
        sp = wx.StandardPaths.Get()
        user_config_dir = sp.GetUserConfigDir()
        app_config_dir = os.path.join(user_config_dir, "SQLiteClient")
        if not os.path.exists(app_config_dir):
            os.mkdir(app_config_dir)
        else:
            pass
        # 读取打开过的数据文件历史，传递给第一个界面
        return 1

    def on_forward_main(self, evt):
        print(evt.attr1)
        print(self.__VERSION__)
        main_frame = MainFrame(self)
        main_frame.Show()


if __name__ == '__main__':
    app = Application()
    frame = SelectDBFileFrame(app)
    frame.Show()
    app.MainLoop()
