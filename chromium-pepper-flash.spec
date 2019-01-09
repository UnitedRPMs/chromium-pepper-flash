%define debug_package %{nil}
%ifarch x86_64 
%global arch	x86_64
%global plat_lib lib64
%else
%global arch 	i386
%global plat_lib lib
%endif

Summary:        Chromium Flash player plugin 
Name:           chromium-pepper-flash
Version:        32.0.0.114
Release:        2%{?dist}

License:        Proprietary
Url:            http://www.adobe.com/products/flashplayer/
Group:          Applications/Internet
Source:		http://wwwimages.adobe.com/content/dam/acom/en/legal/licenses-terms/pdf/Flash_Player_27_0.pdf
Source1:	mms.cfg	

BuildRequires:  wget tar
Obsoletes: 	chromium-pepper-flash-chromium-pdf-plugin
Provides:	pepper-flash

%description
Pepper API (ppapi) based Adobe Flash plugin for Google's Open Source browser Chromium.

%package -n	flashplugin
Summary:        Adobe Flash Player
Provides:	flash-plugin = %{version}-%{release}

%description -n flashplugin
The flashplugin package contains npapi libraries and header files for Firefox.


%prep

install -dm 755 %{_builddir}/%{name}-%{version}
# PPAPI
wget -c https://fpdownload.adobe.com/pub/flashplayer/pdc/%{version}/flash_player_ppapi_linux.%{arch}.tar.gz
tar xmzvf flash_player_ppapi_linux.%{arch}.tar.gz -C %{_builddir}/%{name}-%{version}

# NPAPI
wget -c https://fpdownload.adobe.com/get/flashplayer/pdc/%{version}/flash_player_npapi_linux.%{arch}.tar.gz
tar xmzvf flash_player_npapi_linux.%{arch}.tar.gz -C %{_builddir}/%{name}-%{version}

%setup -T -D %{name}-%{version}

%build

%install

# PPAPI
install -dm 755 %{buildroot}/%{_libdir}/chromium/PepperFlash/
install -dm 755 %{buildroot}/%{_libdir}/chromium-browser/pepper/
install -dm 755 %{buildroot}/%{_libdir}/chromium-browser/PepperFlash/
install -dm 755 %{buildroot}/usr/share/licenses/%{name}/
install -m644 manifest.json %{buildroot}/%{_libdir}/chromium/PepperFlash/
install -m644 libpepflashplayer.so %{buildroot}/%{_libdir}/chromium/PepperFlash/

ln -sf %{_libdir}/chromium/PepperFlash/manifest.json %{buildroot}/%{_libdir}/chromium-browser/PepperFlash/manifest.json
ln -sf %{_libdir}/chromium/PepperFlash/libpepflashplayer.so %{buildroot}/%{_libdir}/chromium-browser/PepperFlash/libpepflashplayer.so

cat > %{buildroot}/%{_libdir}/chromium-browser/pepper/pepper-flash.info << EOF
# Copyright (c) 2016 The Chromium OS Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

# Registration file for Pepper Flash player.

FILE_NAME=%{_libdir}/chromium/PepperFlash/libpepflashplayer.so
PLUGIN_NAME="Shockwave Flash"
VERSION="%{version}"
VISIBLE_VERSION="%{version}"
DESCRIPTION="$PLUGIN_NAME $VISIBLE_VERSION"
MIME_TYPES="application/x-shockwave-flash"
EOF

