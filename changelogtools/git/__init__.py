from .. import scm_exec


def git_log(args):
    return scm_exec('git', ["log"] + args)


def git_logs_between_versions(a, b):
    ls = []

    if b:
        ls.append(str(b))

    ls.append("HEAD" if a.tip else str(a))

    return (a, b,
            git_log(["--format='%h %s'", "..".join(ls)]))
