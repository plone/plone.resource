# -*- coding: utf-8 -*-
from zope.interface import Attribute
from zope.interface import Interface
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.publisher.interfaces import IPublishTraverse


class IResourceDirectory(IPublishTraverse):
    """A directory of file-like resources.

    This interface provides a common API for interacting with resources
    regardless of whether they are stored on the filesystem or in the
    ZODB.
    """

    __name__ = Attribute("""The name of the directory.""")

    def __repr__():
        """Returns a string identifier of the directory."""

    def __contains__(name):
        """Return true if the given file or directory exists
        """

    def __getitem__(name):
        """Return the file or resource directory with the given name
        as an object
        """

    def openFile(path):
        """Returns the file or filelike object identified by the given path
        (relative to this directory).

        Raises IOError if the file cannot be opened.
        """

    def readFile(path):
        """Returns the contents of the file identified by the given path.

        Raises IOError if the file cannot be read.
        """

    def listDirectory():
        """Lists the contents of this directory.

        Raises OSError if the directory cannot be read.
        """

    def isDirectory(path):
        """Returns True if the given path (relative to this directory) is a
        directory (as opposed to a file).
        """

    def isFile(path):
        """Returns True if the given path is a file."""

    def exportZip(out):
        """Exports the contents of this directory as a zip file, which will
        be written to the open file handle ``out``.
        """


class IWritableResourceDirectory(IResourceDirectory):

    def makeDirectory(path):
        """Create the given path as a directory. (Returns successfully without
        doing anything if the directory already exists.)
        """

    def writeFile(path, data):
        """Write a file at the specified path.

        Parent directories will be added if necessary. The final path component
        gives the filename. If the file already exists, it will be overwritten.

        ``data`` may be a string or file-like object.
        """

    def importZip(file):
        """Imports the contents of a zip file into this directory.

        ``file`` may be a filename, file-like object, or instance of
        zipfile.ZipFile. The file data must be a ZIP archive.
        """

    def __delitem__(name):
        """Delete a file or directory inside this directory
        """

    def __setitem__(name, item):
        """Add a file or directory as returned by ``__getitem__()``
        """

    def rename(oldName, newName):
        """Rename a child file or folder
        """


class IUniqueResourceRequest(Interface):
    """Marker interface for requests to ++unique++<id>"""


class IPloneResourceCreatedEvent(IObjectCreatedEvent):
    """An resource has been created."""


class IPloneResourceModifiedEvent(IObjectModifiedEvent):
    """An resource has been created."""
