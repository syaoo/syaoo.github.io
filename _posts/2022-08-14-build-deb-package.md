---
title: DEB安装包的制作
date: 2022-08-14 22:54
tag: ['linux']
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
    src: /assets/images/cover1.jpg
---

# DEB安装包的制作

`deb`是在Debian及其衍生版Ubuntu、Deepin等Linux系统中使用的应用程序安装包的文件格式，以`.deb`作为其扩展名。通过deb可以方便的分发、安装软件，同时有效管理软件依赖。

## deb文件结构

`deb`文件的本质是包含控制信息和应用程序安装数据的数据包，其中有三个文件。

1. debian-binary - 文件内有一行数据用于标识软件包格式的版本，目前是2.0；
2. 控制文档包 - 一个名为control.tar的文档包，包含维护脚本和软件包的名字、版本、依赖等信息，支持gzip或xz压缩；
3. 数据文档包 - 一个名位data.tar的文档包，包含实际安装的应用程序文件，支持gzip或xz压缩。

使用ar命令解压deb文件，可以看到以上三个文件。

```bash
u@o1:~$ ar -x octave_5.2.0-1_amd64.deb
u@o1:~$ ls -l oct
total 1924
-rw-r--r-- 1 u u    2860 Aug 14 13:19 control.tar.xz
-rw-r--r-- 1 u u 1959252 Aug 14 13:19 data.tar.xz
-rw-r--r-- 1 u u       4 Aug 14 13:19 debian-binary
```

控制文档包中主要包含以下文件：

- **control**：包含软件包的名称、版本、依赖项等信息；
- **md5sums**：包含软件包中所有文件的MD5值，以检测损坏的文件；
- **conffiles**：列出软件包中的配置文件。除非特别说明，否则更新期间不会覆盖配置文件；
- **preinst, postinst, prerm and postrm**：软件安装或删除前、后需要执行的脚本；
- **shlibs**：列出共享库的依赖列表。

