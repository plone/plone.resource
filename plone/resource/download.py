# -*- coding: utf-8 -*-
from StringIO import StringIO
from zope.publisher.browser import BrowserView


class DownloadView(BrowserView):

    def __call__(self):
        name = self.context.__name__

        response = self.request.response

        # XXX: It would be better to have the zip file written straight to
        # the output stream, but this is awkward with the ZPublisher response
        # interface. For now, we write the zipfile to a stream in memory.

        out = StringIO()
        self.context.exportZip(out)

        response.setHeader('Content-Type', 'application/zip')
        response.setHeader(
            'Content-Disposition',
            'attachment; filename="%s.zip"' % name
        )
        response.setHeader('Content-Length', len(out.getvalue()))

        response.write(out.getvalue())
