import os
import yum
from glob import glob
from stockpile import util
from stockpile import log

def repo(name, arch=None, baseurls=None, mirrorlist=None):
    yb = util.get_yum()
    if baseurls is not None:
        util.validate_baseurls(baseurls)
        repo = yb.add_enable_repo(name, baseurls=baseurls)
    if mirrorlist is not None:
        util.validate_mirrorlist(mirrorlist)
        repo = yb.add_enable_repo(name, mirrorlist=mirrorlist)
    if arch is not None:
        util.validate_arch_list(arch)
        yb.doSackSetup(thisrepo=name, archlist=arch)
    return repo

def from_file(path):
    if not os.path.exists(path):
        raise exception('No such file or directory: %s' % path)
    yb = util.get_yum()
    yb.getReposFromConfigFile(path)
    for repo in yb.repos.findRepos('*'):
        yb.doSackSetup(thisrepo=repo.getAttribute('name'))
    repos = []
    for repo in yb.repos.findRepos('*'):
        if repo.isEnabled():
            log.info('Added repo %s from file %s' % (repo.id, path))
            repos.append(repo)
        else:
            log.debug('Not adding repo %s because it is disabled' % repo.id)
    return repos

def from_dir(path):
    repos = []
    if os.path.isdir(path):
        for file in sorted(glob('%s/*.repo' % path)):
            for repo in from_file(file):
                repos.append(repo)
    return repos

def set_path(repo, path):
    if type(repo) is not yum.yumRepo.YumRepository:
        raise exception('Repo must be a yum.yumRepo.YumRepository instance')
    repo.pkgdir = path
    return repo