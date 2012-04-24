import wx
import wx.lib.sized_controls as sc

# class ConnDBDialog(wx.Dialog):
#     def __init__(
#             self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
#             style=wx.DEFAULT_DIALOG_STYLE,
#             useMetal=False,
#             ):
#         pre = wx.PreDialog()
#         pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
#         pre.Create(parent, ID, title, pos, size, style)

#         self.PostCreate(pre)

#         if 'wxMac' in wx.PlatformInfo and useMetal:
#             self.SetExtraStyle(wx.DIALOG_EX_METAL)

#         sizer = wx.BoxSizer(wx.VERTICAL)

#         box_host = wx.BoxSizer(wx.HORIZONTAL)
#         label_host = wx.StaticText(self, -1, "Host:")
#         box_host.Add(label_host, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
#         self.text_host = wx.TextCtrl(self, -1, "localhost", size=(80, -1))
#         box_host.Add(self.text_host, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
#         sizer.Add(box_host, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

#         box_port = wx.BoxSizer(wx.HORIZONTAL)
#         label_port = wx.StaticText(self, -1, "Port:")
#         box_port.Add(label_port, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
#         self.text_port = wx.TextCtrl(self, -1, "27017", size=(80, -1))
#         box_port.Add(self.text_port, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
#         sizer.Add(box_port, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

#         box_db = wx.BoxSizer(wx.HORIZONTAL)
#         label_db = wx.StaticText(self, -1, "DB:  ")
#         box_db.Add(label_db, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
#         self.text_db = wx.TextCtrl(self, -1, "", size=(80, -1))
#         box_db.Add(self.text_db, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
#         sizer.Add(box_db, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

#         line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
#         sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP, 5)

#         btnsizer = wx.StdDialogButtonSizer()
        
#         if wx.Platform != "__WXMSW__":
#             btn = wx.ContextHelpButton(self)
#             btnsizer.AddButton(btn)
        
#         btn = wx.Button(self, wx.ID_OK)
#         btn.SetDefault()
#         btnsizer.AddButton(btn)

#         btn = wx.Button(self, wx.ID_CANCEL)
#         btnsizer.AddButton(btn)
#         btnsizer.Realize()

#         sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

#         self.SetSizer(sizer)
#         sizer.Fit(self)
    
#     def get_host(self):
#         return self.text_host.GetValue()
    
#     def get_port(self):
#         return int(self.text_port.GetValue())
        
#     def get_db(self):
#         return self.text_db.GetValue()

class ConnDBDialog(sc.SizedDialog):
	def __init__(self,parent,id):
		sc.SizedDialog.__init__(self,parent,id,'Connect Settings',
								style=wx.DEFAULT_DIALOG_STYLE)
		pane = self.GetContentsPane()
		pane.SetSizerType("form")

		#host
		wx.StaticText(pane,-1,"Host")
		self.hostTxt = wx.TextCtrl(pane, -1,size=(200,-1))
		self.hostTxt.SetSizerProps(expand=True)

		#Port
		wx.StaticText(pane,-1,"Port")
		self.portTxt = wx.TextCtrl(pane, -1,'27017',size=(50,-1))

		#db
		wx.StaticText(pane,-1,"DB")
		self.dbTxt = wx.TextCtrl(pane, -1,size=(150,-1))

		self.SetButtonSizer(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL))
		self.Fit()
		self.SetMinSize(self.GetSize())

	def get_host(self):
		return self.hostTxt.GetValue()

	def get_port(self):
		return int(self.portTxt.GetValue())

	def get_db(self):
		return self.dbTxt.GetValue()

class QueryDialog(sc.SizedDialog):
	def __init__(self,parent,id):
		sc.SizedDialog.__init__(self,parent,id,'Query',style=wx.DEFAULT_DIALOG_STYLE)
		pane = self.GetContentsPane()

		self.queryTxt = wx.TextCtrl(pane, -1, style=wx.TE_MULTILINE,size=(300,200))
		self.queryTxt.SetSizerProps(expand=True, proportion=1)

		self.SetButtonSizer(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL))
		self.Fit()
		self.SetMinSize(self.GetSize())

	def get_query_txt(self):
		return self.queryTxt.GetValue()

