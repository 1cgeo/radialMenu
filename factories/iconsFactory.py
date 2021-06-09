import os
from PyQt5.QtGui import QIcon

class IconsFactory:

    def getIcon(self, iconName):
        icons = {
            'LastLayerDeafult': 'lastlayer_default',
            'LastLayerHover': 'lastlayer_hover',
            'SelectRasterDefault': 'selectraster_default',
            'SelectRasterHover': 'selectraster_hover',
            'AddPointFeatureDefault': 'addpoint_default',
            'AddPointFeatureHover': 'addpoint_hover',
            'SelectFeatureDefault': 'selectfeature_default',
            'SelectFeatureHover': 'selectfeature_hover',
            'SetFeatureInspectorDefault': 'inspect_default',
            'SetFeatureInspectorHover': 'inspect_hover',
            'TopologicalSnappingDefault': 'topologicalsnapping_default',
            'TopologicalSnappingHover': 'topologicalsnapping_hover',
            'OpenAttributeTableDefault': 'attributetable_default',
            'OpenAttributeTableHover': 'attributetable_hover',
            'SetDefaultFieldsDefault': 'setdefaultfields_default',
            'SetDefaultFieldsHover': 'setdefaultfields_hover',
            'RestoreFieldsDefault': 'restorefields_default',
            'RestoreFieldsHover': 'restorefields_hover',
            'MoveFeatureDefault': 'movefeature_default',
            'MoveFeatureHover': 'movefeature_hover',
            'MergeFeatureAttributesHover': 'mergefeatureattributes_hover',
            'MergeFeatureAttributesDefault': 'mergefeatureattributes_default',
            'DeleteSelectedHover': 'deleteselected_hover',
            'DeleteSelectedDefault': 'deleteselected_default',
            'FreeHandHover': 'freehand_hover',
            'FreeHandDefault': 'freehand_default',
            'CutFeaturesHover': 'cutfeatures_hover',
            'CutFeaturesDefault': 'cutfeatures_default',
            'TrimExtendFeatureHover': 'trimextendfeature_hover',
            'TrimExtendFeatureDefault': 'trimextendfeature_default',
            'AddRingHover': 'addring_hover',
            'AddRingDefault': 'addring_default',
            'DeleteRingHover': 'deletering_hover',
            'DeleteRingDefault': 'deletering_default',
            'RightDegreeAngleDigitizingHover': 'rightdegreeangle_hover',
            'RightDegreeAngleDigitizingDefault': 'rightdegreeangle_default',
            'FreeHandReshapeHover': 'freehandreshape_hover',
            'FreeHandReshapeDefault': 'freehandreshape_default',

        }
        if iconName in icons:
            return QIcon( self.getIconPath( icons[iconName] ) )
        return None

    def getIconPath(self, iconName):
        return os.path.join(
            os.path.abspath(os.path.join(
                os.path.dirname(__file__)
            )),
            '..',
            'icons',
            '{}.svg'.format(iconName)
        )