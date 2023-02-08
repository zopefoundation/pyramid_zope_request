import unittest

from pyramid import testing


class Test_PyramidPublisherResponse(unittest.TestCase):
    def _callFUT(self, response):
        from pyramid_zope_request import PyramidPublisherResponse
        return PyramidPublisherResponse(response)

    def test_getattr(self):
        from pyramid.response import Response
        response = self._callFUT(Response(charset='ascii'))
        self.assertEqual(response.charset, 'ascii')
        self.assertEqual(response.headers['content-type'],
                         'text/html; charset=ascii')

    def test_setattr(self):
        from pyramid.response import Response
        response = self._callFUT(Response(charset='ascii'))
        self.assertEqual(response.charset, 'ascii')
        response.charset = 'UTF-8'
        self.assertEqual(response.charset, 'UTF-8')
        self.assertEqual(response.headers['content-type'],
                         'text/html; charset=UTF-8')

    def test_getheader(self):
        from pyramid.response import Response
        response = self._callFUT(Response(charset='ascii'))
        self.assertEqual(response.charset, 'ascii')
        self.assertEqual(response.getHeader('Content-Type'),
                         'text/html; charset=ascii')

    def test_setheader(self):
        from pyramid.response import Response
        response = self._callFUT(Response(charset='ascii'))
        self.assertEqual(response.charset, 'ascii')

        response.setHeader('X-Powered-By', 'Zope (www.zope.org)')
        self.assertEqual(response.getHeader('X-Powered-By'),
                         'Zope (www.zope.org)')

    def test_addheader(self):
        from pyramid.response import Response
        response = self._callFUT(Response(charset='ascii'))
        self.assertEqual(response.charset, 'ascii')

        response.addHeader('X-Powered-By', 'Zope (www.zope.org)')
        self.assertEqual(response.getHeader('X-Powered-By'),
                         'Zope (www.zope.org)')

    def test_setheader_content_type(self):
        from pyramid.response import Response
        response = self._callFUT(Response(charset='ascii'))
        self.assertEqual(response.charset, 'ascii')
        self.assertEqual(response.getHeader('Content-Type'),
                         'text/html; charset=ascii')
        response.setHeader('content-type', 'text/xml')
        # important is that charset stays the same
        self.assertEqual(response.charset, 'ascii')
        self.assertEqual(response.getHeader('Content-Type'),
                         'text/xml; charset=ascii')

    def test_getstatus(self):
        from pyramid.response import Response
        response = self._callFUT(Response())
        self.assertEqual(response.getStatus(), 200)
        response = self._callFUT(Response(status=404))
        self.assertEqual(response.getStatus(), 404)

    def test_setstatus(self):
        from pyramid.response import Response
        response = self._callFUT(Response())

        self.assertEqual(response.getStatus(), 200)
        response.setStatus(404)
        self.assertEqual(response.getStatus(), 404)


class Test_PyramidPublisherRequest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _callFUT(self, environ):
        from pyramid.request import Request
        request = Request(environ)
        request.registry = self.config.registry
        from pyramid_zope_request import PyramidPublisherRequest
        rv = PyramidPublisherRequest(request)
        return rv

    def test_init(self):
        environ = {
            'PATH_INFO': '/',
            'REFERER': 'localhost'
        }
        request = self._callFUT(environ)
        self.assertEqual(request.environment['REFERER'], 'localhost')
        self.assertEqual(request['REFERER'], 'localhost')
        self.assertEqual(request.annotations, {})
        self.assertEqual(request.debug.showTAL, False)
        self.assertEqual(request.debug.sourceAnnotations, False)
        self.assertEqual(request.response.__class__.__name__,
                         'PyramidPublisherResponse')

    def test_convert_form(self):
        environ = {
            'PATH_INFO': '/',
            'QUERY_STRING':
                'lastName=Doe;country:list=Japan;country:list=Hungary',
        }
        request = self._callFUT(environ)
        self.assertEqual(request.form,
                         {'country': ['Japan', 'Hungary'], 'lastName': 'Doe'})

    def test_getattr(self):
        environ = {
            'PATH_INFO': '/',
            'HTTP_REFERER': 'localhost',
        }
        request = self._callFUT(environ)
        self.assertEqual(request.referer, 'localhost')

    def test_geturl(self):
        environ = {
            'PATH_INFO': '/',
            'SERVER_NAME': 'example.com',
            'SERVER_PORT': '5432',
            'wsgi.url_scheme': 'http',
        }
        request = self._callFUT(environ)
        self.assertEqual(request.getURL(), 'http://example.com:5432/')

    def test_keys(self):
        environ = {
            'PATH_INFO': '/',
            'SERVER_NAME': 'example.com',
            'SERVER_PORT': '5432',
            'wsgi.url_scheme': 'http',
        }
        request = self._callFUT(environ)
        self.assertEqual(sorted(request.keys()),
                         ['PATH_INFO', 'SERVER_NAME', 'SERVER_PORT',
                          'webob._parsed_query_vars', 'wsgi.url_scheme'])

    def test_get(self):
        environ = {
            'PATH_INFO': '/',
            'SERVER_NAME': 'example.com',
            'SERVER_PORT': '5432',
            'QUERY_STRING':
                'lastName=Doe;country:list=Japan;country:list=Hungary',
            'wsgi.url_scheme': 'http',
        }
        request = self._callFUT(environ)
        self.assertEqual(request.get('SERVER_NAME'), 'example.com')
        self.assertEqual(request.get('foobar'), None)
        self.assertEqual(request.get('lastName'), 'Doe')


