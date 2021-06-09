from PyQt5 import QtCore, uic, QtWidgets, QtGui
import os 
from radialMenu.factories.actionsFactory import ActionsFactory
from radialMenu.factories.iconsFactory import IconsFactory
from qgis.utils import iface
from qgis import core, gui

class Dialog(QtWidgets.QDialog):
    def __init__(
            self,
            actionsFactory=ActionsFactory(),
            iconsFactory=IconsFactory(),
            parent=None
        ):
        super(Dialog, self).__init__(parent=parent)
        uic.loadUi(self.getUiPath(), self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setModal(False)
        self.hideButtons()
        self.actionsFactory = actionsFactory
        self.iconsFactory = iconsFactory
        self.currentButtonConfigs = []
        self.setupButtons()

    def executeCallback(self, button):
        for config in self.currentButtonConfigs:
            if not( config['button'] == button ):
                continue
            config['action'].execute()
            break
        self.close()

    def loadConfig(self):
        geometryType = iface.activeLayer().geometryType()
        if  geometryType == core.QgsWkbTypes.PointGeometry:
            self.currentButtonConfigs = self.getPointConfig()
        elif  geometryType == core.QgsWkbTypes.LineGeometry:
            self.currentButtonConfigs = self.getLineConfig()
        else:
            self.currentButtonConfigs = self.getPolygonConfig()
        self.loadButtonsConfig( self.currentButtonConfigs )

    def getButtons(self):
        return [
            self.btn1,
            self.btn2,
            self.btn3,
            self.btn4,
            self.btn5,
            self.btn6,
            self.btn7,
            self.btn8
        ]

    def setupButtons(self):
        for b in self.getButtons():
            b.installEventFilter( self )
            b.clicked.connect( lambda b, button=b: self.executeCallback(button) )
            
    def hideButtons(self):
        for b in self.getButtons():
            b.setVisible(False)
            
    def loadButtonsConfig(self, configs):
        self.hideButtons()
        for config in configs:
            config['button'].setVisible(True)
            config['button'].setAutoFillBackground(True)
            config['button'].setFlat(True)
            config['button'].setIcon( config['iconDefault'] )
            config['button'].setIconSize( QtCore.QSize(120,60) )
            config['button'].setToolTip( config['toolTip'] )
            
    def eventFilter(self, btn, e):
        if e.type() == QtCore.QEvent.Enter:
            config = [ config for config in self.currentButtonConfigs if config['button'] == btn ][0]
            btn.setIcon( config['iconHover'] )
        if e.type() == QtCore.QEvent.Leave:
            config = [ config for config in self.currentButtonConfigs if config['button'] == btn ][0]
            btn.setIcon( config['iconDefault'] )
        if e.type() == QtCore.QEvent.Paint:
            return False
        return False

    """ def keyPressEvent(self, e):
        if not( e.key() == QtCore.Qt.Key_P):
            super().keyPressEvent(e)
            return
        self.close() """

    def getIconPath(self, name):
        return os.path.join(
            os.path.abspath(os.path.join(
                os.path.dirname(__file__)
            )),
            name
        )

    def updatePosition(self, point=QtGui.QCursor.pos()):
        self.move( point.x() - (self.width()/2), point.y() - (self.height()/2) )

    def getUiPath(self):
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'ui',
            'radialMenu.ui'
        )

    def getPointConfig(self):
        if iface.activeLayer().selectedFeatures():
            return [
                {
                    'name': 'LastLayer',
                    'button': self.btn1,
                    'iconHover': self.iconsFactory.getIcon( 'LastLayerHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'LastLayerDeafult' ),
                    'action': self.actionsFactory.getAction('LastLayer'),
                    'toolTip': 'Ir para última camada'
                },
                {
                    'name': 'SelectRaster',
                    'button': self.btn2,
                    'iconHover': self.iconsFactory.getIcon( 'SelectRasterHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'SelectRasterDefault' ),
                    'action': self.actionsFactory.getAction('SelectRaster'),
                    'toolTip': 'Mostrar apenas um raster'
                },
                {
                    'name': 'MoveFeature',
                    'button': self.btn3,
                    'iconHover': self.iconsFactory.getIcon( 'MoveFeatureHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'MoveFeatureDefault' ),
                    'action': self.actionsFactory.getAction('MoveFeature'),
                    'toolTip': 'Mover feição'
                },
                {
                    'name': 'MergeFeatureAttributes',
                    'button': self.btn4,
                    'iconHover': self.iconsFactory.getIcon( 'MergeFeatureAttributesHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'MergeFeatureAttributesDefault' ),
                    'action': self.actionsFactory.getAction('MergeFeatureAttributes'),
                    'toolTip': 'Mergear atributos'
                },
                {
                    'name': 'SetDefaultFields',
                    'button': self.btn5,
                    'iconHover': self.iconsFactory.getIcon( 'SetDefaultFieldsHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'SetDefaultFieldsDefault' ),
                    'action': self.actionsFactory.getAction('SetDefaultFields'),
                    'toolTip': 'Criar mais como esse'
                },
                {
                    'name': 'DeleteSelected',
                    'button': self.btn6,
                    'iconHover': self.iconsFactory.getIcon( 'DeleteSelectedHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'DeleteSelectedDefault' ),
                    'action': self.actionsFactory.getAction('DeleteSelected'),
                    'toolTip': 'Deleter seleção'
                },
                {
                    'name': 'OpenAttributeTableOnlySelection',
                    'button': self.btn7,
                    'iconHover': self.iconsFactory.getIcon( 'OpenAttributeTableHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'OpenAttributeTableDefault' ),
                    'action': self.actionsFactory.getAction('OpenAttributeTableOnlySelection'),
                    'toolTip': 'Abrir tabela de atributos (Apenas selecionados)'
                },
                {
                    'name': 'RestoreFields',
                    'button': self.btn8,
                    'iconHover': self.iconsFactory.getIcon( 'RestoreFieldsHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'RestoreFieldsDefault' ),
                    'action': self.actionsFactory.getAction('RestoreFields'),
                    'toolTip': 'Cancelar criar mais como esse'
                }
            ]
        return [
            {
                'name': 'LastLayer',
                'button': self.btn1,
                'iconHover': self.iconsFactory.getIcon( 'LastLayerHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'LastLayerDeafult' ),
                'action': self.actionsFactory.getAction('LastLayer'),
                'toolTip': 'Ir para última camada'
            },
            {
                'name': 'SelectRaster',
                'button': self.btn2,
                'iconHover': self.iconsFactory.getIcon( 'SelectRasterHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'SelectRasterDefault' ),
                'action': self.actionsFactory.getAction('SelectRaster'),
                'toolTip': 'Mostrar apenas um raster'
            },
            {
                'name': 'AddPointFeature',
                'button': self.btn3,
                'iconHover': self.iconsFactory.getIcon( 'AddPointFeatureHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'AddPointFeatureDefault' ),
                'action': self.actionsFactory.getAction('AddPointFeature'),
                'toolTip': 'Adicionar ponto'
            },
            {
                'name': 'SelectFeature',
                'button': self.btn4,
                'iconHover': self.iconsFactory.getIcon( 'SelectFeatureHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'SelectFeatureDefault' ),
                'action': self.actionsFactory.getAction('SelectFeature'),
                'toolTip': 'Selecionar feições'
            },
            {
                'name': 'SetFeatureInspector',
                'button': self.btn5,
                'iconHover': self.iconsFactory.getIcon( 'SetFeatureInspectorHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'SetFeatureInspectorDefault' ),
                'action': self.actionsFactory.getAction('SetFeatureInspector'),
                'toolTip': 'Inspecionar feição'
            },
            {
                'name': 'TopologicalSnapping',
                'button': self.btn6,
                'iconHover': self.iconsFactory.getIcon( 'TopologicalSnappingHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'TopologicalSnappingDefault' ),
                'action': self.actionsFactory.getAction('TopologicalSnapping'),
                'toolTip': 'Habilitar edição topológica'
            },
            {
                'name': 'OpenAttributeTable',
                'button': self.btn7,
                'iconHover': self.iconsFactory.getIcon( 'OpenAttributeTableHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'OpenAttributeTableDefault' ),
                'action': self.actionsFactory.getAction('OpenAttributeTable'),
                'toolTip': 'Abrir tabela de atributos'
            },
            {
                'name': 'RestoreFields',
                'button': self.btn8,
                'iconHover': self.iconsFactory.getIcon( 'RestoreFieldsHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'RestoreFieldsDefault' ),
                'action': self.actionsFactory.getAction('RestoreFields'),
                'toolTip': 'Cancelar criar mais como esse'
            }
        ]

    def getLineConfig(self):
        if iface.activeLayer().selectedFeatures():
            return [
                {
                    'name': 'LastLayer',
                    'button': self.btn1,
                    'iconHover': self.iconsFactory.getIcon( 'LastLayerHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'LastLayerDeafult' ),
                    'action': self.actionsFactory.getAction('LastLayer'),
                    'toolTip': 'Ir para última camada'
                },
                {
                    'name': 'SelectRaster',
                    'button': self.btn2,
                    'iconHover': self.iconsFactory.getIcon( 'SelectRasterHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'SelectRasterDefault' ),
                    'action': self.actionsFactory.getAction('SelectRaster'),
                    'toolTip': 'Mostrar apenas um raster'
                },
                {
                    'name': 'TrimExtendFeature',
                    'button': self.btn3,
                    'iconHover': self.iconsFactory.getIcon( 'TrimExtendFeatureHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'TrimExtendFeatureDefault' ),
                    'action': self.actionsFactory.getAction('TrimExtendFeature'),
                    'toolTip': 'Aparar/Extender feição'
                },
                {
                    'name': 'MergeFeatureAttributes',
                    'button': self.btn4,
                    'iconHover': self.iconsFactory.getIcon( 'MergeFeatureAttributesHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'MergeFeatureAttributesDefault' ),
                    'action': self.actionsFactory.getAction('MergeFeatureAttributes'),
                    'toolTip': 'Mergear atributos'
                },
                {
                    'name': 'SetDefaultFields',
                    'button': self.btn5,
                    'iconHover': self.iconsFactory.getIcon( 'SetDefaultFieldsHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'SetDefaultFieldsDefault' ),
                    'action': self.actionsFactory.getAction('SetDefaultFields'),
                    'toolTip': 'Criar mais como esse'
                },
                {
                    'name': 'DeleteSelected',
                    'button': self.btn6,
                    'iconHover': self.iconsFactory.getIcon( 'DeleteSelectedHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'DeleteSelectedDefault' ),
                    'action': self.actionsFactory.getAction('DeleteSelected'),
                    'toolTip': 'Deleter seleção'
                },
                {
                    'name': 'OpenAttributeTableOnlySelection',
                    'button': self.btn7,
                    'iconHover': self.iconsFactory.getIcon( 'OpenAttributeTableHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'OpenAttributeTableDefault' ),
                    'action': self.actionsFactory.getAction('OpenAttributeTableOnlySelection'),
                    'toolTip': 'Abrir tabela de atributos (Apenas selecionados)'
                },
                {
                    'name': 'RestoreFields',
                    'button': self.btn8,
                    'iconHover': self.iconsFactory.getIcon( 'RestoreFieldsHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'RestoreFieldsDefault' ),
                    'action': self.actionsFactory.getAction('RestoreFields'),
                    'toolTip': 'Cancelar criar mais como esse'
                }
            ]
        return [
            {
                'name': 'LastLayer',
                'button': self.btn1,
                'iconHover': self.iconsFactory.getIcon( 'LastLayerHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'LastLayerDeafult' ),
                'action': self.actionsFactory.getAction('LastLayer'),
                'toolTip': 'Ir para última camada'
            },
            {
                'name': 'SelectRaster',
                'button': self.btn2,
                'iconHover': self.iconsFactory.getIcon( 'SelectRasterHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'SelectRasterDefault' ),
                'action': self.actionsFactory.getAction('SelectRaster'),
                'toolTip': 'Mostrar apenas um raster'
            },
            {
                'name': 'FreeHand',
                'button': self.btn3,
                'iconHover': self.iconsFactory.getIcon( 'FreeHandHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'FreeHandDefault' ),
                'action': self.actionsFactory.getAction('FreeHand'),
                'toolTip': 'Aquisição mão livre'
            },
            {
                'name': 'CutFeatures',
                'button': self.btn4,
                'iconHover': self.iconsFactory.getIcon( 'CutFeaturesHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'CutFeaturesDefault' ),
                'action': self.actionsFactory.getAction('CutFeatures'),
                'toolTip': 'Cortar feições'
            },
            {
                'name': 'SetFeatureInspector',
                'button': self.btn5,
                'iconHover': self.iconsFactory.getIcon( 'SetFeatureInspectorHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'SetFeatureInspectorDefault' ),
                'action': self.actionsFactory.getAction('SetFeatureInspector'),
                'toolTip': 'Inspecionar feição'
            },
            {
                'name': 'TopologicalSnapping',
                'button': self.btn6,
                'iconHover': self.iconsFactory.getIcon( 'TopologicalSnappingHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'TopologicalSnappingDefault' ),
                'action': self.actionsFactory.getAction('TopologicalSnapping'),
                'toolTip': 'Habilitar edição topológica'
            },
            {
                'name': 'OpenAttributeTable',
                'button': self.btn7,
                'iconHover': self.iconsFactory.getIcon( 'OpenAttributeTableHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'OpenAttributeTableDefault' ),
                'action': self.actionsFactory.getAction('OpenAttributeTable'),
                'toolTip': 'Abrir tabela de atributos'
            },
            {
                'name': 'RestoreFields',
                'button': self.btn8,
                'iconHover': self.iconsFactory.getIcon( 'RestoreFieldsHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'RestoreFieldsDefault' ),
                'action': self.actionsFactory.getAction('RestoreFields'),
                'toolTip': 'Cancelar criar mais como esse'
            }
        ]

    def getPolygonConfig(self):
        if iface.activeLayer().selectedFeatures():
            return [
                {
                    'name': 'LastLayer',
                    'button': self.btn1,
                    'iconHover': self.iconsFactory.getIcon( 'LastLayerHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'LastLayerDeafult' ),
                    'action': self.actionsFactory.getAction('LastLayer'),
                    'toolTip': 'Ir para última camada'
                },
                {
                    'name': 'SelectRaster',
                    'button': self.btn2,
                    'iconHover': self.iconsFactory.getIcon( 'SelectRasterHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'SelectRasterDefault' ),
                    'action': self.actionsFactory.getAction('SelectRaster'),
                    'toolTip': 'Mostrar apenas um raster'
                },
                {
                    'name': 'FreeHandReshape',
                    'button': self.btn3,
                    'iconHover': self.iconsFactory.getIcon( 'FreeHandReshapeHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'FreeHandReshapeDefault' ),
                    'action': self.actionsFactory.getAction('FreeHandReshape'),
                    'toolTip': 'Reshape mão livre'
                },
                {
                    'name': 'MergeFeatureAttributes',
                    'button': self.btn4,
                    'iconHover': self.iconsFactory.getIcon( 'MergeFeatureAttributesHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'MergeFeatureAttributesDefault' ),
                    'action': self.actionsFactory.getAction('MergeFeatureAttributes'),
                    'toolTip': 'Mergear atributos'
                },
                {
                    'name': 'SetDefaultFields',
                    'button': self.btn5,
                    'iconHover': self.iconsFactory.getIcon( 'SetDefaultFieldsHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'SetDefaultFieldsDefault' ),
                    'action': self.actionsFactory.getAction('SetDefaultFields'),
                    'toolTip': 'Criar mais como esse'
                },
                {
                    'name': 'DeleteSelected',
                    'button': self.btn6,
                    'iconHover': self.iconsFactory.getIcon( 'DeleteSelectedHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'DeleteSelectedDefault' ),
                    'action': self.actionsFactory.getAction('DeleteSelected'),
                    'toolTip': 'Deleter seleção'
                },
                {
                    'name': 'OpenAttributeTableOnlySelection',
                    'button': self.btn7,
                    'iconHover': self.iconsFactory.getIcon( 'OpenAttributeTableHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'OpenAttributeTableDefault' ),
                    'action': self.actionsFactory.getAction('OpenAttributeTableOnlySelection'),
                    'toolTip': 'Abrir tabela de atributos (Apenas selecionados)'
                },
                {
                    'name': 'RestoreFields',
                    'button': self.btn8,
                    'iconHover': self.iconsFactory.getIcon( 'RestoreFieldsHover' ),
                    'iconDefault': self.iconsFactory.getIcon( 'RestoreFieldsDefault' ),
                    'action': self.actionsFactory.getAction('RestoreFields'),
                    'toolTip': 'Cancelar criar mais como esse'
                }
            ]
        return [
            {
                'name': 'LastLayer',
                'button': self.btn1,
                'iconHover': self.iconsFactory.getIcon( 'LastLayerHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'LastLayerDeafult' ),
                'action': self.actionsFactory.getAction('LastLayer'),
                'toolTip': 'Ir para última camada'
            },
            {
                'name': 'SelectRaster',
                'button': self.btn2,
                'iconHover': self.iconsFactory.getIcon( 'SelectRasterHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'SelectRasterDefault' ),
                'action': self.actionsFactory.getAction('SelectRaster'),
                'toolTip': 'Mostrar apenas um raster'
            },
            {
                'name': 'FreeHand',
                'button': self.btn3,
                'iconHover': self.iconsFactory.getIcon( 'FreeHandHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'FreeHandDefault' ),
                'action': self.actionsFactory.getAction('FreeHand'),
                'toolTip': 'Aquisição mão livre'
            },
            {
                'name': 'RightDegreeAngleDigitizing',
                'button': self.btn4,
                'iconHover': self.iconsFactory.getIcon( 'RightDegreeAngleDigitizingHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'RightDegreeAngleDigitizingDefault' ),
                'action': self.actionsFactory.getAction('RightDegreeAngleDigitizing'),
                'toolTip': 'Aquisição em ângulo reto'
            },
            {
                'name': 'DeleteRing',
                'button': self.btn5,
                'iconHover': self.iconsFactory.getIcon( 'DeleteRingHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'DeleteRingDefault' ),
                'action': self.actionsFactory.getAction('DeleteRing'),
                'toolTip': 'Deletar anel'
            },
            {
                'name': 'AddRing',
                'button': self.btn6,
                'iconHover': self.iconsFactory.getIcon( 'AddRingHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'AddRingDefault' ),
                'action': self.actionsFactory.getAction('AddRing'),
                'toolTip': 'Adicionar anel'
            },
            {
                'name': 'OpenAttributeTable',
                'button': self.btn7,
                'iconHover': self.iconsFactory.getIcon( 'OpenAttributeTableHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'OpenAttributeTableDefault' ),
                'action': self.actionsFactory.getAction('OpenAttributeTable'),
                'toolTip': 'Abrir tabela de atributos'
            },
            {
                'name': 'RestoreFields',
                'button': self.btn8,
                'iconHover': self.iconsFactory.getIcon( 'RestoreFieldsHover' ),
                'iconDefault': self.iconsFactory.getIcon( 'RestoreFieldsDefault' ),
                'action': self.actionsFactory.getAction('RestoreFields'),
                'toolTip': 'Cancelar criar mais como esse'
            }
        ]