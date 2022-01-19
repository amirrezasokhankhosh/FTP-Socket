import socket
import wx
import os


class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Client')
        
        panel = wx.Panel(self)
        
        st1 = wx.StaticText(panel, label='Input', pos=(5, 5))
        self.text_ctrl = wx.TextCtrl(panel, pos=(5, 25))
        
        client_btn = wx.Button(panel, label='Update Client\'s Directory', pos=(5, 75))
        client_btn.Bind(wx.EVT_BUTTON, self.on_press_client)
        
        list_btn = wx.Button(panel, label='List', pos=(5, 125))
        list_btn.Bind(wx.EVT_BUTTON, self.on_press_list)
        
        stor_btn = wx.Button(panel, label='STOR', pos=(5, 175))
        stor_btn.Bind(wx.EVT_BUTTON, self.on_press_stor)
        
        retr_btn = wx.Button(panel, label='RETR', pos=(5, 225))
        retr_btn.Bind(wx.EVT_BUTTON, self.on_press_retr)
        
        st2 = wx.StaticText(panel, label='Server\'s Directory', pos=(200, 5))
        self.text_s = wx.TextCtrl(panel,style = wx.TE_MULTILINE, pos = (200, 25), size = (150, 300))
        
        st3 = wx.StaticText(panel, label='Client\'s Directory', pos=(400, 5))
        self.text_c = wx.TextCtrl(panel,style = wx.TE_MULTILINE, pos = (400, 25), size = (150, 300))
        
        st4 = wx.StaticText(panel, label='Progress', pos=(600, 5))
        self.text = wx.TextCtrl(panel,style = wx.TE_MULTILINE, pos = (600, 25), size = (450, 300))
        self.Show()
        
    def on_press_list(self, event):
        data = stablish_connection("list", "")
        self.text_s.Clear()
        for item in data:
            self.text_s.AppendText(str(item) + '\n')
    
    def on_press_stor(self, event):
        filename = self.text_ctrl.GetValue()
        stablish_connection("stor", filename)
        
    def on_press_retr(self, event):
        filename = self.text_ctrl.GetValue()
        stablish_connection("retr", filename)
        
    def on_press_client(self, event):
        directory = os.listdir('./')
        self.text_c.Clear()
        for item in directory:
            self.text_c.AppendText(str(item) + '\n')
            



def list_cmd(s):
    s.send("list".encode(FORMAT))
    frame.text.AppendText("[LIST]\n")
    data = s.recv(SIZE).decode(FORMAT).split()
    frame.text.AppendText("[LIST RECIEVED]\n")
    return data


def retr_cmd(s, filename):
    s.send("RETR {}".format(filename).encode(FORMAT))
    frame.text.AppendText("[RETR {}]\n".format(filename))
    data = s.recv(SIZE).decode(FORMAT)
    frame.text.AppendText("[DATA RECIEVED]\n")
    file = open('./{}'.format(filename), 'w')
    file.write(data)
    file.close()


def stor_cmd(s, filename):
    s.send("STOR {}".format(filename).encode(FORMAT))
    frame.text.AppendText("[STOR {}]\n".format(filename))
    file = open('./{}'.format(filename), 'r')
    data = file.read()
    s.send(data.encode(FORMAT))
    frame.text.AppendText("[DATA SENT]\n")


def stablish_connection(func, filename):
    data = []
    frame.text.AppendText("\n")
    s = socket.socket()
    s.connect((IP, PORT))
    frame.text.AppendText("[CONNECTED] Clinet is now connected to the server.\n")
    if func == "list":
        data = list_cmd(s)
    elif func == "retr":
        retr_cmd(s, filename)
    elif func == "stor":
        stor_cmd(s, filename)
    s.close()
    frame.text.AppendText("[CONNECTION CLOSED]\n")
    frame.text.AppendText("\n")
    return data



PORT = 12345
IP = '127.0.0.1'
FORMAT = 'utf-8'
SIZE = 1024



if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
    