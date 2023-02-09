##############################################################################
#
# Copyright (c) 2013 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import zope.interface
import zope.publisher.base
import zope.publisher.interfaces.browser
import zope.publisher.skinnable


# http://docs.webob.org/en/latest/differences.html#id11

# XXX: implementing just the bare minimum that gets e.g. z3c.form working
#      feel free to add what's missing
@zope.interface.implementer(zope.publisher.interfaces.IResponse)
class PyramidPublisherResponse:

    def __init__(self, response):
        # avoid direct attribute access, because of __setattr__
        self.__dict__['_response'] = response

    def __getattr__(self, name):
        # mirror Response attributes
        return getattr(self._response, name)

    def __setattr__(self, name, value):
        # there are some attributes on Response that can be set,
        # e.g. ``charset``
        setattr(self._response, name, value)

    def getHeader(self, name):
        return self.headers.get(name)

    def setHeader(self, name, value):
        if name.lower() == 'content-type':
            # work around that webob stores the charset
            # in the header ``Content-type``, zope kills the charset
            # by setting e.g. ``text/html`` without charset
            charset = self._response.charset
            self.headers[name] = value
            # restore the old charset
            self._response.charset = charset
        else:
            self.headers[name] = value

    addHeader = setHeader

    def getStatus(self):
        return self._response.status_code

    def setStatus(self, status_code):
        self._response.status_code = status_code


# XXX: and again, just the bare minimum
@zope.interface.implementer(zope.publisher.interfaces.browser.IBrowserRequest)
class PyramidPublisherRequest(zope.publisher.base.BaseRequest):

    def __init__(self, request):
        # XXX: do I want to call BaseRequest.__init__???
        #      maybe not, we're more like hacking here
        self._request = request
        self._response = PyramidPublisherResponse(request.response)
        self.form = self._convertForm(request.params)
        self.debug = zope.publisher.base.DebugFlags()
        self.annotations = {}
        self._environ = request.environ

    def _convertForm(self, params):
        # BrowserRequest processes inputs HEAVILY
        # we'll process only :list because that's only what we use nowadays
        # and the code in BrowserRequest isn't really reusable
        rv = {}
        for k in params.keys():
            v = params.getall(k)
            if k.endswith(':list'):
                name = k[:-5]
            else:
                v = v[0]
                name = k
            rv[name] = v

        return rv

    def __getattr__(self, name):
        return getattr(self._request, name)

    def getURL(self):
        return self.path_url

    def keys(self):
        'See Interface.Common.Mapping.IEnumerableMapping'
        d = {}
        d.update(self.environment)
        # d.update(self._cookies)
        d.update(self.form)
        return d.keys()

    def get(self, key, default=None):
        'See Interface.Common.Mapping.IReadMapping'
        return self.form.get(key, self.environment.get(key, default))


class PyramidToPublisher:
    """View decorator that sets a skin on the request then wraps the request
    """

    def __init__(self, skin):
        self.skin = skin

    def __call__(self, original_class):
        orig_init = original_class.__init__
        skin = self.skin

        def __init__(self, context, request):
            request = PyramidPublisherRequest(request)
            zope.publisher.skinnable.applySkin(request, skin)
            orig_init(self, context, request)

        original_class.__init__ = __init__
        return original_class
