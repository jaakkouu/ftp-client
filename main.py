import sys
import os
import ftplib
import time
from myvars import *
from dateutil import parser
import wx
from wx import dataview

class ToolbarPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        box = wx.BoxSizer(wx.HORIZONTAL)
        ftpUserText = wx.StaticText(self, -1, "User: ")
        ftpPassText = wx.StaticText(self, -1, "Pass: ")
        ftpUrlText = wx.StaticText(self, -1, "Url: ")
        if 'g_user' in globals():
            self.ftpUserCtrl = wx.TextCtrl(self, -1, value=g_user) 
        else:
            self.ftpUserCtrl = wx.TextCtrl(self, -1) 
        if 'g_pass' in globals():
            self.ftpPassCtrl = wx.TextCtrl(self, -1, value=g_pass, style=wx.TE_PASSWORD) 
        else:
            self.ftpPassCtrl = wx.TextCtrl(self, -1, style=wx.TE_PASSWORD) 
        if 'g_url' in globals():
            self.ftpUrlCtrl = wx.TextCtrl(self, -1, value=g_url) 
        else:
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
        self.TopLevelParent.consolePanel.LogMessage("Connection has been closed successfully!")
        self.connectFtpBtn.Show()
        self.abortConnBtn.Hide()
        self.TopLevelParent.remoteDirPanel.clearView()
        self.Layout()

class ConsolePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        box = wx.BoxSizer(wx.VERTICAL)
        self.logBox = wx.TextCtrl(self, wx.ID_ANY, size=(0,100), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        box.Add(self.logBox, 0, wx.EXPAND|wx.ALL)
        self.SetSizer(box)
        
    def LogMessage(self, message):
        self.logBox.AppendText(message + "\n")

    def ClearMessage(self):
        self.logBox.Clear()

class LocalDirPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        box = wx.BoxSizer(wx.VERTICAL)
        self.localDirs = wx.dataview.DataViewListCtrl(self)
        self.localDirs.Bind(wx.dataview.EVT_DATAVIEW_ITEM_ACTIVATED, self.onItemClick)
        self.localDirs.AppendTextColumn('File')
        self.localDirs.AppendTextColumn('Filesize')
        self.localDirs.AppendTextColumn('Filetype')
        self.localDirs.AppendTextColumn('Last modified')
        itemsInDir = self.getItemsFromDir(self.localDirs.TopLevelParent.localDirPath)
        self.updateDirectory(itemsInDir)
        box.Add(self.localDirs, 1, wx.EXPAND)
        self.SetSizer(box)

    def getItemsFromDir(self, dirPath, event=None):
        # TODO Add file and folder validation
        items = []
        for entry in os.listdir(dirPath):
            entryPath = os.path.join(dirPath, entry)
            if os.path.isdir(entryPath):
                iType = "File folder"
            elif os.path.isfile(entryPath):
                iType = "file"
            lastModified = time.strftime('%d-%m-%Y %H:%M:%S', time.gmtime(os.path.getmtime(entryPath)))
            iSize = os.path.getsize(entryPath)
            items.append((entry, iSize, iType, lastModified))
        return items

    def onItemClick(self, event):
        # TODO Add file and folder validation
        selectedRowIndex = self.localDirs.GetSelectedRow()
        selectedItem = self.localDirs.RowToItem(selectedRowIndex)
        fileName = self.localDirs.GetValue(selectedRowIndex, 0)
        fileSize = self.localDirs.GetValue(selectedRowIndex, 1)
        fileType = self.localDirs.GetValue(selectedRowIndex, 2)
        localDirPath = self.localDirs.TopLevelParent.localDirPath
        remoteDirPath = self.localDirs.TopLevelParent.remoteDirPath
        if fileType == "file":
            self.TopLevelParent.consolePanel.LogMessage('Starting upload of ' + fileName)
            fileToSave = open(localDirPath + "\\" + fileName, 'rb')
            self.TopLevelParent.ftp.storbinary('STOR %s' % fileName, fileToSave)
            self.TopLevelParent.consolePanel.LogMessage('File transfer successful, transferred ' + fileSize + ' bytes')
        else:
            if fileName == "..":
                currentPathList = localDirPath.split("\\")
                del currentPathList[-1]
                separator = "\\"
                currentPath = separator.join(currentPathList)
            else:
                currentPath = localDirPath + "\\" + fileName

            self.localDirs.TopLevelParent.SetLocalDirPath(currentPath)
            itemsInDir = self.getItemsFromDir(self.localDirs.TopLevelParent.localDirPath)
            self.updateDirectory(itemsInDir)

    def updateDirectory(self, items, event=None):
        self.clearView()
        self.localDirs.AppendItem(("..", "", "", ""))
        for item in items:
            self.localDirs.AppendItem(item)
    
    def clearView(self, event=None):
        self.localDirs.DeleteAllItems()
        
class RemoteDirPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        box = wx.BoxSizer(wx.VERTICAL)
        self.remoteDirs = wx.dataview.DataViewListCtrl(self)
        self.remoteDirs.Bind(wx.dataview.EVT_DATAVIEW_ITEM_ACTIVATED, self.onItemClick)
        self.remoteDirs.AppendTextColumn('File')
        self.remoteDirs.AppendTextColumn('Filesize')
        self.remoteDirs.AppendTextColumn('Filetype')
        self.remoteDirs.AppendTextColumn('Last modified')
        self.remoteDirs.AppendTextColumn('Permissions')
        self.remoteDirs.AppendTextColumn('Owner/Group')
        box.Add(self.remoteDirs, 1, wx.EXPAND)
        self.SetSizer(box)

    def onItemClick(self, event):
        # TODO Add file and folder validation
        selectedRowIndex = self.remoteDirs.GetSelectedRow()
        selectedItem = self.remoteDirs.RowToItem(selectedRowIndex)
        fileName = self.remoteDirs.GetValue(selectedRowIndex, 0)
        fileSize = self.remoteDirs.GetValue(selectedRowIndex, 1)
        fileType = self.remoteDirs.GetValue(selectedRowIndex, 2)
        currentPath = self.TopLevelParent.ftp.pwd() + "/"
        if fileType == "file":
            currentPath = self.remoteDirs.TopLevelParent.localDirPath + "\\" + fileName
            pathToSave = open(currentPath, 'wb')
            self.TopLevelParent.consolePanel.LogMessage('Starting download of ' + fileName)
            self.TopLevelParent.ftp.retrbinary('RETR %s' % fileName, pathToSave.write)
            self.TopLevelParent.consolePanel.LogMessage('File transfer successful, transferred ' + fileSize + ' bytes')
        else:
            self.TopLevelParent.ftp.cwd(currentPath + fileName)
            self.TopLevelParent.consolePanel.LogMessage('Retrieving directory listing of "/' + fileName + '"...')
            self.updateDirectory(self)
            self.TopLevelParent.consolePanel.LogMessage('Directory listing of "/' + fileName + '"  successful')

    def parseDirectoryIntoArray(self, lines, event=None):
        files = []
        for line in lines:
            row = line.split(";")
            item = {}
            index = 0
            for column in row:
                columnRow = column.split("=")
                if(index != 7):
                    item[columnRow[0]] = columnRow[1]
                else: # last item in array is the name
                    item["name"] = columnRow[0].strip()
                index += 1
            files.append(item)
        return files

    def updateDirectory(self, event=None):
        self.clearView()
        lines = []
        self.TopLevelParent.ftp.retrlines('MLSD', lines.append)
        lines.pop(0) # remove the first item "."
        items = self.parseDirectoryIntoArray(lines)
        for item in items:
            if item['type'] == 'file': 
                x = getFileItem(item)
            else: 
                x = getFolderItem(item)
            self.remoteDirs.AppendItem(x)

    def clearView(self, event=None):
        self.remoteDirs.DeleteAllItems()

class MainFrame(wx.Frame):
    # TODO Add status bar for frame to show connectivity information
    # TODO Add settings menu

    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=wx.Size(1000, 500))
        sp = wx.StandardPaths.Get()
        self.ftp = None
        # TODO Add ability to change and save starting folder for later use
        self.SetLocalDirPath(sp.GetDocumentsDir())
        self.CreateUI()

    def SetLocalDirPath(self, path):
        self.localDirPath = path

    def SetRemoteDirPath(self, path):
        self.remoteDirPath = path

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
        self.TopLevelParent.consolePanel.LogMessage("Connecting to " + url)
        try:
            self.ftp.login(user, passwd)
            self.TopLevelParent.consolePanel.LogMessage("Connection success!")
            self.TopLevelParent.consolePanel.LogMessage(self.ftp.getwelcome())
            self.TopLevelParent.SetRemoteDirPath(self.ftp.pwd())
            self.remoteDirPanel.updateDirectory(self)
            toolbarPanel.connectFtpBtn.Hide()
            toolbarPanel.abortConnBtn.Show()
            toolbarPanel.Layout()
        except ftplib.all_errors as e:
            error = str(e).split(None, 1)[0]
            self.TopLevelParent.consolePanel.LogMessage("Connection was unsuccesful")
            self.TopLevelParent.consolePanel.LogMessage(error)

def getFileItem(item):
    lastModified = str(parser.parse(item['modify']))
    return (
        item['name'],
        item['size'],
        item['type'],
        lastModified,
        item['UNIX.mode'],
        item['UNIX.uid'] + " " + item['UNIX.gid']
    )

def getFolderItem(item):
    lastModified = str(parser.parse(item['modify']))
    return (
        item['name'],
        item['sizd'],
        item['type'],
        lastModified,
        item['UNIX.mode'],
        item['UNIX.uid'] + " " + item['UNIX.gid']
    )

if __name__ == '__main__':
    # TODO Add visuals
    app = wx.App(False)
    frame = MainFrame(None, title='FTP Client')
    frame.Show()
    app.MainLoop()