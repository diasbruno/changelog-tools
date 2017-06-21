from subprocess import Popen, PIPE


def git_exec(args):
    p = Popen(" ".join(["git"] + args), shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    return out.decode('utf-8')


def git_log(args):
    return git_exec(["log"] + args)


def git_logs_between_versions(a, b):
    ls = []

    if b:
        ls.append(str(b))

    ls.append("HEAD" if a.tip else str(a))

    return (a, b,
            git_log(["--format='%h %s'", "..".join(ls)]))
