from subprocess import Popen, PIPE

__version__ = '0.1.0'


class MissingChangelogClassError(BaseException):
    pass


class NotEnoughVersionsError(BaseException):
    pass


class VersionRequiresCmpMethod(BaseException):
    pass


class VersionRequiresIsInvalidMethod(BaseException):
    pass


class Version(object):
    def cmp(self, b):
        raise VersionRequiresCmpMethod()

    def is_invalid(self):
        raise VersionRequiresIsInvalidMethod()


class SemVer(Version):
    """
    Parses a version name, provides comparison, validate the name
    a str protocol.
    """
    def __init__(self, version):
        v = version
        self.v = v.startswith('v')
        if self.v:
            v = v[1:].split('\n')[0]
        fix = v.split('.')
        self.major = int(fix[0])
        self.minor = int(fix[1])
        self.patch = int(fix[2])
        self.tip = False

    def cmp(self, b):
        """ Provides comparison between two versions. """
        if self.major > b.major:
            return True
        if self.minor > b.minor:
            return True
        if self.patch > b.patch:
            return True
        return False

    def is_invalid(self):
        """ Check if the name is invalid. """
        return self.major == 0 and self.minor == 0 and self.patch == 0

    def __str__(self):
        """ Provides a string protocol. """
        return self.__repr__()

    def __repr__(self):
        """ Provides a representation protocol. """
        starts_with_v = ""
        if self.v:
            starts_with_v = "v"
        version = ".".join(map(str, [self.major, self.minor, self.patch]))
        return starts_with_v + version


class CompareVersions(object):
    """ Object to be used by sorted(). """
    def __init__(self, obj, *args):
        self.obj = obj

    def __lt__(self, other):
        return not self.obj.cmp(other.obj)

    def __gt__(self, other):
        return self.obj.cmp(other.obj)


class Changelog(object):
    """
    Make version names, get the log between two versions
    and format the changelog entry.
    """
    def __init__(self, version=None, delta=None, formatter=None):
        self._delta = delta
        self._formatter = formatter
        self._version = version

    @property
    def version(self):
        return self._version

    @property
    def delta(self):
        return self._delta

    def formatter(self, info):
        a, b, entries = info
        return self._formatter(a, b, entries)


def scm_exec(prog, args):  # pragma: no coverage
    p = Popen(" ".join([prog] + args), shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    return out.decode('utf-8')


def adjacents(ls, f, res):
    """" Apply a function to the head and the next. """
    if len(ls) == 0:
        return res

    first = ls[0]
    if len(ls) == 1:
        next = None
    else:
        next = ls[1]

    res.append(f(first, next))
    return adjacents(ls[1:], f, res)


def check_versions(versions=[]):
    """ Check if there are version to build the changelog. """
    if len(versions) == 0:
        raise NotEnoughVersionsError()
    return True


def changelog(versions=[], changelog=None, tip=False):
    """ Generate the changelog with this configurations. """
    if changelog is None:
        raise MissingChangelogClassError()

    assert check_versions(versions)

    versions = map(changelog.version, versions)
    versions = list(filter(lambda a: not a.is_invalid(), versions))

    assert check_versions(versions)

    if tip:
        versions[0].tip = True

    versions = sorted(versions, key=CompareVersions, reverse=True)
    versions = adjacents(versions, changelog.delta, [])
    changelogs = map(changelog.formatter, versions)

    return "\n".join(changelogs)
