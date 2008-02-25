from zope.component import getUtility, getMultiAdapter

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer

from plone.app.portlets.storage import PortletAssignmentMapping

from collective.portlet.explore import explorerportlet

from collective.portlet.explore.tests.base import TestCase

class TestPortlet(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager',))

    def test_portlet_type_registered(self):
        portlet = getUtility(IPortletType, name='collective.portlet.explore.ExplorerPortlet')
        self.assertEquals(portlet.addview, 'collective.portlet.explore.ExplorerPortlet')

    def test_interfaces(self):
        # TODO: Pass any keyword arguments to the Assignment constructor
        portlet = explorerportlet.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_add_view(self):
        portlet = getUtility(IPortletType, name='collective.portlet.explore.ExplorerPortlet')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        # TODO: Pass a dictionary containing dummy form inputs from the add form
        addview.createAndAdd(data={})

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0], explorerportlet.Assignment))

    # NOTE: This test can be removed if the portlet has no edit form
    def test_invoke_edit_view(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST

        mapping['foo'] = explorerportlet.Assignment()
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, explorerportlet.EditForm))

    def test_obtain_renderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)

        # TODO: Pass any keyword arguments to the Assignment constructor
        assignment = explorerportlet.Assignment()

        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, explorerportlet.Renderer))

class TestRenderer(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager',))

    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)

        # TODO: Pass any default keyword arguments to the Assignment constructor
        assignment = assignment or explorerportlet.Assignment()
        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)

    def test_render(self):
        # TODO: Pass any keyword arguments to the Assignment constructor
        r = self.renderer(context=self.portal, assignment=explorerportlet.Assignment())
        r = r.__of__(self.folder)
        r.update()
        output = r.render()
        # TODO: Test output

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    suite.addTest(makeSuite(TestRenderer))
    return suite
