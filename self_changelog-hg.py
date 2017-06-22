import sys
from datetime import datetime

from changelogtools import (changelog, scm_exec)
from changelogtools.hg import (hg_log, hg_logs_between_versions)

from self_changelog import (GithubWithLinksMarkdown, entry_to_str, header)


def commit_datetime(version):
    date_time = hg_log([str(version), "-l", "-1",
                        '--template "{date|rfc822date}"']).split('\n')[0]

    if date_time is not '':
        dt = datetime.strptime(date_time, '%a %b %d %H:%M:%S %Y %z')
    else:
        dt = datetime.now()

    return dt.strftime('%a, %d %b %Y %H:%M:%S')


def md_changelog_entry(a, b, entries):
    entries = entries.splitlines()[1:]
    if a.is_invalid():
        return ""
    log = header(a, commit_datetime(a))
    log = log + "\n".join(map(entry_to_str, entries)) + "\n\n"

    return log


GithubWithLinksMarkdown.delta = hg_logs_between_versions
GithubWithLinksMarkdown.formatter = md_changelog_entry

BitBucketWithLinksMarkdown = GithubWithLinksMarkdown

if __name__ == "__main__":
    args = sys.argv[1:]
    tip = False

    if len(args) > 0:
        versions = [args[1]]
        tip = True
    else:
        tags = scm_exec('hg', ["tags"])
        if tags != '':
            lines = tags.split("\n")
            tags = map(lambda a: a.split(' ')[0], lines)
            tags = list(filter(lambda line: line != 'tip', tags))
            versions = list(filter(lambda line: line != '', tags))
        else:
            print("No changelog")
            sys.exit(0)

    print(changelog(versions=versions,
                    changelog=BitBucketWithLinksMarkdown,
                    tip=tip))
