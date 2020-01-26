from ftplib import FTP
import wx

def getFTPUrl():
    f = open('creds.txt', 'r')
    content = f.read().split(":")
    f.close()
    return content[0]

def getFTPUser():
    f = open('creds.txt', 'r')
    content = f.read().split(":")
    f.close()
    return content[1]

def getFTPPass():
    f = open('creds.txt', 'r')
    content = f.read().split(":")
    f.close()
    return content[2]

class ToolbarPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        box = wx.BoxSizer(wx.HORIZONTAL)
        connectFtpBtn = wx.Button(self, -1, "Connect")
        ftpUserText = wx.StaticText(self, -1, "User:")
        ftpPassText = wx.StaticText(self, -1, "Pass:")
        ftpUrlText = wx.StaticText(self, -1, "Url:")
        ftpUserCtrl = wx.TextCtrl(self, -1) 
        ftpPassCtrl = wx.TextCtrl(self, -1)
        ftpUrlCtrl = wx.TextCtrl(self, -1)
        box.Add(ftpUserText, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box.Add(ftpUserCtrl, 0, wx.EXPAND | wx.ALL, 5)
        box.Add(ftpPassText, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box.Add(ftpPassCtrl, 0, wx.EXPAND | wx.ALL, 5)
        box.Add(ftpUrlText, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box.Add(ftpUrlCtrl, 0, wx.EXPAND | wx.ALL, 5)
        box.Add(connectFtpBtn, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(box)
        self.SetBackgroundColour('#ececec') #blue

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
        super(MainFrame, self).__init__(parent, title=title)
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