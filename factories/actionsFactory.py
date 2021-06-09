from qgis import gui, core
from qgis.utils import iface
from radialMenu.actions.lastLayer import LastLayer
from radialMenu.actions.selectRaster import SelectRaster
from radialMenu.actions.addPointFeature import AddPointFeature
from radialMenu.actions.selectFeature import SelectFeature
from radialMenu.actions.setFeatureInspector import SetFeatureInspector
from radialMenu.actions.topologicalSnapping import TopologicalSnapping
from radialMenu.actions.openAttributeTable import OpenAttributeTable
from radialMenu.actions.restoreFields import RestoreFields
from radialMenu.actions.setDefaultFields import SetDefaultFields
from radialMenu.actions.openAttributeTableOnlySelection import OpenAttributeTableOnlySelection
from radialMenu.actions.moveFeature import MoveFeature
from radialMenu.actions.mergeFeatureAttributes import MergeFeatureAttributes
from radialMenu.actions.deleteSelected import DeleteSelected
from radialMenu.actions.freeHand import FreeHand
from radialMenu.actions.cutFeatures import CutFeatures
from radialMenu.actions.trimExtendFeature import TrimExtendFeature
from radialMenu.actions.addRing import AddRing
from radialMenu.actions.deleteRing import DeleteRing
from radialMenu.actions.rightDegreeAngleDigitizing import RightDegreeAngleDigitizing
from radialMenu.actions.freeHandReshape import FreeHandReshape

class ActionsFactory:

    def __init__(self):
        self.lastLayer = LastLayer()

    def getAction(self, actionName):
        actions = {
            'LastLayer' : lambda: self.lastLayer,
            'SelectRaster': SelectRaster,
            'AddPointFeature': AddPointFeature,
            'SelectFeature': SelectFeature,
            'SetFeatureInspector': SetFeatureInspector,
            'TopologicalSnapping': TopologicalSnapping,
            'OpenAttributeTable': OpenAttributeTable,
            'RestoreFields': RestoreFields,
            'SetDefaultFields': SetDefaultFields,
            'OpenAttributeTableOnlySelection': OpenAttributeTableOnlySelection,
            'MoveFeature': MoveFeature,
            'MergeFeatureAttributes': MergeFeatureAttributes,
            'DeleteSelected': DeleteSelected,
            'FreeHand': FreeHand,
            'CutFeatures': CutFeatures,
            'TrimExtendFeature': TrimExtendFeature,
            'AddRing': AddRing,
            'DeleteRing': DeleteRing,
            'RightDegreeAngleDigitizing': RightDegreeAngleDigitizing,
            'FreeHandReshape': FreeHandReshape
        }
        return actions[actionName]() if actionName in actions else None

    
