# yumsync - A tool for mirroring and versioning YUM repositories.
# Copyright 2013 Ryan Uber <ru@ryanuber.com>. All rights reserved.
#
# MIT LICENSE
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os

def make_dir(path):
    """ Create a directory recursively, if it does not exist. """
    if not os.path.exists(path):
        os.makedirs(path)

# path = path to symlink
# target = path to real file
def symlink(path, target):
    """ Create a symbolic link.
    Determines if a link in the destination already exists, and if it does,
    updates its target. If the destination exists but is not a link, throws an
    exception. If the link does not exist, it is created.
    """
    if not os.path.islink(path):
        if os.path.exists(path):
            raise Exception('%s exists - Cannot create symlink' % path)
        path_dir = os.path.dirname(path)
        if not os.path.exists(path_dir):
            make_dir(path_dir)
    elif os.readlink(path) != target:
        os.unlink(path)
    if os.path.lexists(path):
        return False
    else:
        os.symlink(target, path)
        return True

def hardlink(source, target):
    " This method creates a hardlink ... "
    if source != target:
        # ensure source exists and collect stats
        if not os.path.exists(source):
            raise Exception('%s does not exist - Cannot create hardlink' % source)
        else:
            source_stat = os.stat(source)
        # create target dir if missing
        target_dir = os.path.dirname(target)
        if not os.path.exists(target_dir):
            make_dir(target_dir)
        # if target is a symlink, unlink
        if os.path.islink(target):
            os.unlink(target)
        # get dev and inode info for target
        if os.path.exists(target):
            target_dev = os.stat(target).st_dev
            target_inode = os.stat(target).st_ino
        else:
            target_dev = os.stat(target_dir).st_dev
            target_inode = None
        if target_dev != source_stat.st_dev:
            raise Exception('source device %s is not equal to target device %s - Cannot create hardlink' %
                            (source_stat.st_dev, target_dev))
        elif (target_inode is not None) and (target_inode != source_stat.st_ino):
            os.unlink(target)

        if os.path.exists(target):
            return False
        else:
            os.link(source, target)
            return True
