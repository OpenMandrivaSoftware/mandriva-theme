%define scriptdir %{_datadir}/bootsplash/scripts
%define mdk_bg %{_datadir}/mdk/backgrounds

%define release 1

%define theme_header() \
Summary:	%{vendor}%{?1:-%1} theme for plymouth and desktop background \
Group:		Graphics \
\
%description	%{?1} \
This package contains the %{?1:-%1} plymouth theme \
with its images and configuration for different resolution as well as \
the the desktop background image. \

%define theme_package(o:) \
%package	%{1} \
Requires:	plymouth-system-theme \
Requires:	plymouth-plugin-script >= 0.8.2 \
Provides:	mandrake_theme mandrake-theme mandrakelinux-theme mandriva-theme = %{version}-%{release} \
Provides:	distro-theme = %{EVRD} \
Provides:	plymouth(system-theme) \
Obsoletes:	mandrake_theme mandrake-theme mandrakelinux-theme %{?-o:%{-o*}} \
Requires:	distro-theme-common \
Suggests:	distro-theme-screensaver \
Conflicts:	kdebase-konsole <= 1:3.4.2-37mdk \
%rename		mandriva-theme-Flash \
%rename		mandriva-theme-Free \
%rename		mandriva-theme-One \
%rename		mandriva-theme-Powerpack \
%rename		mandriva-theme-Moondrake \
%rename		mandriva-theme-OpenMandriva \
%theme_header(%{1})

%define theme_scripts() \
%post -n %{name}-%{1} \
if [ -z "$DURING_INSTALL" ]; then \
  if [ -x %scriptdir/switch-themes ]; then \
    %scriptdir/switch-themes %{1} \
  fi \
else \
  if [ -f /etc/sysconfig/bootsplash ]; then \
    perl -pi -e 's/^\s*SPLASH=.*/SPLASH=auto/; s/^\s*THEME=.*/THEME=%{1}/' /etc/sysconfig/bootsplash \
  fi \
  %{_sbindir}/plymouth-set-default-theme %{1} \
fi \
if [ -f %mdk_bg/%{1}-root.png -a ! -f %mdk_bg/root/default.png -o -L %mdk_bg/root/default.png ]; then \
  rm -f %mdk_bg/root/default.png \
  ln -s %{1}-root-1600x1200.png %mdk_bg/root/default.png \
fi \
if [ -f %mdk_bg/%{1}.jpg -a ! -f %mdk_bg/default.jpg -o -L %mdk_bg/default.jpg ]; then \
  rm -f %mdk_bg/default.jpg \
  ln -s %{1}.jpg %mdk_bg/default.jpg \
fi \
\
%triggerpostun -n %{name}-%{1} -- mandriva-theme-%{1} < 1.2.4 \
for f in kdeglobals konsolerc; do \
  if [ "`readlink /usr/share/config/$f 2>/dev/null`" == "$f-%{1}" ]; then \
    rm -f /usr/share/config/$f \
  fi \
done \
\
%preun -n %{name}-%{1} \
if [ "$1" == "0" ]; then \
  if [ -x %scriptdir/remove-theme ]; then \
    %scriptdir/remove-theme %{1} \
  fi \
  link=`readlink %mdk_bg/default.png` \
  slink=${link%%-*} \
  if [ "$slink" == "%{1}" ]; then rm -f %mdk_bg/default.png;fi \
  link=`readlink %mdk_bg/default.jpg` \
  slink=${link%%-*} \
  if [ "$slink" == "%{1}" ]; then rm -f %mdk_bg/default.jpg;fi \
  link=`readlink %mdk_bg/%{1}.png` \
  slink=${link%%-*} \
  if [ "$slink" == "%{1}" ]; then rm -f %mdk_bg/%{1}.png;fi \
  link=`readlink %mdk_bg/%{1}.jpg` \
  slink=${link%%-*} \
  if [ "$slink" == "%{1}" ]; then rm -f %mdk_bg/%{1}.jpg;fi \
  link=`readlink %mdk_bg/root/%{1}.png` \
  slink=${link%%-*} \
  if [ "$slink" == "%{1}-root" ]; then rm -f %mdk_bg/root/default.png;fi \
fi

%define theme_files() \
%files %{1} \
%_datadir/gfxboot/themes/%{1} \
%_datadir/plymouth/themes/%{1} \
%mdk_bg/%{1}* \

Name:		distro-theme
Version:	1.4.16
Release:	1
Source0:	%{name}-%{version}.tar
License:	GPLv2+
BuildArch:	noarch
BuildRequires:	gimp fonts-ttf-dejavu imagemagick
%theme_header

%theme_package Moondrake      -o distro-theme
%theme_package OpenMandriva   -o distro-theme

%package	common
Summary:	%{vendor} common theme for plymouth
Group:		Graphics
Obsoletes:	plymouth-theme-mdv
%rename		mandriva-theme-common

%description	common
This package contains common images for the %{vendor} plymouth themes.

%package	extra
Summary:	Additional backgrounds from %{distribution} users
Group:		Graphics
%rename		mandriva-theme-extra

%description	extra
This package contains winning picture from Mandriva 2010 photo 
background contest.

%package	screensaver
Summary:	%{distribution} screensaver
Group:		Graphics
%rename		mandriva-theme-Free-screensaver
%rename		mandriva-theme-Powerpack-screensaver
%rename		mandriva-theme-One-screensaver
%rename		mandriva-theme-Flash-screensaver
%rename		mandriva-theme-Rosa-screensaver
%rename		mandriva-screensaver

%description	screensaver
This package contains the %{vendor} screensaver.

%prep
%setup -q

%build
%make

%install
%make install prefix=%{buildroot}

# Default wallpaper should be available without browsing file system
mkdir -p %{buildroot}%{_datadir}/wallpapers
ln -s Moondrake-1920x1440.jpg %{buildroot}%{_datadir}/mdk/backgrounds/Moondrake.jpg

ln -s ../mdk/backgrounds/default.jpg %{buildroot}%{_datadir}/wallpapers/default.jpg

%theme_scripts Moondrake
%theme_scripts OpenMandriva

%files common
%{_datadir}/wallpapers/default.jpg

%files extra
%{_datadir}/mdk/backgrounds/Antes_del_vuelo.jpg
%{_datadir}/mdk/backgrounds/fields.jpg
%{_datadir}/mdk/backgrounds/hibiscus.jpg
%{_datadir}/mdk/backgrounds/Rustic_Chair.jpg
%{_datadir}/mdk/backgrounds/Autumn.jpg
%{_datadir}/mdk/backgrounds/Flower.jpg
%{_datadir}/mdk/backgrounds/Ice.jpg
%{_datadir}/mdk/backgrounds/Smiley01.jpg
%{_datadir}/mdk/backgrounds/chevalier.jpg
%{_datadir}/mdk/backgrounds/gouttes2500.jpg
%{_datadir}/mdk/backgrounds/night_swim.jpg
%{_datadir}/mdk/backgrounds/Beach.jpg
%{_datadir}/mdk/backgrounds/Cat.jpg
%{_datadir}/mdk/backgrounds/Event.jpg
%{_datadir}/mdk/backgrounds/Flowers.jpg
%{_datadir}/mdk/backgrounds/Sunset.jpg
%{_datadir}/mdk/backgrounds/Canal.jpg

%{_datadir}/mdk/backgrounds/Mandriva-extra.xml

%files screensaver
%dir %{_datadir}/mdk/screensaver
%{_datadir}/mdk/screensaver/*-*.png

%theme_files OpenMandriva
%theme_files Moondrake
