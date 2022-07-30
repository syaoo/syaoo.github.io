$\nu$Solve软件包从0.5及以后的版本，包含**$\nu$Solve**、**vgosDbMake**、**vgosDbCalc**和**vgosDbProcLogs**四个程序。
vgosDbMake 从条纹文件中提取数据，并创建一个vgosDb数据集文件(The utility vgosDbMake extracts some data from fringe files and creates a vgosDb set of files for a VLBI session)。
vgosDbCalc 计算理论值和偏导数，并以vgosDb形式存储数据(vgosDbCalc calculates theoretical values and partials, stores these information in the vgosDb format)。
vgosDbProcLogs 从测站站日志文件中提取其他信息（电缆校准和气象参数），并将其添加到vgosDb数据集中(The utility vgosDbProcLogs extracts additional information (cable calibration and meteorological parameters) from stations log files and adds it to a vgosDb set of files.)。

[toc]

## 软硬件需求
该软件对于硬件无特殊要求，现代通用计算机都可以运算。软件在Linux系统上开发，可以兼容任何POSIX系统。此外还需要Qt、netCDF以及HOPS（可选，vgosDbMake需要）运行库的支持。

## 安装基础开发环境gcc、g++、gfotran、make
同一个软件在不同发行版本下可能使用不同的软件包名称，安装时会有所不同。

```bash
# 1. CentOS
# CentOS中的安装命令`yum`在CentOS 8 也可以使用`dnf`。
sudo yum make gcc gcc-c++ gcc-gfortran

# 2. Debian
sudo apt install make gcc g++ gfortran
```

## 必要依赖库的安装
目前各linux发行版本的软件仓库中通常都包含Qt及netCDF相关软件包可供安装，HOPS可以从Haystack的FTP站点下载（ftp://gemini.haystack.mit.edu/pub/hops/ ）。所以除HOPS需要编译安装外，其他都可以比较方便的从各Linux发行版本的软件库中安装。

### Qt
从0.7.1版本之前的版本仅支持Qt4，0.7.1及之后可以使用Qt4或Qt5进行编译安装（不过在安装过程中发现0.7.1使用Qt5或Qt4均有问题）

如无使用进行程序Qt开发的需求**推荐直接从软件仓库安装Qt环境即可**

#### 从软件仓库安装

```bash
# 1. CentOS（以下使用的命令在CentOS 8及 CentOS7验证）
sudo yum install qt5-qtbase-devel qt5-qtbase
# 如果不放心也可使用`qt5-qtbase*`安装所有qt5-base相关组件，在CentOS官方源中似乎没有qt4。

# 2. Debina (Debina 10及Ubuntu20测试)，推荐安装qt5>=5.12.0
sudo apt install qt4-default #安装qt4
sudo apt install qt5-default #安装qt5
```

#### 源码安装

