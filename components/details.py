import sys
from PyQt4 import QtCore as core, QtGui as gui
from widgets import simpleText,simpleList,queryButton

class fileDetails(gui.QDialog):
    def __init__(self,parent,data,
                 overview_label_length  = 96,
                 overview_value_length  = 192,
                 comments_user_length   = 192,
                 parameters_name_length = 384,

                 line_spacing = 23,
                 ):
        super(fileDetails,self).__init__(parent)

        self.data = data

        self.oll = overview_label_length
        self.ovl = overview_value_length
        self.cul = comments_user_length
        self.pnl = parameters_name_length
        self.width = self.oll*2 + self.ovl*2 + line_spacing

        self.ls     = line_spacing
        self.height = self.ls * 11

        self.doUI()

    def doUI(self):
        self.setModal(True)
        self.setWindowTitle("File details")

        self.tabs = gui.QTabWidget(self)
        self.tabs.move(0,0)
        self.tabs.setMinimumSize(self.width,self.height)
        self.setFixedSize(self.width-2,self.height-1)

        self.overview   = overviewWidget(   self.data, self.ls, self.oll, self.ovl, self.height)
        self.parameters = parametersWidget( self.data, self.ls, self.pnl, self.width           )
        self.comments   = commentsWidget(   self.data, self.ls, self.cul, self.width           )

        self.tabs.addTab(self.overview  , "Overview"  )
        self.tabs.addTab(self.parameters, "Parameters")
        self.tabs.addTab(self.comments  , "Comments"  )

        self.show()

class overviewWidget(gui.QWidget):
    def __init__(self,data,ls,ll,vl,height):
        super(overviewWidget,self).__init__(None)
        self.ls=ls
        self.ll=ll
        self.vl=vl
        self.height = height
        self.doUI()
    def doUI(self):
        self.label_name       = simpleText(self,"Name"           ,[0,self.ls*0,self.ll,self.ls])
        self.label_filenum    = simpleText(self,"File number"    ,[0,self.ls*1,self.ll,self.ls])
        self.label_location   = simpleText(self,"Location"       ,[0,self.ls*2,self.ll,self.ls])
        self.label_comments   = simpleText(self,"Comment count"  ,[0,self.ls*3,self.ll,self.ls])
        self.label_parameters = simpleText(self,"Parameter count",[0,self.ls*4,self.ll,self.ls])
        self.label_created    = simpleText(self,"Date created"   ,[0,self.ls*5,self.ll,self.ls])
        self.value_name       = simpleText(self,"",[self.ll,self.ls*0,self.vl,self.ls])
        self.value_filenum    = simpleText(self,"",[self.ll,self.ls*1,self.vl,self.ls])
        self.value_location   = simpleText(self,"",[self.ll,self.ls*2,self.vl,self.ls])
        self.value_comments   = simpleText(self,"",[self.ll,self.ls*3,self.vl,self.ls])
        self.value_parameters = simpleText(self,"",[self.ll,self.ls*4,self.vl,self.ls])
        self.value_created    = simpleText(self,"",[self.ll,self.ls*5,self.vl,self.ls])

        self.label_independents = simpleText(self,"Independents",[self.ll+self.vl+self.ls,self.ls*0,self.ll,self.ls])
        self.label_dependents   = simpleText(self,"Dependents"  ,[self.ll+self.vl+self.ls,self.ls*4,self.ll,self.ls])
        self.list_independents  = simpleList(self,[self.ll*2+self.vl+self.ls,self.ls*0,self.vl,self.ls*3],[])
        self.list_dependents    = simpleList(self,[self.ll*2+self.vl+self.ls,self.ls*4,self.vl,self.ls*3],[])

        self.button_export = queryButton("Export to CSV",self,'',[0,self.height - (self.ls + 25)],self.export)

    def export(self):
        pass

class parametersWidget(gui.QWidget):
    def __init__(self,data,ls,nl,width):
        super(parametersWidget,self).__init__(None)
        self.ls=ls
        self.nl=nl
        self.width=width
        self.doUI()
    def doUI(self):
        self.label_name  = simpleText(self,"Name (units)",[0      , 0, self.nl           , self.ls])
        self.label_value = simpleText(self,"Value"       ,[self.nl, 0, self.width-self.nl, self.ls])
        self.list_parameters = simpleList(self,[0,self.ls,self.width,self.ls*4],[])

class commentsWidget(gui.QWidget):
    def __init__(self,data,ls,ul,width):
        super(commentsWidget,self).__init__(None)
        self.ls=ls
        self.ul=ul
        self.width=width
        self.doUI()
    def doUI(self):
        self.label_user    = simpleText(self,"User / author",[0      , 0, self.ul             , self.ls])
        self.label_comment = simpleText(self,"Comment body" ,[self.ul, 0, self.width - self.ul, self.ls])
        self.list_comments = simpleList(self,[0,self.ls,self.width,self.ls*4],[])

    

test = True
if __name__ == '__main__' and test:
    app=gui.QApplication(sys.argv)
    t = fileDetails(None,None)
    sys.exit(app.exec_())

















