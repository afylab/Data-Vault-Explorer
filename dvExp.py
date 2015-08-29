"""
Author: Brunel Odegard
"""

from PyQt4 import QtCore as core, QtGui as gui
import sys,math,time

from components.widgets import simpleList,simpleText,checkBox,queryButton
from components.details import fileDetails

from functools import partial

def plist(l,delimeter=', '):
    s = ''
    for entry in l:
        s += str(entry) + delimeter
    if len(s) and len(delimeter):
        s = s[:-len(delimeter)]
    return s

class searchWidget(gui.QMainWindow):
    def __init__(self,ls=23,lw=192,lh=23*3,ch=16):
        super(searchWidget,self).__init__()

        self.ls=ls # line spacing
        self.lw=lw # list width
        self.lh=lh # list height
        self.ch=ch # checkbox height
        self.bw=74 # button width

        self.lew = self.lw + self.bw + self.ls           # ListEditWidth  incl. margin
        self.leh = self.lh + self.ls + self.ch + self.ls # ListEditHeight incl. margin

        self.resize(self.lew*3 - self.ls,self.leh*3 - self.ls)
        self.doUI()

    def doUI(self):
        self.label_searchfor = simpleText(self,'Search for:',[0,0,self.bw,self.ls])
        self.cb_files   = checkBox(self,'files'  ,[0,self.ls*1])
        self.cb_folders = checkBox(self,'folders',[0,self.ls*2])
        self.button_go  = queryButton("Search",self,'',[0,self.ls*3],self.go)
        self.setWindowTitle("Data Vault search engine")

        # list edits
        self.s_tags     = stringListEdit(self,'In tags',[self.lew*1,self.leh*0])
        self.s_filename = stringListEdit(self,'In name',[self.lew*2,self.leh*0])

        self.s_units    = stringListEdit(self,'has units'    ,[self.lew*0,self.leh*1])
        self.s_varname  = stringListEdit(self,'Variable name',[self.lew*0,self.leh*2])

        self.s_param_name   = stringListEdit(self,"Parameter name"  ,[self.lew*1,self.leh*1])
        self.s_param_units  = stringListEdit(self,"Parameter units" ,[self.lew*1,self.leh*2])
        
        self.s_in_comment   = stringListEdit(self,"In comment"      ,[self.lew*2,self.leh*1])
        self.s_comment_user = stringListEdit(self,"Has comment user",[self.lew*2,self.leh*2])

        self.show()

    def go(self):
        pass
        

class stringListEdit(gui.QWidget):
    def __init__(self,parent,cbLabel,pos,ls=23,lw=192,lh=23*3,ch=16):
        super(stringListEdit,self).__init__(parent)
        self.cbLabel = cbLabel

        self.ls=ls # line spacing
        self.lw=lw # list width
        self.lh=lh # list height
        self.ch=ch # checkbox height

        self.bw=74
        self.setGeometry(pos[0],pos[1],lw+self.bw,lh+ls+ch)

        self.doUI()
    def doUI(self):
        self.cbEnabled   = checkBox(self,self.cbLabel,[0,0])
        self.activeList  = simpleList(self,[0,self.ch,self.lw,self.lh],[])
        self.inputString = simpleText(self,"",[0,self.ch+self.lh,self.lw-self.bw,self.ls])
        self.inputString.setReadOnly(False)

        self.buttonAdd = queryButton('remove',self,'',[self.lw,self.ch]                ,self.rem)
        self.buttonRem = queryButton('clear' ,self,'',[self.lw,self.lh+self.ch-self.ls],self.clr)
        self.buttonClr = queryButton('add'   ,self,'',[self.lw-self.bw,self.lh+self.ch],self.add)

    def add(self):
        entry = self.inputString.toPlainText()
        if entry != '':
            self.inputString.setText("")
            if not (entry in self.activeList.items):
                self.activeList.add_item(entry)
        self.inputString.setFocus()
    def rem(self):
        if len(self.activeList.items)>0:
            sel = self.activeList.currentRow()
            if sel>=0:
                self.activeList.remove_item(self.activeList.items[sel])
    def clr(self):
        self.activeList.change_items([])