其中，只有`control`是必须的文件，其余都可以根据需要使用。关于控制文件各自动的详细说明可查阅：[5. Control files and their fields — Debian Policy Manual v4.6.1.0](https://www.debian.org/doc/debian-policy/ch-controlfields.html#list-of-fields)。

## 制作deb软件包

制作deb包前需要，需要先准备好应用程序所需要的全部文件，可以通过编译或其他方式获得。然后按以下步骤制作软件包。

编译octave

```bash
mkdir build ; cd build
../octave-7.2.0/configure --prefix=/opt/octave-7.2.0 JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64 CPPFLAGS=-I/usr/include/suitesparse:/usr/include/sunlinsol/ 'LDFLAGS=-L/usr/lib/x86_64-linux-gnu/ -Wl,-rpath=/usr/lib/x86_64-linux-gnu/ -L/usr/lib -Wl,-rpath=/usr/lib  -Wl,-rpath=/opt/octave-7.2.0/lib/octave/7.2.0/ -Wl,-rpath='\''$$ORIGIN/../lib/octave/7.2.0/'\''' --without-sundials_nvecserial
make -j8
```

创建工程目录，目录名可以是准备打包的deb包的名字如：`octave_7.2.0_amd64`。

```bash
mkdir $HOME/octave_7.2.0_amd64
```

把应用程序文件复制到工程目录内，如果是源码编译可以使用`make install`安装到工程目录

```bash
make install DESTDIR=$HOME/octave_7.2.0_amd64
```

之后再创建控制文件目录DEBIAN，并增加control文件

```bash
mkdir $HOME/octave_7.2.0_amd64/DEBIAN
touch $HOME/octave_7.2.0_amd64/DEBIAN/control
```

如此，deb打包的工程目录便创建完成，其目录结果如下

```bash
./
├── DEBIAN
│   └──  control
└── opt
    └── octave-7.2.0
        ├── bin
        ├── include
        ├── lib
        ├── libexec
        └── share
```

其中`./opt`，是应用程序的文件所在的顶层目录。应用程序安装时，会把`opt/`及其中的文件复制到系统根目录。

### 编辑control文件

使用文本编辑器打开control文件对其进行编辑，其中需要包含以下字段：

- Package – 应用程序的名字；
- Version – 应用程序的版本号；
- Architecture – 应用程序的所运行的CPU架构，amd64、arm64等；
- Maintainer – 软件包维护者的名字和邮箱；
- Description – 应用程序的简要说明

下面是一个示例：

```yaml
Package: hello
Version: 1.0
Architecture: arm64
Maintainer: Internal Pointers <info@internalpointers.com>
Description: A program that greets you.
 You can add a longer description here. Mind the space at the beginning of this paragraph.
```

除了上面几个基本字段，还有`Depends`也是很重要的一个字段。`Depends`中指定了该应用程序正常运行所依赖的其他软件包。多个软件包间用英文逗号分隔，可以使用竖线`|`表示可选的软件包，在每个软包名的后可加括号注明所需要的版本号。

```yaml
Depends: libbz2-1.0, libc6 (>= 2.29), libccolamd2 (>= 1:4.5.2), libqhull7, libqt5gui5 (>= 5.7.0) | libqt5gui5-gles (>= 5.7.0)
```

在[7. Declaring relationships between packages — Debian Policy Manual v4.6.1.0](https://www.debian.org/doc/debian-policy/ch-relationships.html#)中还介绍了其他如Build-Depends等类型的依赖包设置。

#### 依赖软件包的确定

一个应用程序可能会依赖很多运行库，如何准确的列出这些库的名字是很重要的。应该使用一些工具可以帮助deb包的制作者来查询这些依赖库的，不过我目前没有发现。参考资料[3]中有一个查询编译依赖库Build-Depends的方法，可以作为参考

1. 如果使用configure生成makefile可以使用`dpkg-depcheck`查询编译依赖库

    ```shell
    dpkg-depcheck -d ./configure
    ```

    软件包名字以`-dev`结尾的是编译需要的包，程序运行时使用的依赖库的包名字没有`-dev`。可

2. 使用`objdump`和`dpkg -S`查询可执行文件的依赖库名字

    ```shell
    # 查询依赖库文件名
    objdump -p /usr/bin/foo | grep NEEDED
    # 查询依赖库的deb包名
    dpkg -S libfoo.so.6
    ```

3. 如果有旧版deb包可以参考旧版的的依赖来设置

本次打包octave使用的`control`文件

```yaml
Package: gunoctave
Version: 7.2.0
Priority: extra
Section: universe/math
Architecture: amd64
Installed-Size: 1125848
Maintainer: GUN
Original-Maintainer: Debian Octave Group <team+pkg-octave-team@tracker.debian.org>
Depends: libamd2 (>= 1:4.5.2), libbz2-1.0, libc6 (>= 2.29), libccolamd2 (>= 1:4.5.2), libcholmod3 (>= 1:4.5.2), libcolamd2 (>= 1:4.5.2), libcxsparse3 (>= 1:4.5.2), libfftw3-double3 (>= 3.3.5), libfftw3-single3 (>= 3.3.5), libfltk-gl1.3 (>= 1.3.0), libfltk1.3 (>= 1.3.3), libgcc-s1 (>= 3.0), libgl1, libglpk40 (>= 4.59), libportaudio2 (>= 19+svn20101113), libqhull7, libqscintilla2-qt5-15 (>= 2.11.2), libqt5core5a (>= 5.12.2), libqt5gui5 (>= 5.7.0) | libqt5gui5-gles (>= 5.7.0), libqt5help5 (>= 5.9.0), libqt5network5 (>= 5.0.2), libqt5printsupport5 (>= 5.0.2), libqt5widgets5 (>= 5.11.0~rc1), libqt5xml5 (>= 5.0.2), libsndfile1 (>= 1.0.20), libstdc++6 (>= 9), libsuitesparseconfig5 (>= 1:5.0.0), libx11-6, zlib1g (>= 1:1.2.2), texinfo, libopenblas0-pthread, libspqr2, libgraphicsmagick++-q16-12, libgl2ps1.4, libarpack2, libqrupdate1, libhdf5-103
Recommends: gnuplot-qt | gnuplot-x11 | gnuplot-nox, libopenblas0 | libatlas3-base, pstoedit, epstool, default-jre-headless, octave-doc
Suggests: liboctave-dev
Breaks: liboctave3v5, liboctave4, liboctave5, liboctave6
Description: GNU Octave language for numerical computations
 Octave is a (mostly Matlab (R) compatible) high-level language, primarily
 intended for numerical computations. It provides a convenient command-line
 interface for solving linear and nonlinear problems numerically.
 .
 Octave can be dynamically extended with user-supplied C++ files.
```

### 生成deb包

使用dpkg-deb命令生成deb软件包

```shell
# dpkg-deb --build --root-owner-group  <directory> <package-dir>
dpkg-deb --build --root-owner-group octave_7.2.0_amd64 octave_7.2.0_amd64.deb
```

其中，`--root-owner-group`参数会让deb包中的所有的文件的所有者都是root。这样按照以上操作就可以生成一个deb软件安装包。

## deb软件包测试

deb包制作好之后还需要进行以下必要的测试，如安装、卸载等。

### 安装测试

使用`dpkg`或`apt`在没有安装该软件的目标系统上进行安装测试

```bash
# sudo dpkg -i <package>
sudo dpkg -i octave_7.2.0_amd64.deb
# 或者
# sudo apt install <package>
sudo apt install ./octave_7.2.0_amd64.deb
```

使用dpkg安装时，可能会遇到依赖错误的问题

```bash
dependency problems - leaving unconfigured
```

可以使用下面命令修复

```bash
sudo apt -f install
```

安装后可以看到`/opt/`目录下增加了`octave-7.2.0`及其子目录。同时可以测试程序是否可以正常运行，如提示缺失动态库检查是否安装，若未安装则需要安装并再次测试，同时把安装的软件包增加到`control`文件的`Depends`项中。

### 卸载测试

使用下面的某一命令卸载软件

```bash
# sudo dpkg -r <appname>
sudo dpkg -r octave
# sudo apt remove <appname>
sudo apt remove octave
```

卸载完成后可以查看系统中是否还有该软件

```bash
dpkg -l | grep octave
```

---

1. [deb (file format) - Wikipedia](https://en.wikipedia.org/wiki/Deb_(file_format))
2. [5. Control files and their fields — Debian Policy Manual v4.6.1.0](https://www.debian.org/doc/debian-policy/ch-controlfields.html#list-of-fields)
3. [Chapter 4. Required files under the debian directory](https://www.debian.org/doc/manuals/maint-guide/dreq.en.html)
4. [deb打包 - 光何 - 博客园](https://www.cnblogs.com/guanghe/p/14919957.html)
5. [Building binary deb packages: a practical guide - Internal Pointers](https://www.internalpointers.com/post/build-binary-deb-package-practical-guide)
6. [Building - Octave](https://wiki.octave.org/Building#Dependencies)
7. [7. Declaring relationships between packages — Debian Policy Manual v4.6.1.0](https://www.debian.org/doc/debian-policy/ch-relationships.html#binary-dependencies-depends-recommends-suggests-enhances-pre-depends)