import pytest
from . import (Version, SemVer, Changelog, NotEnoughVersionsError,
               MissingChangelogClassError, VersionRequiresCmpMethod,
               VersionRequiresIsInvalidMethod,
               CompareVersions, adjacents, changelog)


class BrokenVersion(Version):
    pass


def test_version_require_cmp_method():
    with pytest.raises(VersionRequiresCmpMethod) as excinfo:
        BrokenVersion().cmp(1)
    assert excinfo


def test_version_require_is_invalid_method():
    with pytest.raises(VersionRequiresIsInvalidMethod) as excinfo:
        BrokenVersion().is_invalid()
    assert excinfo


def test_is_version_invalid():
    assert SemVer("v0.0.0").is_invalid()


def test_is_version_is_not_invalid():
    assert not SemVer("v0.0.1").is_invalid()


def test_compare_versions_major_gt():
    a = SemVer("v1.0.1")
    b = SemVer("v0.0.1")
    assert CompareVersions(a) > CompareVersions(b)


def test_compare_versions_minor_gt():
    a = SemVer("v0.1.1")
    b = SemVer("v0.0.1")
    assert CompareVersions(a) > CompareVersions(b)


def test_compare_versions_gt():
    a = SemVer("v0.0.10")
    b = SemVer("v0.0.1")
    assert CompareVersions(a) > CompareVersions(b)


def test_compare_versions_lt():
    a = SemVer("v0.0.10")
    b = SemVer("v0.0.1")
    assert CompareVersions(b) < CompareVersions(a)


def test_parse_semver():
    assert str(SemVer("v1.0.0")) == "v1.0.0"


def test_parse_semver_without_v():
    assert str(SemVer("1.0.0")) == "1.0.0"


def sum(a, b):
    if b is None:
        return a
    else:
        return a + b


def test_change_log():
    a = SemVer("v0.0.10")
    b = SemVer("v0.0.1")
    assert Changelog((a, b, ''))


def test_adjacent_empty():
    assert adjacents([], sum, []) == []


def test_adjacent_one():
    assert adjacents([1], sum, []) == [1]


def test_adjacent_ok():
    assert adjacents([1, 2], sum, []) == [3, 2]


def test_changelog_without_changelog():
    with pytest.raises(MissingChangelogClassError) as excinfo:
        changelog()
    assert excinfo


def test_changelog_no_versions():
    with pytest.raises(NotEnoughVersionsError) as excinfo:
        changelog(versions=[], changelog=Changelog())
    assert excinfo


def delta(a, b):
    return (a, b, '\n'.join(['a', 'b']))


def dummy_formatter(a, b, entries):
    return '%s\n%s\n' % (str(a), entries)


def test_change_log_with_one_version():
    cc = Changelog(version=SemVer,
                   delta=delta,
                   formatter=dummy_formatter)

    c = changelog(versions=["v0.0.1"], changelog=cc)
    assert c == "v0.0.1\na\nb\n"


def test_change_log_with_tip():
    def tip_formatter(a, b, entries):
        return '{} {}\n{}\n'.format(str(a), str(a.tip), entries)

    cc = Changelog(version=SemVer,
                   delta=delta,
                   formatter=tip_formatter)

    c = changelog(versions=["v0.0.1"],
                  changelog=cc,
                  tip=True)

    assert c == "v0.0.1 True\na\nb\n"


def test_change_log_custom_changelog():
    cc = Changelog(version=SemVer,
                   delta=delta,
                   formatter=dummy_formatter)
    c = changelog(versions=["v0.0.1", "v0.0.2"], changelog=cc)
    r = "v0.0.2\na\nb\n\nv0.0.1\na\nb\n"
    assert c == r
