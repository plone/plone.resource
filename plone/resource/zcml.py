import os.path
from zope.interface import Interface
from zope.component.zcml import handler
from zope.configuration.exceptions import ConfigurationError
from zope.configuration.fields import PythonIdentifier
from zope.schema import ASCIILine, TextLine

from plone.resource.interfaces import IResourceDirectory
from plone.resource.directory import FilesystemResourceDirectory


class IResourceDirectoryDirective(Interface):
    """Register resource directories with the global registry.
    """

    directory = TextLine(
        title = u'Directory path',
        description = u'Path relative to the package.',
        required = True
        )

    name = PythonIdentifier(
        title = u'Name',
        description = u'Name of the directory. If not specified, the name of the '
                      u' current package is used.',
        required = False,
        )

    type = ASCIILine(
        title = u'Resource type',
# XXX use a Choice field + vocab
#        vocabulary = 'plone.resource.vocab.ResourceTypes',
        required = False,
        )


def registerResourceDirectory(_context, directory, name=None, type=None):
    """
    Register a new resource directory.
    
    The actual ZCA registrations are deferred so that conflicts can be resolved
    via zope.configuration's discriminator machinery.
    """
    
    if _context.package and directory.startswith('/'):
        raise ConfigurationError('Resource directories in distributions must '
                                 'be specified as relative paths.')
    elif _context.package:
        directory = _context.path(directory)
    
    if not os.path.exists(directory):
        raise IOError, 'Directory not found: %s' % directory
    
    if not type and not name:
        identifier = ''
    elif not type:
        identifier = name
    else:
        identifier = '++%s++%s' % (type, name)
    
    directory = FilesystemResourceDirectory(type, name, directory)
    
    _context.action(
        discriminator = ('plone:resourceDirectory', identifier),
        callable = handler,
        args = ('registerUtility', directory, IResourceDirectory, identifier),
        )
