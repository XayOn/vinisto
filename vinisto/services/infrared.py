""" Vinisto infrarred emitter module """
import re
import subprocess
from contextlib import suppress
from aiohttp import web


def lirc_cfg(file_):
    """ Parse lircd config file """
    def get_remote_values(remote):
        """ Find values for a remote """
        codes_ = re.findall('begin codes(.*?)end codes', remote, re.DOTALL)
        codes = dict([a.split() for a in _clean(codes_[0]).split('\n ') if a])
        values = [a.strip().split(' ', 1) for a in _clean(remote.replace(
            codes_[0], '')).split('\n') if a.strip()]
        values = dict(values)
        values['codes'] = codes
        return values

    def _clean(what):
        return re.sub(' +', ' ', what)

    result = {}
    remotes = re.findall('begin remote(.*?)end remote', file_.read(),
                         re.DOTALL)
    for remote in remotes:
        with suppress(IndexError):
            values = get_remote_values(remote)
            result[values['name']] = values['codes']
    return result


async def run_command(request):
    """ Run a specific command if it exists on the remote """
    remote = request.match_info["remote"]
    cmd = request.match_info["command"]
    assert request.app['remotes'].get(remote, {}).get(cmd, {})
    return web.json_response(
        subprocess.check_call("irsend SEND_ONCE {} {}".format(remote, cmd)))


async def get_remotes(request):
    """ Return loaded remotes """
    return web.json_response(request.app['remotes'])


def run(lircd_cfile):
    """ Run server """
    app = web.Application()
    app['remotes'] = lirc_cfg(open(lircd_cfile[0], 'r'))
    app.router.add_get('/{remote}/{command}', run_command)
    app.router.add_get('/', get_remotes)
    return app
