Name: libgcrypt
Version: 1.5.0
Release: 7%{?dist}
URL: http://www.gnupg.org/
Source0: libgcrypt-%{version}-hobbled.tar.bz2
# The original libgcrypt sources now contain potentially patented ECC
# cipher support. We have to remove it in the tarball we ship with
# the hobble-libgcrypt script.
#Source0: ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-%{version}.tar.bz2
#Source1: ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-%{version}.tar.bz2.sig
Source2: wk@g10code.com
Source3: hobble-libgcrypt
# do not run the ecc curves test
Patch1: libgcrypt-1.5.0-noecc.patch
# make FIPS hmac compatible with fipscheck - non upstreamable
Patch2: libgcrypt-1.5.0-use-fipscheck.patch
# fix tests in the FIPS mode, fix the FIPS-186-3 DSA keygen
Patch5: libgcrypt-1.5.0-tests.patch
# add configurable source of RNG seed and seed by default
# from /dev/urandom in the FIPS mode
Patch6: libgcrypt-1.5.0-fips-cfgrandom.patch
# make the FIPS-186-3 DSA CAVS testable
Patch7: libgcrypt-1.5.0-fips-cavs.patch
# add GCRYCTL_SET_ENFORCED_FIPS_FLAG
Patch8: libgcrypt-1.5.0-set-enforced-mode.patch

# Technically LGPLv2.1+, but Fedora's table doesn't draw a distinction.
# Documentation and some utilities are GPLv2+ licensed. These files
# are in the devel subpackage.
License: LGPLv2+
Summary: A general-purpose cryptography library
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gawk, libgpg-error-devel >= 1.4, pkgconfig
BuildRequires: fipscheck
# This is needed only when patching the .texi doc.
BuildRequires: texinfo
Group: System Environment/Libraries

%package devel
Summary: Development files for the %{name} package
License: LGPLv2+ and GPLv2+
Group: Development/Libraries
Requires(pre): /sbin/install-info
Requires(post): /sbin/install-info
Requires: libgpg-error-devel
Requires: %{name} = %{version}-%{release}

%description
Libgcrypt is a general purpose crypto library based on the code used
in GNU Privacy Guard.  This is a development version.

%description devel
Libgcrypt is a general purpose crypto library based on the code used
in GNU Privacy Guard.  This package contains files needed to develop
applications using libgcrypt.

%prep
%setup -q
%{SOURCE3}
%patch1 -p1 -b .noecc
%patch2 -p1 -b .use-fipscheck
%patch5 -p1 -b .tests
%patch6 -p1 -b .cfgrandom
%patch7 -p1 -b .cavs
%patch8 -p1 -b .enforce

mv AUTHORS AUTHORS.iso88591
iconv -f ISO-8859-1 -t UTF-8 AUTHORS.iso88591 >AUTHORS

%build
%configure --disable-static \
%ifarch sparc64
     --disable-asm \
%endif
     --enable-noexecstack \
     --enable-hmac-binary-check \
     --enable-pubkey-ciphers='dsa elgamal rsa' \
     --disable-O-flag-munging
make %{?_smp_mflags}

%check
fipshmac src/.libs/libgcrypt.so.??
make check

