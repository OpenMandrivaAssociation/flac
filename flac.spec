%define name  flac
%define version 1.2.1
%define release %mkrel 1

%define major  8
%define libname %mklibname %{name} %{major}
%define libnamedev %mklibname -d %{name}
%define majorpp 6
%define libnamepp %mklibname %{name}++ %{majorpp}
%define libnameppdev %mklibname -d %{name}++

Name: %name 
Summary: An encoder/decoder for the Free Lossless Audio Codec
Version:  %version
Release:  %release
License: GPL
Group:  Sound
URL: http://flac.sourceforge.net/
Source: http://prdownloads.sourceforge.net/flac/flac-%{version}.tar.gz
BuildRequires: libogg-devel
BuildRequires: nasm
BuildRequires: libid3lib-devel
BuildRequires: gtk-devel
BuildRequires: gettext-devel
BuildRequires: automake1.8

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


%package -n %libname 
Summary: Shared libraries for FLAC
Group:  System/Libraries

%description  -n %libname
FLAC is an Open Source lossless audio codec developed by Josh Coalson.

This package contains the C libraries.

%package -n %libnamedev
Summary: Libraries and headers needed for building apps using FLAC
Group: Development/C
Requires: %{libname} = %{version}-%release
Requires: libogg-devel
Provides:  libflac-devel = %version-%release
Provides:  liboggflac-devel = %version-%release
Conflicts: %mklibname -d flac 7
Obsoletes: %mklibname -d flac 8

%description -n %libnamedev
FLAC is an Open Source lossless audio codec developed by Josh Coalson.

This package contains the libraries and header files necessary to develop
applications using FLAC written in C.

%package -n %libnamepp
Summary: Shared C++ libraries for FLAC
Group: System/Libraries

%description  -n %libnamepp
FLAC is an Open Source lossless audio codec developed by Josh Coalson.

This package contains the libraries for C++ applications.

%package -n %libnameppdev
Summary: Libraries and headers needed for building apps using FLAC++
Group: Development/C++
Requires: %{libnamepp} = %{version}-%release
Requires: %libnamedev = %version-%release
Provides:  libflac++-devel = %version-%release
Provides:  liboggflac++-devel = %version-%release
Obsoletes: %mklibname -d flac++ 6

%description -n %libnameppdev
FLAC is an Open Source lossless audio codec developed by Josh Coalson.

This package contains the libraries and header files necessary to develop
applications using FLAC written in C++.

%prep
%setup -q -n %name-%version

%build
rm -rf html

cp -r doc/html .
%configure2_5x --disable-xmms-plugin
%make

%install
rm -rf %{buildroot} installed-docs
%makeinstall_std
mv %buildroot%_datadir/doc/flac-%{version} installed-docs
rm -fr %buildroot%_libdir/xmms

%clean
rm -rf %{buildroot}

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig
%post -n %libnamepp -p /sbin/ldconfig
%postun -n %libnamepp -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc AUTHORS COPYING* README installed-docs/*
%{_bindir}/flac
%{_bindir}/metaflac
%{_mandir}/man1/*

%files -n %libname 
%defattr(-, root, root)
%_libdir/libFLAC.so.%{major}*

%files -n %libnamepp 
%defattr(-, root, root)
%_libdir/libFLAC++.so.%{majorpp}*

%files -n %libnamedev
%defattr(-, root, root)
%{_includedir}/FLAC
%{_libdir}/libFLAC.a
%{_libdir}/libFLAC.la
%{_libdir}/libFLAC.so
%_datadir/aclocal/libFLAC.m4
%_libdir/pkgconfig/flac.pc

%files -n %libnameppdev
%defattr(-, root, root)
%{_includedir}/FLAC++
%{_libdir}/libFLAC++.a
%{_libdir}/libFLAC++.la
%{_libdir}/libFLAC++.so
%_datadir/aclocal/libFLAC++.m4
%_libdir/pkgconfig/flac++.pc


