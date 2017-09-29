#!/bin/bash
# vim: dict=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /CoreOS/libgcrypt/smoke-test
#   Description: Test calls upstream test suite.
#   Author: Ondrej Moris <omoris@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2010 Red Hat, Inc. All rights reserved.
#
#   This copyrighted material is made available to anyone wishing
#   to use, modify, copy, or redistribute it subject to the terms
#   and conditions of the GNU General Public License version 2.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE. See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public
#   License along with this program; if not, write to the Free
#   Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301, USA.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Include rhts environment
#. /usr/bin/rhts-environment.sh
. /usr/share/beakerlib/beakerlib.sh

PACKAGE="libgcrypt"

rlJournalStart

    rlPhaseStartSetup
        TmpDir=`mktemp -d`
        rlAssertRpm $PACKAGE
        rlFileBackup --clean "/etc/gcrypt/fips_enabled"
        rlRun "pushd $TmpDir" 0
        rlFetchSrcForInstalled $PACKAGE
        rlRun "rpm -ihv `ls *.rpm`" 0
        if grep '1' /proc/sys/crypto/fips_enabled; then
            rlRun "echo '1' > /etc/gcrypt/fips_enabled" 0
        fi
    rlPhaseEnd

    rlPhaseStartTest
        TOPDIR=`rpm --eval %_topdir`
        rlRun "pushd $TOPDIR" 0
        rlRun "rm -rf BUILD/libgcrypt-*" 0-255
        rlRun "rpmbuild -vv -bc SPECS/libgcrypt.spec" 0
        rlRun "pushd BUILD/libgcrypt-*" 0
        rlRun "fipshmac src/.libs/libgcrypt.so.??" 0
        rlRun "make check > $TmpDir/make_check.out" 0
        rlRun "popd" 0
        rlRun "popd" 0
        rlRun "grep \"All [0-9]\+ tests passed\" $TmpDir/make_check.out" 0 \
            "All tests passed"
        rlRun "cat $TmpDir/make_check.out" 0
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "popd" 0
        rlRun "rm -r $TmpDir" 0
        rlFileRestore
    rlPhaseEnd

rlJournalPrintText
rlJournalEnd
