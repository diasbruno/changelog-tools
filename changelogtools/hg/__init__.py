from .. import scm_exec


def hg_log(args):
    return scm_exec('hg', ["log"] + args)


def hg_logs_between_versions(a, b):
    v = "tip" if a.tip else str(a)

    if b:
        v = '"{}::{} - {}"'.format(str(b), v, str(b))

    return (a, b,
            hg_log(['-r', v, "-M",
                    '--template',
                    '\"{node|short} {splitlines(desc) % \'{line}\'}\\n\"']))
