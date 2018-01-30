# -*- coding=utf-8 -*-
import wx
import wx.stc as stc

faces = {'name': 'Courier New', 'size': 10, 'size2': 12}
keyword = ['select', 'from', 'order', 'by']


class SQLEditorSTC(stc.StyledTextCtrl):
    def __init__(self, parent):
        stc.StyledTextCtrl.__init__(
            self,
            parent,
            pos=wx.DefaultPosition,
            size=wx.DefaultSize,
            style=wx.BORDER_NONE)
        self.CmdKeyAssign(ord('B'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.CmdKeyAssign(ord('N'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)
        self.SetLexer(stc.STC_LEX_SQL)
        self.SetKeyWords(0, " ".join(keyword))

        self.SetMargins(2, 2)
        self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(1, 40)
        self.SetEdgeMode(stc.STC_EDGE_LINE)
        self.SetEdgeColumn(80)
        self.SetViewWhiteSpace(False)

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,
                          "face:%(name)s,size:%(size)d" % faces)
        self.StyleClearAll()  # Reset all to be like the default

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,
                          "face:%(name)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER,
                          "back:#C0C0C0,face:%(name)s,size:%(size2)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(name)s" % faces)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT,
                          "fore:#FFFFFF,back:#0000FF,bold")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD,
                          "fore:#000000,back:#FF0000,bold")
        self.StyleSetSpec(stc.STC_SQL_WORD,
                          "fore:#00007F,bold,size:%(size)d" % faces)
        self.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, 'fore:#000000')

        self.SetCaretForeground("BLUE")
        self.SetSelBackground(1, '#66CCFF')

    def clear(self):
        self.ClearAll()

    def get_selection(self):
        return self.GetTextRange(self.GetAnchor(), self.GetCurrentPos())


class SQLEditor(wx.Panel):
    def __init__(self, parent, main_parent):
        wx.Panel.__init__(self, parent, size=(1, 1))

        self.main_parent = main_parent
        self.btn_run = wx.Button(self, label='Run')
        self.btn_run.Bind(wx.EVT_BUTTON, self.on_run)
        self.btn_clean = wx.Button(self, label='Clean')
        self.btn_clean.Bind(wx.EVT_BUTTON, self.on_clean)

        self.control_box = wx.BoxSizer(wx.HORIZONTAL)
        self.control_box.Add(self.btn_run)
        self.control_box.Add(self.btn_clean)

        self.editor = SQLEditorSTC(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.control_box, 0, wx.EXPAND)
        self.main_sizer.Add(wx.StaticLine(self), 0, wx.EXPAND)
        self.main_sizer.Add(self.editor, 1, wx.EXPAND)

        self.main_sizer.Fit(self)
        self.SetSizer(self.main_sizer)

    def on_run(self, evt):
        content = self.editor.get_selection()
        if not content:
            content = self.editor.GetValue()
        self.main_parent.log(content)

    def on_clean(self, evt):
        self.editor.clear()
        self.editor.SetFocus()
