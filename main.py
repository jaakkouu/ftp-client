import sys 
import os
import ftplib   
import wx   
from wx import dataview

class ToolbarPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        box = wx.BoxSizer(wx.HORIZONTAL)
        ftpUserText = wx.StaticText(self, -1, "User: ")
        ftpPassText = wx.StaticText(self, -1, "Pass: ")
        ftpUrlText = wx.StaticText(self, -1, "Url: ")
        self.ftpUserCtrl = wx.TextCtrl(self, -1) 
        self.ftpPassCtrl = wx.TextCtrl(self, -1, style=wx.TE_PASSWORD)
        self.ftpUrlCtrl = wx.TextCtrl(self, -1)
        self.connectFtpBtn = wx.Button(self, -1, "Connect")
        self.abortConnBtn = wx.Button(self, -1, "Abort Connection")
        self.abortConnBtn.Hide()
        self.connectFtpBtn.Bind(wx.EVT_BUTTON, self.OnConnectFtpBtnClick)
        self.abortConnBtn.Bind(wx.EVT_BUTTON, self.OnAbortConnBtnClick)
        box.Add(ftpUserText, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box.Add(self.ftpUserCtrl, 0, wx.EXPAND | wx.ALL, 5)
        box.Add(ftpPassText, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box.Add(self.ftpPassCtrl, 0, wx.EXPAND | wx.ALL, 5)
        box.Add(ftpUrlText, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        box.Add(self.ftpUrlCtrl, 0, wx.EXPAND | wx.ALL, 5)
        box.Add(self.connectFtpBtn, 0, wx.EXPAND | wx.ALL, 5)
        box.Add(self.abortConnBtn, 0, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(box)
        self.SetBackgroundColour('#ececec')
    
    def OnConnectFtpBtnClick(self, e):
        user = self.ftpUserCtrl.GetValue()
        passwd = self.ftpPassCtrl.GetValue()
        url = self.ftpUrlCtrl.GetValue()
        if len(user) == 0:
            wx.MessageBox("Please provide username", "Connection Error", wx.ICON_ERROR)
        elif len(passwd) == 0:
            wx.MessageBox("Please provide password", "Connection Error", wx.ICON_ERROR)
        elif len(url) == 0:
            wx.MessageBox("Please provide url", "Connection Error", wx.ICON_ERROR)
        else:
            self.TopLevelParent.ConnectFtp(self, url, user, passwd)
    
    def OnAbortConnBtnClick(self, e):
        self.TopLevelParent.ftp.quit()
        wx.MessageBox("Connection has been closed successfully!", "Connection Closed", wx.ICON_INFORMATION)
        self.connectFtpBtn.Show()
        self.abortConnBtn.Hide()
        self.TopLevelParent.remoteDirPanel.clearView()
        self.Layout()

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
        self.files = self.getListOfItemsInDirectory(self)
        self.localDirs = wx.dataview.DataViewListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_HORIZ_RULES)
        self.localDirs.AppendTextColumn('Filename')
        self.localDirs.AppendTextColumn('Type') 
        self.localDirs.AppendTextColumn('Size') 
        self.updateDirectory(self)
        box.Add(self.localDirs, 1, wx.EXPAND)
        self.SetSizer(box)

    def getListOfItemsInDirectory(self, event=None):
        items = []
        sp = wx.StandardPaths.Get()
        documentsDir = sp.GetDocumentsDir()
        for entry in os.listdir(documentsDir):
            if os.path.isfile(os.path.join(documentsDir, entry)): 
                itemType = "Folder" 
            else:
                itemType = "File"
            items.append((entry, itemType, "?"))
        return items

    def updateDirectory(self, event=None):
        files = self.files
        for f in files:
            self.localDirs.AppendItem(f)
        

class RemoteDirPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        box = wx.BoxSizer(wx.VERTICAL)
        self.remoteDirs = wx.dataview.DataViewListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.dataview.DV_HORIZ_RULES)
        self.remoteDirs.AppendTextColumn('Filename')
        self.remoteDirs.AppendTextColumn('Type') 
        self.remoteDirs.AppendTextColumn('Size') 
        box.Add(self.remoteDirs, 1, wx.EXPAND)
        self.SetSizer(box)

    def updateDirectory(self, event=None):
        files = []
        line = self.TopLevelParent.ftp.retrlines("NLST", files.append)
        files.pop(0) # Remove first item "."
        files.pop(0) # Remove first item again ".."
        for f in files:
            item = (f, "Folder", "?")
            self.remoteDirs.AppendItem(item)

    def clearView(self, event=None):
        self.remoteDirs.DeleteAllItems()

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=wx.Size(900, 500))
        self.ftp = None
        self.CreateUI()

    def CreateUI(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#ffffff')
        rows = wx.BoxSizer(wx.VERTICAL)
        dirs = wx.BoxSizer(wx.HORIZONTAL)
        self.toolbarPanel = ToolbarPanel(panel)
        self.consolePanel = ConsolePanel(panel)
        self.localDirPanel = LocalDirPanel(panel)
        self.remoteDirPanel = RemoteDirPanel(panel)
        rows.Add(self.toolbarPanel, 0, wx.EXPAND)
        rows.Add(self.consolePanel, 0, wx.EXPAND)
        dirs.Add(self.localDirPanel, 1, wx.EXPAND)
        dirs.Add(self.remoteDirPanel, 1, wx.EXPAND) 
        rows.Add(dirs, 1, wx.EXPAND)
        panel.SetSizer(rows)

    def ConnectFtp(self, toolbarPanel, url, user, passwd, event=None):
        self.ftp = ftplib.FTP(url)
        try:
            self.ftp.login(user, passwd)
            wx.MessageBox(self.ftp.getwelcome(), "Connection Success", wx.ICON_INFORMATION)
            self.remoteDirPanel.updateDirectory(self)
            toolbarPanel.connectFtpBtn.Hide()
            toolbarPanel.abortConnBtn.Show()
            toolbarPanel.Layout()
        except ftplib.all_errors as e:
            error = str(e).split(None, 1)[0]
            wx.MessageBox(error, "Connection Error", wx.ICON_EXCLAMATION)
     
if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame(None, title='FTP Client')
    frame.Show()
    app.MainLoop()

    