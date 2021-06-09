from qgis import gui, core
from qgis.utils import iface
from PyQt5 import QtCore, uic, QtWidgets, QtGui

class FreeHand:

    def __init__(self):
        self.names = [ 
            'dsgtools: free hand acquisition',
            'dsgtools: ferramenta de aquisição à mão livre'
        ]
        
    def execute(self):
        for a in gui.QgsGui.shortcutsManager().listActions():
            if not( a.text().lower() in self.names ):
                continue
            iface.activeLayer().startEditing()
            a.trigger()
            break