Name: libgcrypt
Version: 1.1.12
Release: 3.1
Source0: ftp://ftp.gnupg.org:/pub/gcrypt/alpha/libgcrypt/libgcrypt-%{version}.tar.gz
Source1: ftp://ftp.gnupg.org:/pub/gcrypt/alpha/libgcrypt/libgcrypt-%{version}.tar.gz.sig
Source2: wk@g10code.com
Patch0: libgcrypt-1.1.7-splint.patch
License: LGPL
Summary: A general-purpose cryptography library.
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Group: System Environment/Libraries

%package devel
Summary: Development files for the %{name} package.
Group: Development/Libraries
PreReq: /sbin/install-info
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
#%patch0 -p0 -b .jbj

%build
%configure --disable-asm
make

%install
rm -fr $RPM_BUILD_ROOT
%makeinstall

# XXX until %%configure is figgered
mv	${RPM_BUILD_ROOT}%{_bindir}/*-libgcrypt-config \
	${RPM_BUILD_ROOT}%{_bindir}/libgcrypt-config || :

rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir
/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}

%clean
rm -fr $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %{_infodir}/gcrypt.info.gz %{_infodir}/dir

%preun devel
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/gcrypt.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%{_libdir}/*.so.*.*
#%{_libdir}/%{name}

%files devel
%defattr(-,root,root)
%{_bindir}/%{name}-config
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_datadir}/aclocal/*
#%{_datadir}/%{name}

%{_infodir}/gcrypt.info*

%changelog
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
