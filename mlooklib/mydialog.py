import wx

class ConnDBDialog(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE,
            useMetal=False,
            ):

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)

        # This extra style can be set after the UI object has been created.
        if 'wxMac' in wx.PlatformInfo and useMetal:
            self.SetExtraStyle(wx.DIALOG_EX_METAL)


        # Now continue with the normal construction of the dialog
        # contents
        sizer = wx.BoxSizer(wx.VERTICAL)

        box_host = wx.BoxSizer(wx.HORIZONTAL)
        label_host = wx.StaticText(self, -1, "Host:")
        box_host.Add(label_host, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.text_host = wx.TextCtrl(self, -1, "localhost", size=(80,-1))
        box_host.Add(self.text_host, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box_host, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box_port = wx.BoxSizer(wx.HORIZONTAL)
        label_port = wx.StaticText(self, -1, "Port:")
        box_port.Add(label_port, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.text_port = wx.TextCtrl(self, -1, "27017", size=(80,-1))
        box_port.Add(self.text_port, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box_port, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box_db = wx.BoxSizer(wx.HORIZONTAL)
        label_db = wx.StaticText(self,-1,"DB:  ")
        box_db.Add(label_db,0,wx.ALIGN_CENTRE|wx.ALL,5)
        self.text_db = wx.TextCtrl(self, -1, "", size=(80,-1))
        box_db.Add(self.text_db, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box_db, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def get_value(self):
        return self.text_host.GetValue(),self.text_port.GetValue(),self.text_db.GetValue()