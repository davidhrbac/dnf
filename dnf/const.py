# const.py
# dnf constants.
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

CONF_FILENAME='/etc/dnf/dnf.conf'
PID_FILENAME = '/var/run/dnf.pid'
PREFIX='dnf'
LOG='dnf.log'
LOG_TRANSACTION='dnf.transaction.log'
TMPDIR='/var/tmp/'
SYSTEM_CACHEDIR='/var/cache/dnf'
CACHEDIR_SUFFIX='$basearch/$releasever'
VERSION_MAJOR=0
VERSION_MINOR=2
VERSION_PATCH=6
VERSION="%d.%d.%d" % (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)
