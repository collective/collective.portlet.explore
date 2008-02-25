from kss.core import kssaction
from plone.app.kss.plonekssview import PloneKSSView 

class ExpandMenu(PloneKSSView):
    @kssaction
    def expandNode(self, uid):
        """Expand the navtree at a given UID for a given portlet.
        """
        print uid

