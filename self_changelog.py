import sys
from datetime import datetime

from changelogtools import (Changelog, SemVer, changelog, default_cli, scm_exec)
from changelogtools.git import (git_log, git_logs_between_versions)


def github_url(h):
    return '../../commit/%s' % h


def entry_to_str(entry):
    log = entry.split(' ')
    hash = log[0]
    return "- [%s](%s) %s" % (hash, github_url(hash), ' '.join(log[1:]))


def commit_datetime(version):
    date_time = git_log([str(version), "-1", '--format="%ad"']).split('\n')[0]

    if date_time is not '':
        dt = datetime.strptime(date_time, '%a %b %d %H:%M:%S %Y %z')
    else:
        dt = datetime.now()

    return dt.strftime('%a, %d %b %Y %H:%M:%S')


def header(a, dt):
    log = str(a) + " - " + dt + " UTC\n"
    return log + ("-" * (len(log) - 1)) + "\n\n"


def md_changelog_entry(a, b, entries):
    entries = entries.splitlines()[1:]
    if a.is_invalid():
        return ""
    log = header(a, commit_datetime(a))
    log = log + "\n".join(map(entry_to_str, entries)) + "\n\n"

    return log


# This changelog style will generate a link to all commits on changelog.
# You can change delta and formatter by setting:
#
# GithubWithLinksMarkdown.delta = hg_delta_function
# GithubWithLinksMarkdown.formatter = hg_formatter_function
GithubWithLinksMarkdown = Changelog(version=SemVer,
                                    delta=git_logs_between_versions,
                                    formatter=md_changelog_entry)

def git_tags():
    return scm_exec('git', ["tag", "-l"])

if __name__ == "__main__":
    tip = False

    args = default_cli.parse_args()

    if args.tip or args.between:
        versions = args.versions
    else:
        tags = git_tags()
        versions = list(filter(lambda line: line != '', tags.split("\n")))

        if len(tags) == 0:
            print("No changelog")
            sys.exit(0)

    print(changelog(versions=versions,
                    changelog=GithubWithLinksMarkdown,
                    tip=args.tip,
                    between=args.between))
