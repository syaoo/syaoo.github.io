---
title: linuxdeploy
date: 2022-05-23 15:59
tag: ['tag1','tag2']
mathjax: false
mathjax_autoNumber: true
# Mermaid
mermaid: false
# Chart
chart: false
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover3.jpg
---

abstract

<!--more-->

### appimage制作

calcdata的解决

```
../linuxdeploy-x86_64.AppImage --appdir=/home/a2/Downloads/ns/nusolve_appimage/ -p qt --custom-apprun /home/a2/Downloads/for_get_env/nusolve.sh -o appimage
```

输出appimage需要完善添加启动脚本、desktop文件、图标文件。


使用ORIGIN
[makefile - Difficulty adding $ORIGIN to LDFLAGS - Stack Overflow](https://stackoverflow.com/questions/62034115/difficulty-adding-origin-to-ldflags)

[Creating relocatable Linux executables by setting RPATH with $ORIGIN | by Luke Chen | Medium](https://nehckl0.medium.com/creating-relocatable-linux-executables-by-setting-rpath-with-origin-45de573a2e98)

configure --prefix=/usr --with-calc-datadir=/data/calc/apri LDFLAGS="-L/home/a2/.local/miniconda3/envs/ns/lib/ -Wl,-R'\$\$ORIGIN../lib' -Wl,-R/home/a2/.local/miniconda3/envs/ns/lib/ -Wl,-as-needed"  --with-netcdf-include=/home/a2/.local/miniconda3//envs/ns/include --with-netcdf-lib=/home/a2/.local/miniconda3/envs/ns/lib F77=gfortran --with-hops-dir=/home/a2/Downloads/ns/hops_bin/usr/

使用$ORIGIN/../lib能避免多次对同一个目录使用linux_deploy后nuSolve打开"Edit"-"Edit general config"程序会卡死的问题，这可能是由某些库的错误引用造成的。

[Packaging native binaries — AppImage documentation](https://docs.appimage.org/packaging-guide/from-source/native-binaries.html#packaging-from-source)
[Releases · linuxdeploy/linuxdeploy](https://github.com/linuxdeploy/linuxdeploy/releases/)
[linuxdeploy/linuxdeploy-plugin-qt: Qt plugin for linuxdeploy, bundling Qt resources, plugins, QML files and a lot more.](https://github.com/linuxdeploy/linuxdeploy-plugin-qt)



[linuxdeploy/linuxdeploy-plugin-appimage: Plugin for linuxdeploy. Creates AppImages from AppDirs.](https://github.com/linuxdeploy/linuxdeploy-plugin-appimage)
[linuxdeploy/linuxdeploy-plugin-qt: Qt plugin for linuxdeploy, bundling Qt resources, plugins, QML files and a lot more.](https://github.com/linuxdeploy/linuxdeploy-plugin-qt)
[User Guide — AppImage documentation](https://docs.appimage.org/user-guide/index.html)

[appimage-builder documentation — appimage-builder 1.0.0 documentation](https://appimage-builder.readthedocs.io/en/latest/index.html)

---

**参考**
1. [Welcome to the AppImage documentation — AppImage documentation](https://docs.appimage.org/index.html)
2. 
