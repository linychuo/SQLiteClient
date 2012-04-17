import wx
import wx.aui
import wx.grid
import wx.html
import  wx.gizmos as gizmos

from mydialog import ConnDBDialog
from dbutil import *


ID_SHOW_CONN_DIALOG = wx.NewId()

class MainWindow(wx.Frame):
    def __init__(self, parent, id= -1, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE | 
                                            wx.SUNKEN_BORDER | 
                                            wx.CLIP_CHILDREN):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)

        self.createMenuBar()
        self.createStatusBar()
        self.createToolBar()
        self.host = ''
        self.port = 0

        self._mgr.AddPane(self.CreateTreeCtrl(), wx.aui.AuiPaneInfo().Name("left").Caption("DB info").Left().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))
        self._mgr.AddPane(self.CreateHTMLCtrl(), wx.aui.AuiPaneInfo().Name("right_html").CenterPane())
        self._mgr.AddPane(self.CreateTreeListCtrl(), wx.aui.AuiPaneInfo().Name("right_tree_list").CenterPane().Hide())

        self._mgr.Update()

    def CreateHTMLCtrl(self):
        htmlCtrl = wx.html.HtmlWindow(self, -1, wx.DefaultPosition, wx.Size(400, 300),wx.html.HW_NO_SELECTION)
        if "gtk2" in wx.PlatformInfo:
            htmlCtrl.SetStandardFonts()
        htmlCtrl.SetPage(self.GetIntroText())
        return htmlCtrl

    def GetIntroText(self):
        return """\
            <html><body>
            <h1>MLook,mongodb client by wxpython</h1>
            </body></html>
            """

    def createToolBar(self):
        tb = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER | wx.TB_HORZ_TEXT)
        tb.SetToolBitmapSize(wx.Size(16, 16))
        
        tb.AddLabelTool(101, "Find", wx.ArtProvider_GetBitmap(wx.ART_FIND,wx.ART_TOOLBAR, wx.Size(16, 16)))
        tb.AddLabelTool(101, "View", wx.ArtProvider_GetBitmap(wx.wx.ART_LIST_VIEW, wx.ART_TOOLBAR, wx.Size(16, 16)))
        #tb.AddSeparator()
        tb.Realize()
        self._mgr.AddPane(tb, wx.aui.AuiPaneInfo().Name("tb").Caption("Toolbar").ToolbarPane().Top().Row(2).LeftDockable(False).RightDockable(False))

    def createStatusBar(self):
        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -3])
        self.statusbar.SetStatusText("Ready", 0)
        self.statusbar.SetStatusText("Welcome To MLook!", 1)

    def createMenuBar(self):
        mb = wx.MenuBar()
        file_menu = wx.Menu()
        file_menu.Append(ID_SHOW_CONN_DIALOG, "Connect")
        file_menu.Append(wx.ID_EXIT, "Exit")
        self.Bind(wx.EVT_MENU, self.OnShowConnDialog, id=ID_SHOW_CONN_DIALOG)

        mb.Append(file_menu, "File")

        self.SetMenuBar(mb)

    def CreateTreeCtrl(self):
        self.db_info_tree = wx.TreeCtrl(self, -1, wx.Point(0, 0), wx.Size(160, 250),
                           wx.TR_DEFAULT_STYLE | wx.NO_BORDER)
        
        img_size = (16, 16)
        imglist = wx.ImageList(img_size[0], img_size[1])
        imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, img_size))
        imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, img_size))
        imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16)))
        self.db_info_tree.AssignImageList(imglist)
        return self.db_info_tree

    def CreateTreeListCtrl(self):
        self.table_data_tree = gizmos.TreeListCtrl(self, -1, style=wx.TR_DEFAULT_STYLE | wx.TR_FULL_ROW_HIGHLIGHT 
                                                   | wx.TR_HIDE_ROOT | wx.TR_ROW_LINES | wx.TR_COLUMN_LINES)
        
        img_size = (16, 16)
        imglist = wx.ImageList(img_size[0], img_size[1])
        imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, img_size))
        imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, img_size))
        imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16)))
        self.table_data_tree.AssignImageList(imglist)
        
        self.table_data_tree.AddColumn("Key")
        self.table_data_tree.AddColumn("Value")
        self.table_data_tree.AddColumn("Type")
        self.table_data_tree.SetMainColumn(0)
        self.table_data_tree.SetColumnWidth(0, 200)
        
        self.table_data_tree_root = self.table_data_tree.AddRoot("Root")
        self.table_data_tree.SetItemText(self.table_data_tree_root, "", 1)
        self.table_data_tree.SetItemText(self.table_data_tree_root, "", 2)
        
        return self.table_data_tree
        

    def OnShowConnDialog(self, event):
        dlg = ConnDBDialog(self, -1, "Connect Setting", size=(400, 200))
        dlg.CenterOnScreen()
        val = dlg.ShowModal()

        if val == wx.ID_OK:
            self.host = dlg.get_host()
            self.port = dlg.get_port()
            dbname = dlg.get_db()
            
            self.db_info_tree.DeleteAllItems()
            root = self.db_info_tree.AddRoot(self.host, 1, 0)
            
            if dbname:
                db = get_db(self.host, self.port, dbname)
                db_item = self.db_info_tree.AppendItem(root, dbname, 0)
                self.db_info_tree.SetItemImage(db_item, 1, wx.TreeItemIcon_Expanded)
                table_names = list(db.collection_names())
                table_names.sort()
                for item in table_names:
                    child = self.db_info_tree.AppendItem(db_item, item, 2)
                    self.db_info_tree.SetPyData(child, ('is_table'))
            else:
                conn = get_conn(self.host, self.port)
                db_names = conn.database_names()
                db_names.sort()
                for item in db_names:
                    child = self.db_info_tree.AppendItem(root, item, 0)
                    self.db_info_tree.SetItemImage(child, 1, wx.TreeItemIcon_Expanded)
                    self.db_info_tree.SetPyData(child, ('is_db'))
                    
            self.db_info_tree.Expand(root)
            self.db_info_tree.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        else:
            print("You pressed Cancel\n")
        dlg.Destroy()
    
    def OnLeftDClick(self, event):
        pt = event.GetPosition();
        node, flags = self.db_info_tree.HitTest(pt)
        if node:
            if self.db_info_tree.GetPyData(node) == 'is_db':
                dbname = self.db_info_tree.GetItemText(node)
                db = get_db(self.host, self.port, dbname)
                self.db_info_tree.DeleteChildren(node)
                table_names = list(db.collection_names())
                table_names.sort()
                for item in table_names:
                    child = self.db_info_tree.AppendItem(node, item, 2)
                    self.db_info_tree.SetPyData(child, ('is_table'))
                self.db_info_tree.Expand(node)
            elif self.db_info_tree.GetPyData(node) == 'is_table':
                table_name = self.db_info_tree.GetItemText(node)
                parent = self.db_info_tree.GetItemParent(node)
                dbname = self.db_info_tree.GetItemText(parent)
                db = get_db(self.host, self.port, dbname)
                self._mgr.GetPane("right_html").Hide()
                self._mgr.GetPane("right_tree_list").Show()
                
                query_result = list(db[table_name].find().limit(1000))
                self.table_data_tree.DeleteChildren(self.table_data_tree_root)
                for idx, item in enumerate(query_result):
                    txt = "(%d) {...}" % idx 
                    child = self.table_data_tree.AppendItem(self.table_data_tree_root, txt)
                    self.table_data_tree.SetItemText(child, '', 1)
                    self.table_data_tree.SetItemText(child, 'document', 2)
                    for k in item:
                        last = self.table_data_tree.AppendItem(child, k)
                        self.table_data_tree.SetItemText(last, unicode(item[k]), 1)
                        self.table_data_tree.SetItemText(last, type(item[k]).__name__, 2)
                
                self._mgr.Update()