Qt各版本的安装文件及源码可以在这里下载：https://download.qt.io/archive/qt/ 其中有些版本会提供安装程序（\*.run）也可直接使用安装程序安装。
源码下载解压后，进入源码目录下，安装基本可分为三步：
- 生成Makefile文件 `./configure`
- 编译程序 `make`
- 安装 `make install`
第一步中可以指定如一些参数，如 `--prefix=/opt/qt`指定qt安装的路径为`/opt/qt`；`-opensource`参数指定使用开源许可等，其他参数可以使用`./configure --help`。另外在安装过程中可能会在第一、二步遇到一些错误，通常为缺失依赖库，可根据提示进行安装或指定依赖库的路径。**搜索引擎（[百度](https://www.baidu.com)、[Google](https://www.google.com)）是个好东西**。
下面有几个我安装过程中遇到的问题及解决方法，可做参考：

1. 安装Qt5时遇到:ERROR: The OpenGL functionality tests failed!
```
ERROR: The OpenGL functionality tests failed!
You might need to modify the include and library search paths by editing QMAKE_INCDIR_OPENGL[_ES2],
QMAKE_LIBDIR_OPENGL[_ES2] and QMAKE_LIBS_OPENGL[_ES2] in the mkspec for your platform.
```
**解决方法**：
在CentOS上，安装需要的依赖库`sudo dnf install mesa-libGL-devel mesa-libGLU-devel -y`，之后`rm config.cache`删除configure记录，重新运行configure。

2. 安装Qt5遇到：error: one or more PCH files were found, but they were invalid
```
cc1plus: error: one or more PCH files were found, but they were invalid
cc1plus: error: use -Winvalid-pch for more information
cc1plus: fatal error: .pch/release-shared/Qt5Core: No such file or directory
compilation terminated.
```
**解决方法**：
执行configure命令时添加`-no-pch`参数。

3. 提示没有python命令
目前新发行的系统中默认只有python3.6，可以使用建立软链接的方式将python命令指向python3如：
```
ln -s /usr/bin/python3.6 /usr/bin/python
```
为python3增加一个python别名应该也可以`alias python=python3`。

### netCDF

```bash
# 1. CentOS(以下使用的命令在CentOS 8及 CentOS7验证)
sudo dnf install zlib-devel.x86_64 #已安装
sudo dnf install epel-release-8-8.el8.noarch -y #安装扩展源，扩展源有hdf5
sudo dnf install hdf5-devel #安装hdf5
sudo dnf install netcdf-devel.x86_64 # 安装netcdf

# 如果安装hdf5-devel是提升无法安装libaec可尝试下面的命令
sudo dnf --enablerepo=PowerTools install libaec-devel

# 2. Debian
sudo apt install libhdf5-dev libnetcdf-dev
```

这里安装的zlib、hdf5、netcdf也都可使用源码安装，安装过程与Qt基本相似。
netCDF源码可以从这里下载：ftp://ftp.unidata.ucar.edu/pub/netcdf/

### HOPS
如果需要编译vgosDbMake，需要安装HOPS，下载地址：ftp://gemini.haystack.mit.edu/pub/hops/
HOPS通过源码安装，过程与Qt源码安装类似：
- 安装HOPS依赖库：gplot可从 https://pkgs.org/ 查询不同发现版本系统对应的软件包名称。
如CentOS 8需要的软件包为：pgplot-devel-5.2.2-47.el8.x86_64.rpm

![dMtcnK.png](https://s1.ax1x.com/2020/08/18/dMtcnK.png)

详情页可是看到安装方法(Install Howto)：
>1. Download latest rpmfusion-nonfree-release rpm from:
>http://download1.rpmfusion.org/nonfree/el/updates/testing/8/x86_64/
>2. Install rpmfusion-nonfree-release rpm:
>`# rpm -Uvh rpmfusion-nonfree-release*rpm`
>3. Install pgplot-devel rpm package:
>`# dnf install pgplot-devel`

进入HOPS源码目录，新建build目录并进入该目录，然后依次执行：
```shell
../hops-3.21/configure --prefix=$HOME/hops # 指定安装目录为用户目录下的hops目录内
make install
```
**详细内容可查看README文件**。

## $\nu$Solve安装
nuSolve可以从[sourceforge](https://sourceforge.net/projects/nusolve/)下载源码安装。
同样安装可以分为三步（进如源码目录）：
- 生成Makefile文件 `./configure`
- 编译程序 `make`
- 安装 `make install`
注意，第一步中，如果前面有通过源码安装的依赖且安装在非默认安装位置，同样需要相应的参数来指定所需要的库及头文件的位置。如：
```shell
--with-qt-dir=[PATH_TO_QT-4.8] # 指定Qt安装目录
# 如果Qt的库没有放置在安装目录下，还需要下面参数分别给出
--with-qt-include =[PATH_TO_QT-4.8 includes]
--with-qt-lib=[PATH_TO_QT-4.8 libraries]
--with-qt-bin=[PATH_TO_QT-4.8 binaries (the utility 'moc')]
```
指定netCDF位置
```shell
--with-netcdf-include =[PATH_TO_NETCDF includes]
--with-netcdf-lib=[PATH_TO_NETCDF libraries]
```
**默认是不编译vgosDbMake的，如需编译则应给出HOPS文件路径**：
```shell
--with-hops-dir=[PATH_TO_HOPS]
# 或者
--with-hops-include=[PATH_TO_HOPS include files]
--with-hops-lib=[PATH_TO_HOPS libraries]
--with-hops-share=[PATH_TO_HOPS shared data]
```

### 安装遇到的问题及解决

1. 编译错误：error: '::malloc' has not been declared

```
In file included from /usr/include/c++/8/ext/string_conversions.h:41,
from /usr/include/c++/8/bits/basic_string.h:6400,
from /usr/include/c++/8/string:52,
from /usr/include/c++/8/bits/locale_classes.h:40,
from /usr/include/c++/8/bits/ios_base.h:41,
from /usr/include/c++/8/ios:42,
from /usr/include/c++/8/ostream:38,
from ./Sg3dVector.h:35,
from Sg3dVector.cpp:23:
/usr/include/c++/8/cstdlib:151:11: error: '::malloc' has not been declared
using ::malloc;
^~~~~~
make[2]: *** [Makefile:790: Sg3dVector.lo] Error 1
make[2]: Leaving directory '/home/vgos/csfile/dir/nusolve-0.7.1/src/SgLib'
make[1]: *** [Makefile:579: all-recursive] Error 1
make[1]: Leaving directory '/home/vgos/csfile/dir/nusolve-0.7.1'
make: *** [Makefile:413: all] Error 2
```

**解决方法**：
这个问题通常发生在netcdf没有安装在默认位置，系统不能自动寻找到所需要的库文件，可以使用`LD_LIBRARY_PATH`指定netcdf库的位置：

```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/local/netcdf/lib
./configure --prefix=/usr --with-netcdf-include=$HOME/local/netcdf/include --with-netcdf-lib=$HOMElocal/netcdf/lib #重新生成Makefile
make
```
参考：http://104.197.24.192/unstumping-the-internet/malloc-has-not-been-declared/#rootcause

2. 编译过程中找不到文件- error: QtCore/QString: No such file or directory

```
SgMatrix.cpp:25:10: fatal error: QtCore/QString: No such file or directory
#include <QtCore/QString>
^~~~~~~~~~~~~~~~
compilation terminated.
make[2]: *** [Makefile:790: SgMatrix.lo] Error 1
make[2]: Leaving directory '/home/test/Downloads/nusolve-0.7.1/src/SgLib'
make[1]: *** [Makefile:579: all-recursive] Error 1
make[1]: Leaving directory '/home/test/Downloads/nusolve-0.7.1'
make: *** [Makefile:413: all] Error 2
```
**解决方法**：
查找文件路径手动指定
```
./configure --prefix=$HOME/ns --with-qt-include=/usr/include/qt5 --with-qt-dir=/usr/include/qt5
```

3. 编译过程中找不到moc命令
```
/usr/bin/moc SgGuiLogger.h -o SgGuiLogger.moc.cpp
make[2]: /usr/bin/moc: Command not found
make[2]: *** [Makefile:994: SgGuiLogger.moc.cpp] Error 127
make[2]: Leaving directory '/home/test/test/nusolve-0.7.0/src/SgLib'
make[1]: *** [Makefile:526: all-recursive] Error 1
make[1]: Leaving directory '/home/test/test/nusolve-0.7.0'
make: *** [Makefile:395: all] Error 2
```
**解决方法**：
确认moc位置，使用MOC参数手动指定如：
```
./configure --prefix=$HOME/ns MOC='/usr/local/Trolltech/Qt-4.8.7/bin/moc'
```
4. 使用Qt5编译nuSolve 0.7.1时遇到的编译错误
```
/bin/sh ../../libtool --tag=CXX --mode=compile g++ -DHAVE_CONFIG_H -I. -I../.. -I/Qt5.12.0/5.12.0/gcc_64/include -I/home/test/local/netcdf/include -Wall -W -Wpointer-arith -Wcast-align -Wredundant-decls -DDEBUG -g -ggdb -O3 -fopenmp -g -Wall -W -Wpointer-arith -Wcast-align -Wredundant-decls -DDEBUG -MT SgMatrix.lo -MD -MP -MF .deps/SgMatrix.Tpo -c -o SgMatrix.lo SgMatrix.cpp
libtool: compile: g++ -DHAVE_CONFIG_H -I. -I../.. -I/Qt5.12.0/5.12.0/gcc_64/include -I/home/test/local/netcdf/include -Wall -W -Wpointer-arith -Wcast-align -Wredundant-decls -DDEBUG -g -ggdb -O3 -fopenmp -g -Wall -W -Wpointer-arith -Wcast-align -Wredundant-decls -DDEBUG -MT SgMatrix.lo -MD -MP -MF .deps/SgMatrix.Tpo -c SgMatrix.cpp -fPIC -DPIC -o .libs/SgMatrix.o
libtool: compile: g++ -DHAVE_CONFIG_H -I. -I../.. -I/Qt5.12.0/5.12.0/gcc_64/include -I/home/test/local/netcdf/include -Wall -W -Wpointer-arith -Wcast-align -Wredundant-decls -DDEBUG -g -ggdb -O3 -fopenmp -g -Wall -W -Wpointer-arith -Wcast-align -Wredundant-decls -DDEBUG -MT SgMatrix.lo -MD -MP -MF .deps/SgMatrix.Tpo -c SgMatrix.cpp -o SgMatrix.o >/dev/null 2>&1
```
**解决方法**：
未找到解决方法，怀疑是程序bug。

5. 使用Qt4编译nuSolve 0.7.1只有nuSolve程序可以正常使用，其他程序的图形界面无法打开。
如运行vgosDbCalc，图形界面打不开，但是其命令可以使用。
```
$ ./vgosDbCalc
QWidget: Must construct a QApplication before a QPaintDevice
Aborted (core dumped)

$ ./vgosDbCalc -v
This is:
vgosDbCalc-0.4.1 (Lake Marian) released on 19 May, 2020
SgLib-0.7.1 (Linganore Creek) released on 19 May, 2020

```

**解决方法**：
未找到解决方法，怀疑是程序bug。


### 使用conda配置编译环境并编译软件

编译软件可能会遇到缺乏必要的编译工具或依赖库情况，通常只需要使用apt等工具安装即可，不过此类工具都需要管理员权限，对于普通用户这一点是行不通的。虽然许多软件可以使用源码安装，但是需要的软件比较多时都进行编译安装也是非常耗时且麻烦的时间。

conda作为一个著名的软件包与环境管理工具，许多依赖库或编译工具都可以使用它来安装，同时还有创建编译专用环境，避免对系统环境造成影响。conda安装也十分方便，在[Miniconda](https://docs.conda.io/en/latest/miniconda.html)网站下载Miniconda3 Linux 64-bit安装脚本Miniconda3-latest-Linux-x86_64.sh，并添加脚本执行权限后运行，安装程序引导安装即可。

```
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh
```

#### 创建虚拟环境，并在虚拟环境中安装需要的依赖库或编译工具

```bash
# 创建名为build的虚拟环境
conda create -n build
# 进入虚拟环境
conda activate build
# 系统中已有g++、gcc、make可以，还需安装gfortran
conda install gfortran_linux-64
cd ~/miniconda3/envs/build/bin/
# 为x86_64-conda-linux-gnu-gfortran.bin设置名为gfortran的软连接
ln -s x86_64-conda-linux-gnu-gfortran.bin gfortran
```

安装qt 5.12.9和netcdf，nusolve-0.7.3可以使用qt 5.9.7，nusolve-0.7.4需要使用Qt 5.12以上版本

```bash
conda install -c conda-forge qt=5.12.9 libnetcdf
```


#### 编译安装hops

vgosDbMake依赖于hops的运行库，如需要编译vgosDbMake应先安装hops。

hops需要pgplot和fftw3相关库，这两个库都可以通过conda安装，但是pgplot库的文件组织好像有些问题，configure不能检测到需要手动调整一下文件组织。

```bash
# 安装fftw3
conda install -c eumetsat fftw3

# 下载pgplot的安装文件包，并把其中各级目录的文件都放在同一个路径下面
wget https://anaconda.org/conda-forge/pgplot/5.2.2/download/linux-64/pgplot-5.2.2-h68245ad_1008.tar.bz2
mkdir ./pgplot
tar -xjf ~/.local/miniconda3/pkgs/pgplot-5.2.2-h68245ad_1008.tar.bz2 pgplot
cp pgplot/bin/* pgplot
cp pgplot/lib/* pgplot
cp pgplot/include/pgplot/* pgplot
cp pgplot/share/pgplot* pgplot
```

下载hops，并编译安装

```shell
tar -xzf hops.tgz
# 创建编译目录
mkdir hops_build
cd hops_build

# fftw3配置文件路径
# 生成makefile，LDFLAGS指定需要的动态库的位置，PKG_CONFIG_PATH指定fftw3配置文件路径，PGPLOT_DIR给出pgplot库及其相关文件的位置
../hops-3.23/configure  LDFLAGS="-L/home/a2/.local/miniconda3/envs/build/lib -Wl,-R/home/a2/.local/miniconda3/envs/build/lib -L/usr/lib/x86_64-linux-gnu/ -Wl,-R/usr/lib/x86_64-linux-gnu/" PGPLOT_DIR=/home/a2/Downloads/build/tar/hops_build/pgplot/ PKG_CONFIG_PATH=/home/a2/.local/miniconda3/envs/build/lib/pkgconfig --enable-mark5 --enable-difx  --prefix=/usr
make -j12
make install 
```

#### 编译安装nusolve

其中vgosDbCalc用的了calc11中的一些库，其中如DE421_little_Endian,blokq.c11.dat, tilt.dat 和 ut1ls.dat等先验文件是硬编码在程序中的，这些文件在计算中可能会用的。源码文件data目录中有这些先验文件。
编译时需要使用`--with-calc-datadir=`参数设置这些先验文件的存储路径，configure运行时会在src/vgosDbCalc/calc11/param11.i中相应的位置替换路径。

```fortran
!     Include file param11.i
!
!     ******************************************************************
!     *      CALC 11 Version                                           *
!     ******************************************************************
!
!     JPL_DE421 is the path name for the JPL ephemeris file.
!
      Integer*4   N_RECL_JPL
      PARAMETER ( N_RECL_JPL =    4 )
      Integer*4   K_SIZE_JPL
      PARAMETER ( K_SIZE_JPL = 2036 )
      Integer*4   I_RECL_JPL
! For Little Endians
      CHARACTER  JPL_DE421*80
      PARAMETER (JPL_DE421 = '/data/calc/apri/DE421_little_Endian ') ! Local customization
!     PARAMETER (JPL_DE421 = 'DE421_little_Endian             ') ! Local customization
! For Big Endians
!     CHARACTER  JPL_DE421*80
!     PARAMETER (JPL_DE421 = '/data/calc/apri/DE421_big_Endian    ') ! Local customization
!     PARAMETER (JPL_DE421 = 'DE421_big_Endian                ') ! Local customization
!  Sorry, no Medium Endians
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
      CHARACTER  A_TILTS*80
      PARAMETER (A_TILTS   = '/data/calc/apri/tilt.dat            ') ! Local customization
!
      CHARACTER  OC_file*80
      PARAMETER (OC_file   = '/data/calc/apri/blokq.c11.dat       ') ! Local customization
!
      CHARACTER  OPTL_file*80
      PARAMETER (OPTL_file = '/data/calc/apri/blokq.c11.dat       ') ! Local customization
!
!  Leap seconds file (Not needed by difx correlator)
      CHARACTER  DFLEAP*80
      PARAMETER (DFLEAP    = '/data/calc/apri/ut1ls.dat           ') ! Local customization
!     PARAMETER (DFLEAP    = 'ut1ls.dat                       ') ! Local customization
!
```

编译需要的依赖环境已经配置完成，开始nusolve的编译

`$ORIGIN`是一个指示实际的可执行文件名的特殊变量，其被解析为可执行文件在运行时的位置。

```bash
./configure --prefix=/usr --with-calc-datadir=/data/calc/apri LDFLAGS="-L/home/a2/.local/miniconda3/envs/ns/lib/ -Wl,-R'\$\$ORIGIN/../lib' -Wl,-R/home/a2/.local/miniconda3/envs/ns/lib/ -Wl,-as-needed"  --with-netcdf-include=/home/a2/.local/miniconda3//envs/ns/include --with-netcdf-lib=/home/a2/.local/miniconda3/envs/ns/lib F77=gfortran --with-hops-dir=/home/a2/Downloads/ns/hops_bin/usr/
make -j24
make install
```

##### 一些问题的解决

1. 编译前环境检查找不到libQt5Core

```
checking for moc-qt5... moc-qt5
checking for sync in -lQt5Core... no
configure: error: Cannot find libQt5Core. Ask your sysadmin to install the library.
```
增加LDFLAGS指定qt5库的位置

```bash
export LDFLAGS="-L/home/a2/miniconda3/envs/build/lib/"
```

或者在运行configure是添加LDFLAGS参数

```bash
./configure --prefix=/home/solve/opt/nusolve --with-calc-datadir=./ LDFLAGS="-L/home/solve/miniconda3/lib/"   --with-netcdf-include=/home/solve/miniconda3/include --with-netcdf-lib=/home/solve/miniconda3/lib
```
2. 编译环境检查时找不到libQt5Gui

```
checking for sync in -lQt5Gui... no
configure: error: Cannot find libQt5Gui. Ask your sysadmin to install the library.
```
提示libQt5Gui没有找到，但是在指定的动态库目录中有该文件，查看config.log，发现

```
configure:14407: /home/a2/.local/miniconda3/envs/ns/bin/x86_64-conda-linux-gnu-cc -o conftest -march=nocona -mtune=haswell -ftree-vectorize -fPIC -fstack-protector-strong -fno-plt -O2 -ffunction-sections -pipe -isystem /home/a2/.local/miniconda3/envs/ns/include -DNDEBUG -D_FORTIFY_SOURCE=2 -O2 -isystem /home/a2/.local/miniconda3/envs/ns/include -L/home/a2/.local/miniconda3/envs/ns/lib/ -Wl,-R/home/a2/.local/miniconda3/envs/ns/lib/ conftest.c -lQt5Gui  -lm -lc  >&5
/home/a2/.local/miniconda3/envs/ns/bin/../lib/gcc/x86_64-conda-linux-gnu/11.2.0/../../../../x86_64-conda-linux-gnu/bin/ld: warning: libGL.so.1, needed by /home/a2/.local/miniconda3/envs/ns/lib//libQt5Gui.so, not found (try using -rpath or -rpath-link)
```

查找了一些资料，在一个[关于Undefined reference to `clock_gettime` although `-lrt` is given的讨论](https://stackoverflow.com/questions/17150075/undefined-reference-to-clock-gettime-although-lrt-is-given)中发现在LDFLAGS中增编译参数`-Wl,--as-needed`可以解决 


```bash
LDFLAGS="-L/home/a2/.local/miniconda3/envs/ns/lib/ -Wl,-R/home/a2/.local/miniconda3/envs/ns/lib/ -Wl,-as-needed"
```

3. 编译环境检查时找不到FORTRAN编译器

```
configure: error: Cannot find usable FORTRAN compiler
```

使用conda安装的gfortran编译器为x86_64-conda-linux-gnu-gfortran，虽然将其链接到gfortran，但是程序依然configure依然将其识别为了x86_64-conda-linux-gnu-gfortran，即`F77=x86_64-conda-linux-gnu-gfortran`。而configure脚本中会检测F77的值是否为gofrtran或f77，为避免这一错误的出现增加编译参数`F77=gfortran`。

```bash
if test "x$F77" = xgfortran; then
    { $as_echo "$as_me:${as_lineno-$LINENO}: result: FORTRAN compiler: gfortran" >&5
$as_echo "FORTRAN compiler: gfortran" >&6; }
elif test "x$F77" = xf77; then
    { $as_echo "$as_me:${as_lineno-$LINENO}: result: FORTRAN compiler: f77" >&5
$as_echo "FORTRAN compiler: f77" >&6; }
else
    as_fn_error $? "Cannot find usable FORTRAN compiler" "$LINENO" 5
fi
```

```bash
../nusolve-0.7.4/configure --prefix=/usr --with-calc-datadir=../nusolve-0.7.4 LDFLAGS="-L/home/a2/.local/miniconda3/envs/ns/lib/ -Wl,-R/home/a2/.local/miniconda3/envs/ns/lib/ -Wl,-as-needed"  --with-netcdf-include=/home/a2/.local/miniconda3//envs/ns/include --with-netcdf-lib=/home/a2/.local/miniconda3/envs/ns/lib F77=gfortran --with-hops-dir=/home/a2/Downloads/ns/hops_bin/usr/
```

4. 编译错误'Format_RGBA64' is not a member of 'QImage'

```
SgGuiPlotter.cpp: In member function 'void SgPlot::save2Image()':
SgGuiPlotter.cpp:4242:89: error: 'Format_RGBA64' is not a member of 'QImage'
 4242 |     QImage                      image(2*QSize(area_->width(), area_->height()), QImage::Format_RGBA64);
      |                                                                                         ^~~~~~~~~~~~~
make[2]: *** [Makefile:875：SgGuiPlotter.lo] 错误 1
```

查询[Qt的文档](https://doc.qt.io/qt-5/qimage.html#Format-enum)发现`Format_RGBA64`是qt5.12新增成员函数，需要使用qt5.12编译。

|Constant|Value|Description|
|-|-|-|
|mage::Format_RGBA64|26|The image is stored using a 64-bit halfword-ordered RGBA format (16-16-16-16). (added in Qt 5.12)|


5. 运行程序时找不到动态库，需要在`LD_LIBRARY_PATH`环境变量中设置动态库的路径

```
./configure --prefix=/home/solve/opt/nusolve --with-calc-datadir=./ LDFLAGS="-L/home/solve/miniconda3/lib/ -Wl,-R/home/solve/miniconda3/lib/"  --with-netcdf-include=/home/solve/miniconda3/include --with-netcdf-lib=/home/solve/miniconda3/lib
```
编译时LDFLAGS中增加"-Wl,-R"参数，让连接器在运行时也能够找到需要的动态库

```
LDFLAGS="-L/home/a2/.local/miniconda3/envs/build/lib/ -Wl,-R/home/a2/.local/miniconda3/envs/build/lib/"
```

参考：[Makefile选项CFLAGS,LDFLAGS,LIBS - Taskiller - 博客园](https://www.cnblogs.com/taskiller/archive/2012/12/14/2817650.html)



## 程序打包（Appimage）

为了能够方便的在其他设备上安装运行程序，将程序整合为一个可独立运行的软件包是很必要的，目前linux系统上有snap、appimage、Flatpak等多种软件打包格式，这里选择Appimag的方式。打包后的程序可以在当前系统版本或更新版本上直接运行使用。关于Appiamge的详细信息可参见[官方文档](https://docs.appimage.org/introduction/index.html)。

### appimage制作

appimage要求的目录结构如下：

```
-AppDir
- usr
- bin # 可执行程序
- lib # 依赖库文件
- share # 其他文件，如用户手册等
```

因此在编译运行`configure`时需要增加设置参数`--prefix=/usr`，在执行`make install`安装是需要增加`DESTDIR`参数，如`make install DESTDIR=$HOME/AppDir`即将程序安装到用户目录下的AppDir文件夹内。

使用appimage格式打包程序，可以实现一次编译在大多数linux发行系统上都可以直接运行。对于nuSolve来说，要实现这一方式需要解决的问题主要有两个：1、多程序运行问题，2、vgosDbCalc硬编码先验路径问题。这两个问题都可以通过自定义脚本来实现：自定义脚本的不同参数启动不同程序；设置固定的临时文件夹作为先验文件存储目录，每次运行vgosDbCalc前创建并复制文件到该目录。另外还实现了软件安装功能，在安装是可以自定义先验文件的路径。

使用使用打包工具linuxdeploy辅助打包，该工具会自动复制程序所依赖的多数动态库，并调整动态库搜索路径到`../lib`。linuxdeploy的[下载地址](https://github.com/linuxdeploy/linuxdeploy/releases)及[使用帮助](https://docs.appimage.org/packaging-guide/from-source/linuxdeploy-user-guide.html)。下载后增加执行权限即可使用，`./linuxdeploy-x86_64.AppImage --help`查询帮助。下面是一个示例用法，

```
./linuxdeploy-x86_64.AppImage --appdir=/home/a2/Downloads/ns/nusolve_appimage/ -p qt --custom-apprun /home/a2/Downloads/for_get_env/nusolve.sh -o appimage
```

运行结束会生成一个`.AppImage`扩展名的程序文件，理论上文件可以直接在与编译系统相同或更新版本上运行。


### appimage制作




输出appimage需要完善添加启动脚本、desktop文件、图标文件。



使用ORIGIN
[makefile - Difficulty adding $ORIGIN to LDFLAGS - Stack Overflow](https://stackoverflow.com/questions/62034115/difficulty-adding-origin-to-ldflags)

[Creating relocatable Linux executables by setting RPATH with $ORIGIN | by Luke Chen | Medium](https://nehckl0.medium.com/creating-relocatable-linux-executables-by-setting-rpath-with-origin-45de573a2e98)

```
configure --prefix=/usr --with-calc-datadir=/data/calc/apri LDFLAGS="-L/home/a2/.local/miniconda3/envs/ns/lib/ -Wl,-R'\$\$ORIGIN../lib' -Wl,-R/home/a2/.local/miniconda3/envs/ns/lib/ -Wl,-as-needed"  --with-netcdf-include=/home/a2/.local/miniconda3//envs/ns/include --with-netcdf-lib=/home/a2/.local/miniconda3/envs/ns/lib F77=gfortran --with-hops-dir=/home/a2/Downloads/ns/hops_bin/usr/
```

使用$ORIGIN/../lib能避免多次对同一个目录使用linux_deploy后nuSolve打开"Edit"-"Edit general config"程序会卡死的问题，这可能是由某些库的错误引用造成的。

[Packaging native binaries — AppImage documentation](https://docs.appimage.org/packaging-guide/from-source/native-binaries.html#packaging-from-source)
[Releases · linuxdeploy/linuxdeploy](https://github.com/linuxdeploy/linuxdeploy/releases/)
[linuxdeploy/linuxdeploy-plugin-qt: Qt plugin for linuxdeploy, bundling Qt resources, plugins, QML files and a lot more.](https://github.com/linuxdeploy/linuxdeploy-plugin-qt)