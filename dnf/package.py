# package.py
# Module defining the dnf.Package class.
#
# Copyright (C) 2012  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#

import binascii
import hawkey
import os.path
import yum.misc

class Package(hawkey.Package):
    def __init__(self, initobject, yumbase):
        super(Package, self).__init__(initobject)
        self.yumbase = yumbase
        self.localpath = None
        self._size = None
        self._chksum = None

    @property
    def chksum(self):
        if self._chksum:
            return self._chksum
        return super(Package, self).chksum

    @chksum.setter
    def chksum(self, val):
        self._chksum = val

    @property
    def size(self):
        if self._size:
            return self._size
        return super(Package, self).size

    @size.setter
    def size(self, val):
        self._size = val

    @property # yum compatibility attribute
    def idx(self):
        return self.rpmdbid

    @property # yum compatibility attribute
    def repoid(self):
        return self.reponame

    @property # yum compatibility attribute
    def pkgtup(self):
        return (self.name, self.arch, str(self.e), self.v, self.r)

    @property # yum compatiblity attribute
    def repo(self):
        return self.yumbase.repos.repos[self.reponame]

    @property # yum compatiblity attribute
    def relativepath(self):
        return self.location

    @property # yum compatibility attribute
    def a(self):
        return self.arch

    @property # yum compatibility attribute
    def e(self):
        split = self.evr.split(":", 1)
        if len(split) > 1:
            return int(split[0])
        else:
            return 0

    @property # yum compatibility attribute
    def v(self):
        vr = self.evr.split(":", 1)[-1]
        return vr.split("-")[0]

    @property # yum compatibility attribute
    def r(self):
        vr = self.evr.split(":", 1)[-1]
        return vr.split("-")[1]

    @property # yum compatibility attribute
    def ui_from_repo(self):
        return self.reponame

    # yum compatibility method
    def getDiscNum(self):
        return self.medianr

    # yum compatibility method
    def localPkg(self):
        """ Package's location in the filesystem.

            For packages in remote repo returns where the package will be/has
            been downloaded.
        """
        if self.reponame == hawkey.CMDLINE_REPO_NAME:
            return self.location
        return self.localpath or \
            os.path.join(self.repo.pkgdir, os.path.basename(self.location))

    # yum cmopatibility method
    def verifyLocalPkg(self):
        if self.reponame == hawkey.SYSTEM_REPO_NAME:
            raise ValueError, "Can not verify an installed package."
        if self.reponame == hawkey.CMDLINE_REPO_NAME:
            return True # local package always verifies against itself
        (chksum_type, chksum) = self.chksum
        chksum_type = hawkey.chksum_name(chksum_type)
        sum_in_md = binascii.hexlify(chksum)
        real_sum = yum.misc.checksum(chksum_type, self.localPkg(),
                                     datasize=self.size)
        return real_sum == sum_in_md