# License
install -m644 %{SOURCE0} %{buildroot}/%{_datadir}/licenses/%{name}/
install -m644 LGPL/*.txt %{buildroot}/%{_datadir}/licenses/%{name}/

# NPAPI
install -D libflashplayer.so %{buildroot}/%{_libdir}/mozilla/plugins/libflashplayer.so
  install -D usr/bin/flash-player-properties %{buildroot}/%{_bindir}/flash-player-properties
  install -D usr/%{plat_lib}/kde4/kcm_adobe_flash_player.so %{buildroot}/%{_libdir}/kde4/kcm_adobe_flash_player.so
  
  for size in 16x16 22x22 24x24 32x32 48x48; do
    install -Dm644 usr/share/icons/hicolor/$size/apps/flash-player-properties.png \
      %{buildroot}/usr/share/icons/hicolor/$size/apps/flash-player-properties.png
  done
  install -Dm644 usr/share/applications/flash-player-properties.desktop %{buildroot}/%{_datadir}/applications/flash-player-properties.desktop
  install -Dm644 usr/share/kde4/services/kcm_adobe_flash_player.desktop %{buildroot}/%{_datadir}/kde4/services/kcm_adobe_flash_player.desktop

  install -Dm644 %{S:1} %{buildroot}/etc/adobe/mms.cfg

  install -Dm644 -t %{buildroot}/%{_datadir}/licenses/flashplugin license.pdf 

%files
%dir %{_libdir}/chromium/
%{_libdir}/chromium/PepperFlash/
%{_datadir}/licenses/%{name}/
%{_libdir}/chromium-browser/pepper/pepper-flash.info
%{_libdir}/chromium-browser/PepperFlash/

%files -n flashplugin
%{_libdir}/mozilla/plugins/libflashplayer.so
%{_bindir}/flash-player-properties
%{_libdir}/kde4/kcm_adobe_flash_player.so
%{_datadir}/applications/flash-player-properties.desktop
%{_datadir}/kde4/services/kcm_adobe_flash_player.desktop
%{_sysconfdir}/adobe/mms.cfg
%{_datadir}/licenses/flashplugin/license.pdf
%{_datadir}/icons/hicolor/16x16/apps/flash-player-properties.png
%{_datadir}/icons/hicolor/22x22/apps/flash-player-properties.png
%{_datadir}/icons/hicolor/24x24/apps/flash-player-properties.png
%{_datadir}/icons/hicolor/32x32/apps/flash-player-properties.png
%{_datadir}/icons/hicolor/48x48/apps/flash-player-properties.png

%changelog

* Wed Jan 09 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 32.0.0.114-2
- Updated to 32.0.0.114

* Tue Dec 11 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 32.0.0.101-2
- Updated to 32.0.0.101

* Mon Nov 19 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 31.0.0.153-1
- Updated to 31.0.0.153

* Wed Nov 14 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 31.0.0.148-1
- Updated to 31.0.0.148

* Wed Oct 10 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 31.0.0.122-1
- Updated to 31.0.0.122

* Wed Sep 12 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 31.0.0.108-1
- Updated to 31.0.0.108

* Tue Aug 14 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 30.0.0.154-1
- Updated to 30.0.0.154

* Fri Jul 13 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 30.0.0.134-1
- Updated to 30.0.0.134

* Sat Jun 09 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 30.0.0.113-1
- Updated to 30.0.0.113

* Mon May 07 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 29.0.0.171-1
- Updated to 29.0.0.171

* Tue Apr 10 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 29.0.0.140-1
- Updated to 29.0.0.140

* Wed Mar 14 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 29.0.0.113-1
- Updated to 29.0.0.113

* Tue Feb 06 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 28.0.0.161-1
- Updated to 28.0.0.161

* Tue Jan 09 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 28.0.0.137-1
- Updated to 28.0.0.137

* Tue Dec 12 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 28.0.0.126-1
- Updated to 28.0.0.126

* Wed Nov 15 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 27.0.0.187-1
- Updated to 27.0.0.187

* Wed Oct 25 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 27.0.0.183-1
- Updated to 27.0.0.183

* Sun Oct 22 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 27.0.0.170-1
- Updated to 27.0.0.170

* Wed Oct 11 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 27.0.0.159-1
- Updated to 27.0.0.159

* Fri Sep 22 2017 David Vásquez <davidjeremias82 AT gmail DOT com> - 27.0.0.130-1
- Updated to 27.0.0.130-1

* Thu Aug 10 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 26.0.0.151-1
- Updated to 26.0.0.151

* Mon Jul 17 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 26.0.0.137-1
- Updated to 26.0.0.137

* Tue Jun 20 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 26.0.0.131-1
- Updated to 26.0.0.131

* Thu Jun 15 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 26.0.0.126-1
- Updated to 26.0.0.126

* Thu May 18 2017 David Vásquez <davidjeremias82 AT gmail DOT com> - 25.0.0.171-1
- Updated to 25.0.0.171

* Wed Apr 12 2017 David Vásquez <davidjeremias82 AT gmail DOT com> - 25.0.0.148-1
- Updated to 25.0.0.148

* Sat Mar 18 2017 David Vásquez <davidjeremias82 AT gmail DOT com> - 25.0.0.127-1
- Updated to 25.0.0.127

* Wed Feb 22 2017 David Vásquez <davidjeremias82 AT gmail DOT com> - 24.0.0.221-1
- Updated to 24.0.0.221

* Tue Jan 3 2017 David Vásquez <davidjeremias82 AT gmail DOT com> - 24.0.0.186-2
- Support npapi

* Tue Jan 3 2017 David Vásquez <davidjeremias82 AT gmail DOT com> - 24.0.0.186-1
- Updated to 24.0.0.186

* Tue Sep 13 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 23.0.0.162-1
- Updated to 23.0.0.162

* Tue Jul 12 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 22.0.0.192-1
- Updated to 22.0.0.192

* Tue Jun 21 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 21.0.0.242-2
- Compatibility with chromium-bin

* Wed Jun 15 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 21.0.0.242-1
- Updated to 21.0.0.242

* Sun May 08 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 21.0.0.216-1
- Updated to 21.0.0.216

* Tue Mar 29 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 21.0.0.197-1
- Updated to 21.0.0.197
- Dropped 32 architectures

* Wed Jan 27 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 20.0.0.286-1
- Updated to 20.0.0.286

* Wed Jan 06 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 20.0.0.228-1
- Updated to 20.0.0.228

* Fri Nov 06 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 19.0.0.226-1
- Updated to 19.0.0.226

* Mon Sep 28 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 19.0.0.185-1
- Updated to 19.0.0.185

* Sun Jun 28 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 18.0.0.194-1
- Updated to 18.0.0.194

* Wed Mar 11 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 17.0.0.134-1
- Updated to 17.0.0.134

* Mon Dec 08 2014 David Vásquez <davidjeremias82 AT gmail DOT com> - 16.0.0.257-1
- Updated to 16.0.0.257

* Mon Dec 08 2014 David Vásquez <davidjeremias82 AT gmail DOT com> - 15.0.0.239
- initial build 
