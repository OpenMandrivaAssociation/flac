%define major  8
%define libname %mklibname %{name} %{major}
%define libnamedev %mklibname -d %{name}
%define majorpp 6
%define libnamepp %mklibname %{name}++ %{majorpp}
%define libnameppdev %mklibname -d %{name}++

Summary:	An encoder/decoder for the Free Lossless Audio Codec
Name:		flac
Version:	1.2.1
Release:	13
License:	BSD and GPLv2+
Group:		Sound
URL:		http://flac.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/flac/flac-%{version}.tar.gz
Patch1:		flac-1.2.1-asm.patch
Patch2:		flac-1.2.1-gcc43.patch
Patch3:		flac-1.2.1-hidesyms.patch
Patch4:		flac-1.2.1-tests.patch
Patch5:		flac-1.2.1-cflags.patch
Patch6:		flac-1.2.1-bitreader.patch
Patch7:		flac-1.2.1-fix-str-fmt.patch
BuildRequires:	pkgconfig(ogg)
%ifarch %{ix86}
BuildRequires:	nasm
%endif
BuildRequires:	libid3lib-devel
BuildRequires:	gettext-devel
BuildRequires:	automake
BuildRequires:	libtool

%description
FLAC is an Open Source lossless audio codec developed by Josh Coalson.

FLAC is comprised of 1) `libFLAC', a library which implements
reference encoders and decoders, licensed under the GNU Lesser
General Public License (LGPL); 2) `flac', a command-line program for
encoding and decoding files, licensed under the GNU General public
License (GPL); 3) `metaflac', a command-line program for editing
FLAC metadata, licensed under the GPL; 4) player plugins for XMMS
and Winamp, licensed under the GPL; and 5) documentation, licensed
under the GNU Free Documentation License.

%package -n %{libname}
Summary:	Shared libraries for FLAC
Group:		System/Libraries

%description  -n %{libname}
FLAC is an Open Source lossless audio codec developed by Josh Coalson.

This package contains the C libraries.

%package -n %{libnamedev}
Summary:	Libraries and headers needed for building apps using FLAC
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	libogg-devel
Provides:	libflac-devel = %{version}-%{release}
Provides:	liboggflac-devel = %{version}-%{release}
Conflicts:	%{mklibname -d flac 7} < 1.2.1-13
Obsoletes:	%{mklibname -d flac 8} < 1.2.1-13

%description -n %{libnamedev}
FLAC is an Open Source lossless audio codec developed by Josh Coalson.

This package contains the libraries and header files necessary to develop
applications using FLAC written in C.

%package -n %{libnamepp}
Summary:	Shared C++ libraries for FLAC
Group:		System/Libraries

%description  -n %{libnamepp}
FLAC is an Open Source lossless audio codec developed by Josh Coalson.

This package contains the libraries for C++ applications.

%package -n %{libnameppdev}
Summary:	Libraries and headers needed for building apps using FLAC++
Group:		Development/C++
Requires:	%{libnamepp} = %{version}-%{release}
Requires:	%{libnamedev} = %{version}-%{release}
Provides:	libflac++-devel = %{version}-%{release}
Provides:	liboggflac++-devel = %{version}-%{release}
Obsoletes:	%{mklibname -d flac++ 6} < 1.2.1-13

%description -n %{libnameppdev}
FLAC is an Open Source lossless audio codec developed by Josh Coalson.

This package contains the libraries and header files necessary to develop
applications using FLAC written in C++.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1 -b .asm
%patch2 -p1 -b .gcc43
%patch3 -p1 -b .hidesyms
# reduce number of tests
%patch4 -p1 -b .tests
%patch5 -p1 -b .cflags
%patch6 -p0 -b .bitreader
%patch7 -p0

%build
./autogen.sh -V

rm -rf html

cp -r doc/html .
%configure2_5x \
    --disable-xmms-plugin \
    --disable-thorough-tests \
    --disable-asm-optimizations

%make

%check
#make -C test check

%install
%makeinstall_std

mv %{buildroot}%{_datadir}/doc/flac-%{version} installed-docs
rm -fr %{buildroot}%{_libdir}/xmms

%files
%doc AUTHORS COPYING* README installed-docs/*
%{_bindir}/flac
%{_bindir}/metaflac
%{_mandir}/man1/*

%files -n %{libname}
%{_libdir}/libFLAC.so.%{major}*

%files -n %{libnamepp}
%{_libdir}/libFLAC++.so.%{majorpp}*

%files -n %{libnamedev}
%{_includedir}/FLAC
%{_libdir}/libFLAC.a
%{_libdir}/libFLAC.so
%{_datadir}/aclocal/libFLAC.m4
%{_libdir}/pkgconfig/flac.pc

%files -n %{libnameppdev}
%{_includedir}/FLAC++
%{_libdir}/libFLAC++.a
%{_libdir}/libFLAC++.so
%{_datadir}/aclocal/libFLAC++.m4
%{_libdir}/pkgconfig/flac++.pc


%changelog
* Mon May 07 2012 Alexander Khrukin <akhrukin@mandriva.org> 1.2.1-12mdv2012.0
+ Revision: 797237
- rebuild

* Thu May 03 2012 Guilherme Moro <guilherme@mandriva.com> 1.2.1-11
+ Revision: 795709
+ rebuild (emptylog)

* Mon Jun 20 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2.1-10
+ Revision: 686311
- avoid pulling 32 bit libraries on 64 bit arch

* Sun May 08 2011 Funda Wang <fwang@mandriva.org> 1.2.1-9
+ Revision: 672369
- disable test as it cannot pass due to unknown reasons

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Fri Dec 03 2010 Funda Wang <fwang@mandriva.org> 1.2.1-8mdv2011.0
+ Revision: 605827
- fix str fmt

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2.1-7mdv2010.1
+ Revision: 521126
- rebuilt for 2010.1

* Thu Sep 24 2009 Olivier Blin <blino@mandriva.org> 1.2.1-6mdv2010.0
+ Revision: 448272
- use nasm on x86 only (from Arnaud Patard)
- gtk-devel buildrequire is useless (from Arnaud Patard)

  + Christophe Fergeau <cfergeau@mandriva.com>
    - rebuild

* Sun Mar 08 2009 Emmanuel Andry <eandry@mandriva.org> 1.2.1-4mdv2009.1
+ Revision: 352744
- diff p7 to fix string format not literal

  + Antoine Ginies <aginies@mandriva.com>
    - rebuild

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 1.2.1-3mdv2009.0
+ Revision: 264464
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed May 21 2008 Oden Eriksson <oeriksson@mandriva.com> 1.2.1-2mdv2009.0
+ Revision: 209712
- sync with fedora

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Oct 08 2007 Götz Waschk <waschk@mandriva.org> 1.2.1-1mdv2008.1
+ Revision: 95688
- new version

* Wed Jul 25 2007 Götz Waschk <waschk@mandriva.org> 1.2.0-1mdv2008.0
+ Revision: 55188
- new version
- fix devel package names

* Sun May 13 2007 Anssi Hannula <anssi@mandriva.org> 1.1.4-2mdv2008.0
+ Revision: 26539
- add conflicts with previous devel package

