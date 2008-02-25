from new import instancemethod
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

        queryBuilder = getMultiAdapter((root, assignment),
                                       INavigationQueryBuilder)
        # Dragons be here
        strategy = getMultiAdapter((aq_inner(self.context), assignment), INavtreeStrategy)
        strategy.root = "/".join(root.getPhysicalPath())
        strategy.showAllParents = True
        strategy.rootPath = "/".join(root.getParentNode().getPhysicalPath())
        def nodeFilter(self, node):
            if not self._old_nodeFilter(node):
                return False
            return node["item"].getPath().startswith(self.root+"/") or \
                     node["item"].getPath()==self.root

        strategy._old_nodeFilter = strategy.nodeFilter
        strategy.nodeFilter = instancemethod(nodeFilter, strategy, strategy.__class__)

        query=queryBuilder()

        data=buildFolderTree(root, query=query, strategy=strategy)
        html=self.recurse(children=data.get('children', []), level=1, bottomLevel=assignment.bottomLevel)

        core=self.getCommandSet("core")
        selector="div#portletwrapper-%s li.node-%s " % (portlethash, uid)

        core.replaceHTML(selector, html)

        selector="div#portletwrapper-%s span.kssattr-uid-%s" % (portlethash,uid)
        core.removeClass(selector, "toggleNode")
        core.addClass(selector, "expandedNode")
        core.addClass(selector, "showChildren")