class interface(gui.QMainWindow):
    def __init__(self,ls=23,lw=384,lh=128,th=34):
        super(interface,self).__init__()

        self.ls=ls # line spacing (height of a line of text)
        self.lw=lw # list width   (length of a list object)
        self.lh=lh # list height  (height of a list object)
        self.th=th # toolbar height
        self.bl=74 # button length

        self.path = ['']


        self.connect()

    def connect(self):
        import labrad
        firstAttempt=True
        success=connect=False
        while not success:
            if firstAttempt:pwd,ok=gui.QInputDialog.getText(self,"Password","Enter LabRAD password")
            else:pwd,ok=gui.QInputDialog.getText(self,"Password","Something went wrong. Either thepassword\nwas incorrect or LabRAD isn't running.")
            try:
                self.connection = labrad.connect(password = str(pwd))
                self.dv = self.connection.data_vault
                success=True;connect=True
            except:
                if pwd=='exit':success=True
            firstAttempt=False
        if connect:
            self.doUI()
        else:
            gui.qApp.quit()

    def up(self):
        '''Returns one level up in registry'''
        if len(self.path)>1: # don't do it if we're already in root
            self.path=self.path[:-1]
            self.dv.cd(self.path)
            self.update_lists()

    def go(self,folder):
        self.path.append(folder)
        self.dv.cd(self.path)
        self.update_lists()

    def home(self):
        self.path = ['']
        self.dv.cd(self.path)
        self.update_lists()

    def goto_folder(self):
        folder = self.list_folders.get_selected()
        self.go(folder)

    def update_lists(self):
        dir_contents = self.dv.dir()
        self.list_folders.change_items(dir_contents[0])
        self.list_files.change_items(dir_contents[1])
        label = "current dir: root"
        for subfolder in self.path[1:]:
            label+='\\%s'%subfolder
        self.label_dir.setText(label)

    def doUI(self):
        # size
        self.resize(self.lw+self.lh,self.lh*2+self.ls*4)

        # toolbar buttons
        self.toolbar = self.addToolBar('nan')
        self.toolbar.setMovable(False)

        homeAction = gui.QAction(gui.QIcon('resources\\images\\home.png'),'Home',self)
        homeAction.setShortcut('Ctrl+H')
        homeAction.triggered.connect(self.home)

        upAction = gui.QAction(gui.QIcon('resources\\images\\up.png'),'Up',self)
        upAction.setShortcut('Ctrl+U')
        upAction.triggered.connect(self.up)

        searchAction = gui.QAction(gui.QIcon('resources\\images\\search.png'),'Search',self)
        searchAction.setShortcut('Ctrl+F')
        searchAction.triggered.connect(self.search)

        self.toolbar.addAction(homeAction)
        self.toolbar.addAction(upAction)
        self.toolbar.addAction(searchAction)

        # current directory label
        self.label_dir = simpleText(self,"current dir: root",[0,self.th,self.lw,self.ls])

        # current directory list
        dir_contents = self.dv.dir()
        self.label_folders = simpleText(self,"Folders",[0,self.th+self.ls*1,self.lw,self.ls])
        self.list_folders  = simpleList(self,[0,self.th+self.ls*2+self.lh*0,self.lw,self.lh],dir_contents[0])
        self.list_folders.itemDoubleClicked.connect(self.goto_folder)
        
        self.label_folders = simpleText(self,"Files",[0,self.th+self.ls*3+self.lh,self.lw,self.ls])
        self.list_files    = simpleList(self,[0,self.th+self.ls*4+self.lh*1,self.lw,self.lh],dir_contents[1])

        # folder info
        self.label_folder_info = simpleText(self,"Folder info",[self.lw+self.ls,self.th+self.ls*1,self.lw,self.ls])
        self.folder_info       = simpleList(self,              [self.lw+self.ls,self.th+self.ls*2,self.lw,self.lh],[])

        # file info
        self.label_file_info = simpleText(self,"File info",[self.lw+self.ls,self.th+self.ls*3+self.lh,self.lw-self.bl,self.ls])
        self.file_info       = simpleList(self,            [self.lw+self.ls,self.th+self.ls*4+self.lh,self.lw,self.lh],[])

        # Details button
        self.button_show_details = queryButton('Show details',self,'',[self.lw*2+self.ls-self.bl,self.th+self.ls*3+self.lh],self.show_details)

        # window title
        self.setWindowTitle("Data Vault Explorer")
        
        self.resize(self.lw*2 + self.ls,self.lh*2 + self.ls*4 + self.th)
        self.show()
        
        self.timer = core.QTimer(self)
        self.timer.setInterval(25)
        self.timer.timeout.connect(self.timer_event)
        self.timer.start()

        self.selected_folder = ""
        self.selected_file   = ""

    def timer_event(self):
        sel_folder = self.list_folders.get_selected()
        sel_file  = self.list_files.get_selected()

        if sel_folder != self.selected_folder:
            self.selected_folder = sel_folder
            self.update_folder_info(sel_folder)

        if sel_file != self.selected_file:
            self.selected_file = sel_file
            self.update_file_info(sel_file)

    def update_file_info(self,sel_file):
        if sel_file != "":
            self.dv.open(sel_file)
            variables  = self.dv.variables()
            parameters = self.dv.parameters()
            name       = self.dv.get_name()
            comments   = self.dv.get_comments()
            users = []
            for comment in comments:
                if not comment[1] in users:
                    users.append(comment[1])
            
            tags       = self.dv.get_tags([],[sel_file])[1][0][1]
            ts = ''
            for tag in tags:
                ts += tag+', '
            ts = ts[:-2]
            
            self.file_info.change_items([
                'Name: %s'%name,
                'Tags: %s'%ts,
                'Independents: %s'%plist([c[0] for c in variables[0]]),
                'Dependents: %s'%plist([c[0] for c in variables[1]]),
                'Parameters: %s'%plist(parameters),
                'Comment count: %i'%len(comments),
                'Commenting users: %s'%plist(users)
                ])
        else:
            self.file_info.change_items([])
    
    def update_folder_info(self,sel_folder):
        if sel_folder != "":
            tags = self.dv.get_tags([sel_folder],[])[0][0][1]
            ts = ''
            for tag in tags:
                ts += tag+', '
            ts = ts[:-2]

            self.dv.cd(sel_folder)
            cont = self.dv.dir()
            self.dv.cd(self.path)

            subf_count = len(cont[0])
            file_count = len(cont[1])

            self.folder_info.change_items([
                "Name: %s"%sel_folder,
                "Tags: %s"%ts,
                "Subfolders: %i"%subf_count,
                "Files: %i"%file_count,
                ])
        else:
            self.folder_info.change_items([])

    def show_details(self):
        if self.selected_file == "":
            return

    def search(self):
        self.seeker = searchWidget()
        
        
        
        


if __name__=='__main__':
    app = gui.QApplication(sys.argv)
    i=interface()
    sys.exit(app.exec_())













