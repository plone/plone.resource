# -*- coding: utf-8 -*-
"""Utilities for working with manifest files.

The manifest is stored in a file ``manifest.cfg`` in the root of a resource
directory. It uses ini file (ConfigParser) syntax.

For example, for the resource type foo, there could be a manifest file like::

    [foo]
    title = A foo resource
    description = Used for doing foo-like things
    bar = Moe's

We can define this manifest format using::

    from plone.resource.manifest import ManifestFormat
    FOO_FORMAT = ManifestFormat('foo',
            keys=['title', 'description', 'bar'],
            defaults={'bar': 'baz'},
        )

To get this manifest from an open file pointer ``fp``, do::

    from plone.resource.manifest import getManifest
    manifest = getManifest(fp, FOO_FORMAT)

``manifest`` will now be a dict with keys ``title``, ``description``, and
``bar``. ``title`` and ``description`` will be ``None`` if not found in the
manifest. ``bar`` will be ``baz`` if not found.
"""
from ConfigParser import SafeConfigParser
from plone.resource.directory import FILTERS
from plone.resource.interfaces import IResourceDirectory
from plone.resource.utils import iterDirectoriesOfType
from zope.component import getUtility
import logging

MANIFEST_FILENAME = 'manifest.cfg'

LOGGER = logging.getLogger('plone.resource.manifest')


class ManifestFormat(object):
    """Describes a manifest format.

    An immutable, threadsafe object.

    ``resourceType`` is used as the section header.

    ``keys`` should be a list of keys that should be returned.

    ``defaults`` can be used to pass a dict of default values. The keys
    should correspond to ``keys``, but it is not mandatory to fill every key.

    ``parameterSections`` can be a list section names in the ``manifest.cfg``
    file that can be used to supply additional, free-form parameters. For
    example, if ``parameters`` is ['parameters'] and 'resourceType' is
    'theme', then the ``manifest.cfg`` file may optionally contain a section
    ``[theme:parameters]``.
    """

    def __init__(self, resourceType, keys, defaults=None,
                 parameterSections=None):
        self.resourceType = resourceType
        self.keys = keys
        self.defaults = defaults or {}
        self.parameterSections = parameterSections or []


def getManifest(fp, format, defaults=None):
    """Read the manifest from the given open file pointer according to the
    given ManifestFormat. Pass a dict as ``defaults`` to override the defaults
    from the manifest format.
    """

    if defaults is None:
        defaults = format.defaults

    parser = SafeConfigParser()
    parser.readfp(fp)

    results = {}
    for key in format.keys:
        if parser.has_option(format.resourceType, key):
            results[key] = parser.get(format.resourceType, key)
        else:
            results[key] = defaults.get(key, None)

    for key in format.parameterSections:
        sectionName = "%s:%s" % (format.resourceType, key,)
        if parser.has_section(sectionName):
            results[key] = dict(parser.items(sectionName))
        else:
            results[key] = {}

    return results


def extractManifestFromZipFile(zipfile, format, defaults=None,
                               manifestFilename=MANIFEST_FILENAME):
    """Get a resource name and manifest from the given open
    ``zipfile.ZipFile`` using the given format. Returns a tuple::

        (resourceName, manifestDict)

    Where ``resourceName`` is the resource name, taken to be the name of the
    single top level directory inside the zip file (ignoring certain OS
    files), and ``manifestDict`` is a dictionary as returned by
    ``getManifest()``.

    The ``manifestDict`` may be None if no manifest file was found.

    Will throw a ValueError if the zip file does not contain a single top
    level directory.

    Pass ``defaults`` to override the defaults from the manifest format.

    Pass ``manifestFilename`` to use a custom manifest filename.
    """

    resourceName = None
    manifestDict = None

    for name in zipfile.namelist():
        member = zipfile.getinfo(name)
        path = member.filename.lstrip('/')

        # Skip filtered files (OS X junk and dot files, mainly)
        if any(
            any(
                filter.match(n) for filter in FILTERS
            ) for n in path.split('/')
        ):
            continue

        pathSegments = path.rstrip('/').split('/')
        isDirectory = path.endswith('/')

        # Is this a new top level directory?
        if pathSegments[0] != resourceName:

            # We already thought we had one - abort
            if resourceName is not None:
                raise ValueError("More than one top level directory")

            # Store the first path segment (which may either be the directory)
            # itself, or the directory part in which some file is found
            if isDirectory or len(pathSegments) > 0:
                resourceName = pathSegments[0]
            else:
                raise ValueError(
                    "Found a top level file - expected a single top level "
                    "directory"
                )

        # Did we find a manifest file?
        if (
            resourceName is not None and
            not isDirectory and
            path == "%s/%s" % (resourceName, manifestFilename,)
        ):
            manifest = zipfile.open(member)
            try:
                manifestDict = getManifest(manifest, format, defaults=defaults)
            finally:
                manifest.close()

    if resourceName is None:
        raise ValueError("No top level directory found")

    return (resourceName, manifestDict)


def getAllResources(format, defaults=None, filter=None,
                    manifestFilename=MANIFEST_FILENAME):
    """Get a dict of all resources of the resource type indicated by the
    manifest format. Returns a dict where the keys are the resource ids and
    the values are manifests. The value may be None if no manifest was found.

    Pass ``defaults`` to override the defaults from the manifest format.

    Pass ``filter``, a callable that takes a resource directory as its
    only argument, if you want to be able to filter out any resource
    directories. It should return True if the given directory should be
    included.

    Pass ``manifestFilename`` to use a different manifest file name
    convention.
    """

    resources = {}

    for directory in iterDirectoriesOfType(format.resourceType):

        if filter is not None and not filter(directory):
            continue

        name = directory.__name__
        resources[name] = None

        if directory.isFile(manifestFilename):

            manifest = directory.openFile(manifestFilename)
            try:
                resources[name] = getManifest(manifest, format, defaults)
            except:
                LOGGER.exception(
                    "Unable to read manifest for theme directory {0}".format(
                        name
                    )
                )
            finally:
                manifest.close()

    return resources


def getZODBResources(format, defaults=None, filter=None,
                     manifestFilename=MANIFEST_FILENAME):
    """Get a dict of all resources in the ZODB of the resource type indicated
    by the manifest format. Returns a dict where the keys are the resource
    ids and the values are manifests. The value may be None if no manifest was
    found.

    Pass ``defaults`` to override the defaults from the manifest format.

    Pass ``filter``, a callable that takes a resource directory as its
    only argument, if you want to be able to filter out any resource
    directories. It should return True if the given directory should be
    included.

    Pass ``manifestFilename`` to use a different manifest file name
    convention.
    """

    resources = {}

    persistentDirectory = getUtility(IResourceDirectory, name="persistent")
    if format.resourceType not in persistentDirectory:
        return resources

    resourcesDirectory = persistentDirectory[format.resourceType]

    for name in resourcesDirectory.listDirectory():

        resourceDir = resourcesDirectory[name]

        if filter is not None and not filter(resourceDir):
            continue

        resources[name] = None

        if resourceDir.isFile(manifestFilename):
            manifest = resourceDir.openFile(MANIFEST_FILENAME)
            try:
                resources[name] = getManifest(manifest, format, defaults)
            except:
                LOGGER.exception(
                    "Unable to read manifest for {0} directory {1}".format(
                        manifest.resourceType, name
                    )
                )
            finally:
                manifest.close()

    return resources
