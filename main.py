import wx

class ToolbarPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        box = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self, label="Toolbar", style=wx.ALIGN_CENTRE)
        box.Add(text, 0, wx.EXPAND | wx.ALL, 15)
        self.SetSizer(box);
        self.SetBackgroundColour('#0074D9') #blue

class ConsolePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        box = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, label="Console", style=wx.ALIGN_LEFT)
        box.Add(text, 0, wx.EXPAND | wx.ALL, 15)
        self.SetSizer(box);
        self.SetBackgroundColour('#01FF70') #lime

class LocalDirPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        box = wx.BoxSizer(wx.VERTICAL)
        sp = wx.StandardPaths.Get()
        dirs = wx.GenericDirCtrl(self, wx.ID_ANY, sp.GetDocumentsDir(), wx.DefaultPosition, wx.Size(-1, -1), wx.DIRCTRL_3D_INTERNAL | wx.SUNKEN_BORDER, wx.EmptyString, 0)
        box.Add(dirs, 1, wx.EXPAND)
        self.SetSizer(box);
        self.SetBackgroundColour('#FF4136') #red

class RemoteDirPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        box = wx.BoxSizer(wx.VERTICAL)
        dirs = wx.GenericDirCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(-1, -1), wx.DIRCTRL_3D_INTERNAL | wx.SUNKEN_BORDER, wx.EmptyString, 0)
        box.Add(dirs, 1, wx.EXPAND)
        self.SetSizer(box);
        self.SetBackgroundColour('#85144b') #maroon
        
class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title)
        self.CreateUI()

    def CreateUI(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColou    r('#ffffff')

        rows = wx.BoxSizer(wx.VERTICAL)
        rows.Add(ToolbarPanel(panel), 0, wx.EXPAND)
        rows.Add(ConsolePanel(panel), 0, wx.EXPAND)
        dirs = wx.BoxSizer(wx.HORIZONTAL)
        dirs.Add(LocalDirPanel(panel), 1, wx.EXPAND)
        dirs.Add(RemoteDirPanel(panel), 1, wx.EXPAND) 
        rows.Add(dirs, 1, wx.EXPAND)
        panel.SetSizer(rows)
        

if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame(None, title='FTP Client')
    frame.Show()
    app.MainLoop()

