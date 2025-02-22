{pkgs}: {
  deps = [
    pkgs.glibcLocales
    pkgs.xorg.libXi
    pkgs.xorg.libXtst
    pkgs.xorg.libX11
  ];
}
