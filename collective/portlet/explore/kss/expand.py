from Acquisition import aq_inner
from kss.core import kssaction
from plone.portlets.utils import unhashPortletInfo
from plone.app.kss.plonekssview import PloneKSSView 
from plone.app.portlets.utils import assignment_mapping_from_key 
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.portlets.portlets.navigation import NavtreeStrategy

class MyNavtreeStrategy(NavtreeStrategy):
    def __init__(self, context, view, root):
        super(MyNavtreeStrategy, self).__init__(context, view)
        self.root="/".join(root.getPhysicalPath())+"/"

    def nodeFilter(self, node):
        if not super(MyNavtreeStrategy, self).nodeFilter(node):
            return False
        return node["item"].getPath().startswith(self.root)



class ExpandMenu(PloneKSSView):
    recurse = ViewPageTemplateFile('../recurse.pt')

    @kssaction
    def expandNode(self, portlethash, uid):
        """Expand the navtree at a given UID for a given portlet.
        """

        rt=getToolByName(self.context, "reference_catalog")
        root=rt.lookupObject(uid)

        info=unhashPortletInfo(portlethash)
        mapping=assignment_mapping_from_key(self.context,
                info["manager"], info["category"], info["key"])
        assignment=mapping[info["name"]]

        queryBuilder = getMultiAdapter((root, assignment), INavigationQueryBuilder)
        strategy = MyNavtreeStrategy(aq_inner(self.context), assignment, root)

        query=queryBuilder()

        data=buildFolderTree(self.context, obj=root, query=query, strategy=strategy)
        html=self.recurse(children=data.get('children', []), level=1, bottomLevel=assignment.bottomLevel)

        core=self.getCommandSet("core")
        core.replaceHTML("div#portletwrapper-%s li.node-%s " % (portlethash, uid),
                        html)

