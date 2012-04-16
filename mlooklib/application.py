import wx
from mainwindow import MainWindow
 
class wxApp(wx.App):
    def OnInit(self):
        frame = MainWindow(None, wx.ID_ANY, "MLook", size=(1024, 768))
        frame.Show(True)
        self.SetTopWindow(frame)
        return True
