# -*- coding: utf-8 -*-
import os
from qgis.utils import iface
from qgis import core, gui
from PyQt5 import QtCore, QtGui, QtWidgets
from .dialog import Dialog

class Main:

    def __init__(self, iface):
        self.iface = iface
        self.dlg = Dialog()

    def initGui(self):
        self.toolBar = self.iface.addToolBar('teste')
        self.radilaMenuAction = self.createAction(
            "Menu Radial", 
            os.path.join(
                os.path.abspath(os.path.join(
                    os.path.dirname(__file__)
                )),
                'icons',
                'radialmenu.svg'
            ), 
            self.showRadialMenu
        )

    def createAction(self, text, iconPath, callback):
        action = QtWidgets.QAction(
            QtGui.QIcon(iconPath),
            text,
            self.iface.mainWindow()
        )
        self.toolBar.addAction(action)
        iface.registerMainWindowAction(action, "'")
        action.triggered.connect(callback)
        return action

    def unload(self):
        self.iface.mainWindow().removeToolBar(self.toolBar)
    
    def showRadialMenu(self):
        if not isinstance(iface.activeLayer(), core.QgsVectorLayer):
            return
        self.dlg.updatePosition( QtGui.QCursor.pos() )
        self.dlg.loadConfig()
        self.dlg.show()
        self.dlg.activateWindow()        
    