class Test_PyramidToPublisher(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _getRequest(self, environ):
        from pyramid.request import Request
        request = Request(environ)
        request.registry = self.config.registry
        return request

    def test_wrap(self):
        environ = {
            'PATH_INFO': '/',
            'SERVER_NAME': 'example.com',
            'SERVER_PORT': '5432',
            'QUERY_STRING':
                'lastName=Doe;country:list=Japan;country:list=Hungary',
            'wsgi.url_scheme': 'http',
        }
        req = self._getRequest(environ)

        from zope.publisher.interfaces.browser import IBrowserRequest

        class ITestLayer(IBrowserRequest):
            pass

        from pyramid_zope_request import PyramidToPublisher
        wrapper = PyramidToPublisher(ITestLayer)

        class View:
            def __init__(self, context, request):
                self.context = context
                self.request = request

        wrapped = wrapper(View)
        view = wrapped('blabla', req)

        self.assertEqual(view.request.__class__.__name__,
                         'PyramidPublisherRequest')

        # check applied skin
        import zope.interface
        from zope.publisher.interfaces import ISkinType
        ifaces = [
            iface
            for iface in zope.interface.directlyProvidedBy(view.request)
            if not ISkinType.providedBy(iface)]
        self.assertEqual(len(ifaces), 1)
        self.assertEqual(ifaces[0].__name__, 'ITestLayer')


class Test_z3cform(unittest.TestCase):
    # this is the real deal
    # render a z3c.form with a pyramid request
    def setUp(self):
        self.config = testing.setUp()
        from z3c.form import testing as z3cform_testing
        z3cform_testing.setUp(self)
        z3cform_testing.setupFormDefaults()

    def tearDown(self):
        from z3c.form import testing as z3cform_testing
        z3cform_testing.tearDown(self)
        testing.tearDown()

    def _getRequest(self, environ):
        from pyramid.request import Request
        request = Request(environ)
        request.registry = self.config.registry
        return request

    def _getView(self):
        import z3c.form.interfaces
        from zope.publisher.interfaces.browser import IBrowserRequest

        class IMyLayer(z3c.form.interfaces.IFormLayer, IBrowserRequest):
            pass

        import zope.schema

        class IPerson(zope.interface.Interface):
            name = zope.schema.TextLine(
                title='Name',
                required=True)

        @zope.interface.implementer(IPerson)
        class Person:
            name = ''

        import z3c.form.field
        import z3c.form.form

        from pyramid_zope_request import PyramidToPublisher

        @PyramidToPublisher(IMyLayer)
        class edit_person(z3c.form.form.Form):
            fields = z3c.form.field.Fields(IPerson)

        environ = {
            'PATH_INFO': '/',
            'SERVER_NAME': 'example.com',
            'SERVER_PORT': '5432',
            'wsgi.url_scheme': 'http',
        }
        request = self._getRequest(environ)

        context = Person()
        context.name = 'John Doe'

        view = edit_person(context, request)

        return view

    def test_z3cform_call(self):
        view = self._getView()
        # render with __call__, there must be a ZPT template in place

        import os

        from z3c.form import tests
        from zope.browserpage.viewpagetemplatefile import BoundPageTemplate
        from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

        view.template = BoundPageTemplate(
            ViewPageTemplateFile('simple_edit.pt',
                                 os.path.dirname(tests.__file__)), view)

        result = view()
        self.assertTrue("<!DOCTYPE html" in result)
        self.assertTrue('id="form-widgets-name"' in result)
        self.assertTrue('name="form.widgets.name"' in result)
        self.assertTrue('value="John Doe"' in result)

    def test_z3cform_update(self):
        view = self._getView()
        view.update()
        # do not render by calling __call__, but render with a
        # pyramid/chameleon template by using the view's attributes
        self.assertEqual(view.action, "http://example.com:5432/")
        self.assertEqual(view.status, "")

        self.assertEqual(view.widgets['name'].name, 'form.widgets.name')
        self.assertEqual(view.widgets['name'].label, 'Name')
        self.assertEqual(view.widgets['name'].required, True)
        self.assertEqual(view.widgets['name'].value, 'John Doe')
