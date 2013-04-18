%define major 8
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}

%define majorpp 6
%define libnamepp %mklibname %{name}++ %{majorpp}
%define devnamepp %mklibname -d %{name}++

Summary:	An encoder/decoder for the Free Lossless Audio Codec
Name:		flac
Version:	1.2.1
Release:	14
License:	BSD and GPLv2+
Group:		Sound
Url:		http://flac.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/flac/%{name}-%{version}.tar.gz
Patch1:		flac-1.2.1-asm.patch
Patch2:		flac-1.2.1-gcc43.patch
Patch3:		flac-1.2.1-hidesyms.patch
Patch4:		flac-1.2.1-tests.patch
Patch5:		flac-1.2.1-cflags.patch
Patch6:		flac-1.2.1-bitreader.patch
Patch7:		flac-1.2.1-fix-str-fmt.patch
Patch8:		flac-1.2.1-automake-1.13.patch
Patch9:		ac_config_macro_XMMS.patch

BuildRequires:	libtool
%ifarch %{ix86}
BuildRequires:	nasm
%endif
BuildRequires:	gettext-devel
BuildRequires:	id3lib-devel
BuildRequires:	pkgconfig(ogg)

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
This package contains the C libraries.

%package -n %{devname}
Summary:	Libraries and headers needed for building apps using FLAC
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains the libraries and header files necessary to develop
applications using FLAC written in C.

%package -n %{libnamepp}
Summary:	Shared C++ libraries for FLAC
Group:		System/Libraries

%description  -n %{libnamepp}
This package contains the libraries for C++ applications.

%package -n %{devnamepp}
Summary:	Libraries and headers needed for building apps using FLAC++
Group:		Development/C++
Requires:	%{libnamepp} = %{version}-%{release}
Requires:	%{devname} = %{version}-%{release}
Provides:	%{name}++-devel = %{version}-%{release}

%description -n %{devnamepp}
This package contains the libraries and header files necessary to develop
applications using FLAC written in C++.

%prep
%setup -q
%apply_patches
mv configure.in configure.ac

./autogen.sh -V
rm -rf html
cp -r doc/html .
autoreconf -fi

%build
%configure2_5x \
	--disable-static \
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

%files -n %{devname}
%{_includedir}/FLAC
%{_libdir}/libFLAC.so
%{_datadir}/aclocal/libFLAC.m4
%{_libdir}/pkgconfig/flac.pc

%files -n %{devnamepp}
%{_includedir}/FLAC++
%{_libdir}/libFLAC++.so
%{_datadir}/aclocal/libFLAC++.m4
%{_libdir}/pkgconfig/flac++.pc

