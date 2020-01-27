from ftplib import FTP
import wx

def Connect(url, user, passwd):
    ftp = FTP(url)
    ftp.login(user, passwd)
    wx.MessageBox(ftp.getwelcome())

class ToolbarPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        box = wx.BoxSizer(wx.HORIZONTAL)
        ftpUserText = wx.StaticText(self, -1, "User:")
        ftpPassText = wx.StaticText(self, -1, "Pass:")
        ftpUrlText = wx.StaticText(self, -1, "Url:")
        self.ftpUserCtrl = wx.TextCtrl(self, -1) 
        self.ftpPassCtrl = wx.TextCtrl(self, -1, style=wx.TE_PASSWORD)
        self.ftpUrlCtrl = wx.TextCtrl(self, -1)
        connectFtpBtn = wx.Button(self, -1, "Connect")
        connectFtpBtn.Bind(wx.EVT_BUTTON, self.OnConnectFtpBtnClick)
        box.Add(ftpUserText, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box.Add(self.ftpUserCtrl, 0, wx.EXPAND | wx.ALL, 5)
        box.Add(ftpPassText, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box.Add(self.ftpPassCtrl, 0, wx.EXPAND | wx.ALL, 5)
        box.Add(ftpUrlText, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box.Add(self.ftpUrlCtrl, 0, wx.EXPAND | wx.ALL, 5)
        box.Add(connectFtpBtn, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(box)
        self.SetBackgroundColour('#ececec')
    
    def OnConnectFtpBtnClick(self, e):
        username = self.ftpUserCtrl.GetValue()
        password = self.ftpPassCtrl.GetValue()
        url = self.ftpUrlCtrl.GetValue()
        Connect(url, username, password)

class ConsolePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        box = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, label="Console", style=wx.ALIGN_LEFT)
        box.Add(text, 0, wx.EXPAND | wx.ALL, 15)
        self.SetSizer(box)

class LocalDirPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        box = wx.BoxSizer(wx.VERTICAL)
        sp = wx.StandardPaths.Get()
        dirs = wx.GenericDirCtrl(self, wx.ID_ANY, sp.GetDocumentsDir(), wx.DefaultPosition, wx.Size(-1, -1), wx.DIRCTRL_3D_INTERNAL | wx.SUNKEN_BORDER, wx.EmptyString, 0)
        box.Add(dirs, 1, wx.EXPAND)
        self.SetSizer(box)

class RemoteDirPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        box = wx.BoxSizer(wx.VERTICAL)
        dirs = wx.GenericDirCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(-1, -1), wx.DIRCTRL_3D_INTERNAL | wx.SUNKEN_BORDER, wx.EmptyString, 0)
        box.Add(dirs, 1, wx.EXPAND)
        self.SetSizer(box)
        
class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=wx.Size(900, 500))
        self.CreateUI()

    def CreateUI(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#ffffff')
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