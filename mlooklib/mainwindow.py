import wx
import wx.aui
import wx.grid
import wx.html

from mydialog import ConnDBDialog
from dbutil import *


ID_SHOW_CONN_DIALOG = wx.NewId()

class MainWindow(wx.Frame):
    def __init__(self, parent, id=-1, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE |
                                            wx.SUNKEN_BORDER |
                                            wx.CLIP_CHILDREN):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        self.createMenuBar()
        self.createStatusBar()
        self.createToolBar()

        self._mgr.AddPane(self.CreateTreeCtrl(), wx.aui.AuiPaneInfo().Name("left").Caption("DB info").Left().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))
        #self._mgr.AddPane(self.CreateGrid(), wx.aui.AuiPaneInfo().Name("grid_content").CenterPane().MaximizeButton(True))
        self._mgr.AddPane(self.CreateHTMLCtrl(), wx.aui.AuiPaneInfo().Name("right").CenterPane())

        self._mgr.Update()

    def CreateHTMLCtrl(self):
        ctrl = wx.html.HtmlWindow(self, -1, wx.DefaultPosition, wx.Size(400, 300))
        if "gtk2" in wx.PlatformInfo:
            ctrl.SetStandardFonts()
        ctrl.SetPage(self.GetIntroText())        
        return ctrl

    def GetIntroText(self):
        return """\
            <html><body>
            <h1>MLook,mongodb client by wxpython</h1>
            </body></html>
            """

    def createToolBar(self):
        tb = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER | wx.TB_HORZ_TEXT)
        tb.SetToolBitmapSize(wx.Size(16,16))
        tb_bmp1 = wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16))
        tb.AddLabelTool(101, "Item 1", tb_bmp1)
        tb.AddLabelTool(101, "Item 2", tb_bmp1)
        tb.AddSeparator()
        tb.AddLabelTool(101, "Item 5", tb_bmp1)
        tb.Realize()
        self._mgr.AddPane(tb, wx.aui.AuiPaneInfo().
                          Name("tb").Caption("Sample Bookmark Toolbar").
                          ToolbarPane().Top().Row(2).
                          LeftDockable(False).RightDockable(False))

    def createStatusBar(self):
        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -3])
        self.statusbar.SetStatusText("Ready", 0)
        self.statusbar.SetStatusText("Welcome To wxPython!", 1)

    def createMenuBar(self):
        mb = wx.MenuBar()
        file_menu = wx.Menu()
        file_menu.Append(ID_SHOW_CONN_DIALOG,"Connect")
        file_menu.Append(wx.ID_EXIT, "Exit")
        self.Bind(wx.EVT_MENU, self.OnShowConnDialog, id=ID_SHOW_CONN_DIALOG)

        mb.Append(file_menu, "File")

        self.SetMenuBar(mb)

    def CreateTreeCtrl(self):
        self.db_info_tree = wx.TreeCtrl(self, -1, wx.Point(0, 0), wx.Size(160, 250),
                           wx.TR_DEFAULT_STYLE | wx.NO_BORDER)
        return self.db_info_tree

    def CreateGrid(self):
        grid = wx.grid.Grid(self, -1, wx.Point(0, 0), wx.Size(150, 250),
                            wx.NO_BORDER | wx.WANTS_CHARS)
        grid.CreateGrid(10, 20)

        return grid

    def OnShowConnDialog(self,event):
        dlg = ConnDBDialog(self,-1,"Connect Setting",size=(400, 200))
        dlg.CenterOnScreen()
        val = dlg.ShowModal()

        if val == wx.ID_OK:
            host,port,dbname = dlg.get_value()
            db = get_conn(host,int(port),dbname)

            img_size = (16,16)
            imglist = wx.ImageList(img_size[0], img_size[1])
            fldridx     = imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, img_size))
            fldropenidx = imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, img_size))
            fileidx     = imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, img_size))
            
            self.db_info_tree.AssignImageList(imglist)

            root = self.db_info_tree.AddRoot(host)
            self.db_info_tree.SetItemImage(root, fldridx, wx.TreeItemIcon_Normal)
            self.db_info_tree.SetItemImage(root, fldropenidx, wx.TreeItemIcon_Expanded)
            for item in list(db.collection_names()):
                self.db_info_tree.AppendItem(root,item,0)
            self.db_info_tree.Expand(root)
        else:
            print("You pressed Cancel\n")
        dlg.Destroy()

