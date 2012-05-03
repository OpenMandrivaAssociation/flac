%define major  8
%define libname %mklibname %{name} %{major}
%define libnamedev %mklibname -d %{name}
%define majorpp 6
%define libnamepp %mklibname %{name}++ %{majorpp}
%define libnameppdev %mklibname -d %{name}++

Summary: An encoder/decoder for the Free Lossless Audio Codec
Name: flac
Version: 1.2.1
Release: %mkrel 11
License: BSD and GPLv2+
Group: Sound
URL: http://flac.sourceforge.net/
Source: http://prdownloads.sourceforge.net/flac/flac-%{version}.tar.gz
Patch1: flac-1.2.1-asm.patch
Patch2: flac-1.2.1-gcc43.patch
Patch3: flac-1.2.1-hidesyms.patch
Patch4: flac-1.2.1-tests.patch
Patch5: flac-1.2.1-cflags.patch
Patch6: flac-1.2.1-bitreader.patch
Patch7: flac-1.2.1-fix-str-fmt.patch
BuildRequires: libogg-devel
%ifarch %{ix86}
BuildRequires: nasm
%endif
BuildRequires: libid3lib-devel
BuildRequires: gettext-devel
BuildRequires: automake
BuildRequires: libtool
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
rm -rf %{buildroot} installed-docs

%makeinstall_std

mv %buildroot%_datadir/doc/flac-%{version} installed-docs
rm -fr %buildroot%_libdir/xmms

%if "%{_lib}" == "lib64"
perl -pi -e "s|-L/usr/lib\b|-L%{_libdir}|g" %{buildroot}%{_libdir}/*.la
%endif

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %libnamepp -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %libnamepp -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

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
%{_libdir}/libFLAC.*a
%{_libdir}/libFLAC.so
%_datadir/aclocal/libFLAC.m4
%_libdir/pkgconfig/flac.pc

%files -n %libnameppdev
%defattr(-, root, root)
%{_includedir}/FLAC++
%{_libdir}/libFLAC++.*a
%{_libdir}/libFLAC++.so
%_datadir/aclocal/libFLAC++.m4
%_libdir/pkgconfig/flac++.pc
