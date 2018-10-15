# -*- coding=utf-8 -*-
"""
Main application
"""
import os

import wx

from events import EVT_FORWARD_MAIN_EVENT
from main import MainFrame
from wizard import SelectDBFileFrame

__VERSION__ = '1.0.0'
__APP_NAME__ = 'SQLiteClient'


def read_conf_file(fp):
    """
    Read configuration from file
    """
    try:
        with open(fp) as f:
            return f.readlines()
    except IOError as e:
        return []


def write_conf_file(fp, content):
    with open(fp, 'w') as f:
        f.write(content)


class Application(wx.App):
    def __init__(self):
        super(Application, self).__init__()
        self.Bind(EVT_FORWARD_MAIN_EVENT, self.on_forward_main)

        sp = wx.StandardPaths.Get()
        user_config_dir = sp.GetUserConfigDir()
        self.app_config_dir = os.path.join(user_config_dir, __APP_NAME__)
        if not os.path.exists(self.app_config_dir):
            os.mkdir(self.app_config_dir)

    def OnInit(self):
        self.SetAppName(__APP_NAME__)
        self.SetAppDisplayName(__APP_NAME__)

        return 1

    def on_forward_main(self, evt):
        selected_file = evt.selected_file
        main_frame = MainFrame(self, selected_file)
        main_frame.Show()
        # main_frame.Maximize()

    def write_file_history(self, fh):
        fp = os.path.join(self.app_config_dir, 'fh')
        if os.path.exists(fp):
            all_file_history = read_conf_file(fp)
            if fh not in all_file_history:
                write_conf_file(fp, fh)
        else:
            write_conf_file(fp, fh)

    def read_file_history(self):
        return read_conf_file(os.path.join(self.app_config_dir, 'fh'))

    def del_file_history(self, fh):
        pass

    @staticmethod
    def get_app_name():
        return __APP_NAME__


if __name__ == '__main__':
    app = Application()
    frame = SelectDBFileFrame(app)
    frame.Show()
    app.MainLoop()