# Add generation of HMAC checksums of the final stripped binaries 
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    fipshmac $RPM_BUILD_ROOT/%{_lib}/*.so.?? \
%{nil}

%install
rm -fr $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Change /usr/lib64 back to /usr/lib.  This saves us from having to patch the
# script to "know" that -L/usr/lib64 should be suppressed, and also removes
# a file conflict between 32- and 64-bit versions of this package.
# Also replace my_host with none.
sed -i -e 's,^libdir="/usr/lib.*"$,libdir="/usr/lib",g' $RPM_BUILD_ROOT/%{_bindir}/libgcrypt-config
sed -i -e 's,^my_host=".*"$,my_host="none",g' $RPM_BUILD_ROOT/%{_bindir}/libgcrypt-config

rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir ${RPM_BUILD_ROOT}/%{_libdir}/*.la
/sbin/ldconfig -n $RPM_BUILD_ROOT/%{_libdir}

# Relocate the shared libraries to /%{_lib}.
mkdir -p $RPM_BUILD_ROOT/%{_lib}
for shlib in $RPM_BUILD_ROOT/%{_libdir}/*.so* ; do
	if test -L "$shlib" ; then
		rm "$shlib"
	else
		mv "$shlib" $RPM_BUILD_ROOT/%{_lib}/
	fi
done

# Figure out where /%{_lib} is relative to %{_libdir}.
touch $RPM_BUILD_ROOT/root_marker
relroot=..
while ! test -f $RPM_BUILD_ROOT/%{_libdir}/$relroot/root_marker ; do
	relroot=$relroot/..
done

# Overwrite development symlinks.
pushd $RPM_BUILD_ROOT/%{_libdir}
for shlib in $relroot/%{_lib}/lib*.so.* ; do
	shlib=`echo "$shlib" | sed -e 's,//,/,g'`
	target=`basename "$shlib" | sed -e 's,\.so.*,,g'`.so
	ln -sf $shlib $target
done
popd

# Add soname symlink.
/sbin/ldconfig -n $RPM_BUILD_ROOT/%{_lib}/
rm -f $RPM_BUILD_ROOT/root_marker

# Create /etc/gcrypt (hardwired, not dependent on the configure invocation) so
# that _someone_ owns it.
mkdir -p -m 755 $RPM_BUILD_ROOT/etc/gcrypt

%clean
rm -fr $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
[ -f %{_infodir}/gcrypt.info.gz ] && \
    /sbin/install-info %{_infodir}/gcrypt.info.gz %{_infodir}/dir
exit 0

%preun devel
if [ $1 = 0 -a -f %{_infodir}/gcrypt.info.gz ]; then
    /sbin/install-info --delete %{_infodir}/gcrypt.info.gz %{_infodir}/dir
fi
exit 0

%files
%defattr(-,root,root,-)
%dir /etc/gcrypt
/%{_lib}/libgcrypt.so.*
/%{_lib}/.libgcrypt.so.*.hmac
%doc COPYING.LIB AUTHORS NEWS THANKS

%files devel
%defattr(-,root,root,-)
%{_bindir}/%{name}-config
%{_bindir}/dumpsexp
%{_bindir}/hmac256
%{_includedir}/*
%{_libdir}/*.so
%{_datadir}/aclocal/*

%{_infodir}/gcrypt.info*
%doc COPYING

%changelog
* Mon Dec  3 2012 Tomas Mraz <tmraz@redhat.com> 1.5.0-7
- fix multilib conflict in libgcrypt-config

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr  5 2012 Tomas Mraz <tmraz@redhat.com> 1.5.0-5
- Correctly rebuild the info documentation

* Wed Apr  4 2012 Tomas Mraz <tmraz@redhat.com> 1.5.0-4
- Add GCRYCTL_SET_ENFORCED_FIPS_FLAG command

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 15 2011 Kalev Lember <kalevlember@gmail.com> 1.5.0-2
- Rebuilt for rpm bug #728707

* Thu Jul 21 2011 Tomas Mraz <tmraz@redhat.com> 1.5.0-1
- new upstream version

* Mon Jun 20 2011 Tomas Mraz <tmraz@redhat.com> 1.4.6-4
- Always xor seed from /dev/urandom over /etc/gcrypt/rngseed

* Mon May 30 2011 Tomas Mraz <tmraz@redhat.com> 1.4.6-3
- Make the FIPS-186-3 DSA implementation CAVS testable
- add configurable source of RNG seed /etc/gcrypt/rngseed
  in the FIPS mode (#700388)

* Fri Feb 11 2011 Tomas Mraz <tmraz@redhat.com> 1.4.6-1
- new upstream version with minor changes

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb  4 2011 Tomas Mraz <tmraz@redhat.com> 1.4.5-6
- fix a bug in the fips-186-3 dsa parameter generation code

* Tue Feb  1 2011 Tomas Mraz <tmraz@redhat.com> 1.4.5-5
- use /dev/urandom for seeding in the FIPS mode
- make the tests to pass in the FIPS mode also fixing
  the FIPS-186-3 DSA keygen

* Sun Feb 14 2010 Rex Dieter <rdieter@fedoraproject.org> 1.4.5-4
- FTBFS libgcrypt-1.4.5-3.fc13: ImplicitDSOLinking (#564973)

* Wed Feb  3 2010 Tomas Mraz <tmraz@redhat.com> 1.4.5-3
- drop the S390 build workaround as it is no longer needed
- additional spec file cleanups for merge review (#226008)

* Mon Dec 21 2009 Tomas Mraz <tmraz@redhat.com> 1.4.5-1
- workaround for build on S390 (#548825)
- spec file cleanups
- upgrade to new minor upstream release

* Tue Aug 11 2009 Tomas Mraz <tmraz@redhat.com> 1.4.4-8
- fix warning when installed with --excludedocs (#515961)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Tomas Mraz <tmraz@redhat.com> 1.4.4-6
- and now really apply the padlock patch

* Wed Jun 17 2009 Tomas Mraz <tmraz@redhat.com> 1.4.4-5
- fix VIA padlock RNG inline assembly call (#505724)

* Thu Mar  5 2009 Tomas Mraz <tmraz@redhat.com> 1.4.4-4
- with the integrity verification check the library needs to link to libdl
  (#488702)

* Tue Mar  3 2009 Tomas Mraz <tmraz@redhat.com> 1.4.4-3
- add hmac FIPS integrity verification check

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Tomas Mraz <tmraz@redhat.com> 1.4.4-1
- update to 1.4.4
- do not abort when the fips mode kernel flag is inaccessible
  due to permissions (#470219)
- hobble the library to drop the ECC support

* Mon Oct 20 2008 Dennis Gilmore <dennis@ausil.us> 1.4.3-2
- disable asm on sparc64

* Thu Sep 18 2008 Nalin Dahyabhai <nalin@redhat.com> 1.4.3-1
- update to 1.4.3
- own /etc/gcrypt

* Mon Sep 15 2008 Nalin Dahyabhai <nalin@redhat.com>
- invoke make with %%{?_smp_mflags} to build faster on multi-processor
  systems (Steve Grubb)

* Mon Sep  8 2008 Nalin Dahyabhai <nalin@redhat.com> 1.4.2-1
- update to 1.4.2

* Tue Apr 29 2008 Nalin Dahyabhai <nalin@redhat.com> 1.4.1-1
- update to 1.4.1
- bump libgpgerror-devel requirement to 1.4, matching the requirement enforced
  by the configure script

* Thu Apr  3 2008 Joe Orton <jorton@redhat.com> 1.4.0-3
- add patch from upstream to fix severe performance regression
  in entropy gathering

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4.0-2
- Autorebuild for GCC 4.3

* Mon Dec 10 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.4.0-1
- update to 1.4.0

* Tue Oct 16 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.2.4-6
- use ldconfig to build the soname symlink for packaging along with the
  shared library (#334731)

* Wed Aug 22 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.2.4-5
- add missing gawk buildrequirement
- switch from explicitly specifying the /dev/random RNG to just verifying
  that the non-LGPL ones were disabled by the configure script

* Thu Aug 16 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.2.4-4
- clarify license
- force use of the linux /dev/random RNG, to avoid accidentally falling back
  to others which would affect the license of the resulting library

* Mon Jul 30 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.2.4-3
- disable static libraries (part of #249815)

* Fri Jul 27 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.2.4-2
- move libgcrypt shared library to /%%{_lib} (#249815)

* Tue Feb  6 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.2.4-1
- update to 1.2.4

* Mon Jan 22 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.2.3-2
- make use of install-info more failsafe (Ville Skyttä, #223705)

* Fri Sep  1 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.2.3-1
- update to 1.2.3

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.2-3.1
- rebuild

* Mon Jun 05 2006 Jesse Keating <jkeating@redhat.com> 1.2.2-3
- Added missing buildreq pkgconfig

* Tue May 16 2006 Nalin Dahyabhai <nalin@redhat.com> 1.2.2-2
- remove file conflicts in libgcrypt-config by making the 64-bit version
  think the libraries are in /usr/lib (which is wrong, but which it also
  prunes from the suggest --libs output, so no harm done, hopefully)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.2-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.2-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Oct  5 2005 Nalin Dahyabhai <nalin@redhat.com> 1.2.2-1
- update to 1.2.2

* Wed Mar 16 2005 Nalin Dahyabhai <nalin@redhat.com> 1.2.1-1
- update to 1.2.1

* Fri Jul 30 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- another try to package the symlink

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun May  2 2004 Bill Nottingham <notting@redhat.com> - 1.2.0-1
- update to official 1.2.0

* Fri Apr 16 2004 Bill Nottingham <notting@redhat.com> - 1.1.94-1
- update to 1.1.94

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Feb 21 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- add symlinks to shared libs at compile time

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Mar 20 2003 Jeff Johnson <jbj@redhat.com> 1.1.12-1
- upgrade to 1.1.12 (beta).

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Jeff Johnson <jbj@redhat.com>
- update to 1.1.7
- change license to LGPL.
- include splint annotations patch.
- install info pages.

* Tue Apr  2 2002 Nalin Dahyabhai <nalin@redhat.com> 1.1.6-1
- update to 1.1.6

* Thu Jan 10 2002 Nalin Dahyabhai <nalin@redhat.com> 1.1.5-1
- fix the Source tag so that it's a real URL

* Wed Dec 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- initial package
