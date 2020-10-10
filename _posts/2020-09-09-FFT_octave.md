---
title: FFT与频谱、功率谱、能量谱等
tag: ['fft']
mathjax: true
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover1.jpg
---

计算时间序列的FFT以及其频谱（幅值谱，相位谱），功率谱、能量谱和倒频谱。一些基本理论和示例演示（含代码Octave\Matlab）
<!--more-->
FFT（Fast Fourier Transformation，离散傅里叶变换）是目前普遍使用的一种DFT的一种快速算法，其可将计算量从$n^2$降低到$n\log(n)$。当数据量很大时，使FFT的点数$n$为2的幂时，可明显提示计算效率。在Octave/Matlab中内置有相关函数可以方便的对数据做快速傅里叶变换处理；Python的Scipy、Numpy包中也提供有FFT计算相关的模块，二者都是包括了一个基于Fortran FFTPACK的`fft`函数，Scipy对Numpy提供的FFT功能做了扩展；PyFFW库也可以提供更快的FFT计算。本文以Octave程序为了，来探讨使用FFT来计算数据的频谱，功率谱等信息，在Python、Matlab中方法也类似。

在Matlab官方文档中给出了如下表格，对采样数据及FFT计算结果做了说明：

| 数量                 | 说明                                 |
| :------------------- | :----------------------------------- |
| `x`                  | 采样的数据                           |
| `n = length(x)`      | 样本数量                             |
| `fs`                 | 采样频率（每单位时间或空间的样本数） |
| `dt = 1/fs`          | 每样本的时间或空间增量               |
| `t = (0:n-1)/fs`     | 数据的时间或空间范围                 |
| `y = fft(x)`         | 数据的离散傅里叶变换 (DFT)           |
| `abs(y)`             | DFT 的振幅                           |
| `(abs(y).^2)/n`      | DFT 的功率                           |
| `fs/n`               | 频率增量，频率分辨率                 |
| `f = (0:n-1)*(fs/n)` | 频率范围                             |
| `fs/2`               | Nyquist 频率（频率范围的中点）       |

FFT计算的结果是长度与FFT点数相同复数序列，分别表示$0\mathrm{Hz},\frac{fs}{n}\times1\mathrm{Hz},\frac{fs}{n}\times2\mathrm{Hz},...\frac{fs}{n}\times n\mathrm{Hz}$各频率分量的信息，模表示各频率分量的幅度特征；复数的相位角（$\theta,z = abs(z)e^{i\theta}$）表示各频率分量的相位（在Octave中可以使用`angle()`函数计算）；为避免发生混叠，使采样结果能准确恢复原信号，采用频率$f_s$必须大于最高频率$f_c$的两倍。即$f_s>2*f_c$；`fft`函数可以传入参数$N$用于指定FFT变化点数，如`fft(x,1024)`表示做点数为1024的FFT变换。

## 离散傅里叶变换(DFT)与快速傅里叶变换(FFT)

离散傅里叶变换的过程一般分为采样、截断和延拓三步。信号经过采样后得到$N$点的序列，$N=\dfrac{T}{T_s}$，其中$T$为采样时间，$T_s$为采样时间间隔。该采样序列的离散傅里叶变换：
$$
X(k)\rightleftharpoons x(n)
$$
第$k$个频域分量为
$$
X(k)=\sum_{n=0}^{N-1}x(n)e^{-j2\pi kn/N} \qquad (k=0,1,...,N) \qquad\qquad(1)
$$
第$n$个时域分量为
$$
x(n)=\frac{1}{N}\sum_{k=0}^{N-1}X(k)e^{j2\pi kn/N}  \qquad (n=0,1,...,N) \qquad\qquad(2)
$$
频域分量$X(k)$的模$|X(k)|$表示各分量的幅值，但是注意到计算过程中，每个频域分量都是所有$N$个时域数据点的累加，所以频域分量的真实幅值为$\frac{1}{N}|X(k)|$。 

由上面公式可是看到，计算所有频域分量的离散傅里叶变换，需要$N^2$次计算，随着$N$的增加计算量会急剧增大，而快速傅里叶变换（FFT）则可以将计算量降低到$N\log(N)$，大大减少的计算次数。

## FFT使用

假设信号：$S(t)=3\sin(2\pi15t-\frac{\pi}{5})+\cos(2\pi100t-\frac{\pi}{4})$，取采样频率$f_s=300\mathrm{Hz}$，采样点数$n=600$：

```matlab
S = @(t) 3*sin(2*pi*15*t-pi/5) ...
    + 7*cos(2*pi*100*t-pi/4); % 信号函数
fs = 300;  % 采样频率
n = 600;   % 采样点数
t = (0:n-1)/fs;    % 样本数据的时间范围
x = S(t);         % 样本数据
df = fs/n;     % 频率增量
x_fft = fft(x);
```

这里`x_fft`是大小与`x`相同的复数序列，`x_fft(1)`与`x_fft(n/2+1)`分别表内直流分量（DC,$0\mathrm{Hz}$）和奈奎斯特频率分量（Nyquist 频率，$f_s/2\mathrm{Hz}$）,该序列关于奈奎斯特频率对称。

```matlab
% 原始数据图像
plot(t,x,'linewidth',0.5)
title('data')
xlabel('time/s');
ylabel('Amplitude');
%% 幅值谱
fx = (0:n-1)*df; 
plot(fx,abs(x_fft));
title('Amplitude')
xlabel('Frequency/HZ');
ylabel('Amplitude|y|');
```

下面两幅图，分别为信号采样图像和FFT计算结果的模。由前面的论述知道，FFT结果的模只能反映各频率分量的相对大小，右侧的双边幅值谱也证实了这一结果。可以看到，FFT结果中有四个峰值，在$[0,f_s/2]$区间存在两个峰，在$[f_s/2,f_s]$区间存在两峰，它们关于奈奎斯特频率（$f_s/2$）对称。

![wQHIED.png](https://s1.ax1x.com/2020/09/08/wQHIED.png)

### 频谱
频谱反应的是信号的幅度和相位随频率的/分布情况，它描述了信号的频域特征。

#### 幅度谱

幅度谱反映了信号的幅值随频率分布分情况。
```matlab
% 校正幅度
x_fft_cor = x_fft/(n);
plot(fx,abs(x_fft_cor));
title('Corrected Amplitude')
xlabel('Frequency/HZ');
ylabel('Amplitude|y/n|');

x_fftshift = fftshift(x_fft);
fx0 = fx-fs/2; % 将频率范围调整到以0为中心
plot(fx0,abs(x_fftshift/(n)));
title('After FFTshit')
xlabel('Frequency/HZ');
ylabel('Amplitude|y/n|');
```

把前面得到的幅值 *除*  **采样点数**修正幅值并绘制双边幅度谱图像，可以看到对应频点的幅值并不是真实幅值，可以理解为FFT把信号分解为幅值相同正负频率分量（$e^{i\theta}=\cos\theta+i\sin\theta$），$[0,f_s/2]$和$[f_s/2,f_s]$分别对应$$[0,f_s/2]$$和$[-f_s/2,0]$，同`fftshift`可以将零频分量移动到频谱中心得到左图，所以真实的幅值还应再乘2。

![wQHhDK.png](https://s1.ax1x.com/2020/09/08/wQHhDK.png)

还应注意，**由于零频（直流分量）和奈奎斯特频率不会出现两次，所有只需对除零频和奈奎斯特频率以外的频率分量乘2即可**，对于实数值信号，只需要对正负频率之一进行估计，即绘制**单边频谱**$[0,f_s/2]$即可，当FFT点数为偶数时截取长度为$(nfft/2+1)$，为奇数时截取长度为$((nfft+1)/2)$。

```matlab
% 截取fft[0,fs/2]
x_side_fft = x_fft(1:n/2+1);
x_side_fft = abs(x_side_fft/n);
x_side_fft(2:end-1) = x_side_fft(2:end-1)*2; % 除了0和Nyquist频率外乘2； 
fx_side = fx(1:n/2+1);
plot(fx_side,x_side_fft);
title('From FFT')
xlabel('Frequency/HZ');
ylabel('Amplitude|y/(2*n)|');
xlim([0,fs/2]);

% 截取fftshit [0,fs/2]
x_side_fftshift = x_fftshift(n/2+1:end);
x_side_fftshift = abs(x_side_fftshift/n);
x_side_fftshift(2:end-1) = x_side_fftshift(2:end-1)*2; % 除了0和Nyquist频率外乘2；
plot(fx_side,x_side_fft);
title('From FFTshift')
xlabel('Frequency/HZ');
ylabel('Amplitude|y/(2*n)|'); 
xlim([0,fs/2]);
```

下图右侧是截取FFT结果的$[0,f_s/2]$一侧的结果，右侧图像是截取的FFTshit结果的$[0,f_s/2]$，二者结果是等价的。在做乘2处理后，所得幅值与实际幅值时相同的。

![wQHfu6.png](https://s1.ax1x.com/2020/09/08/wQHfu6.png)

所以，为了得到各频率分量的真实幅值需要**"按输入信号的长度（采样点数）缩放 DFT，并将 0 和 Nyquist 之外的所有频率乘以 2"**。

还应注意的时，在估计频率分量的幅值时，如果DFT的频率分辨率$fs/nfft$（$nfft$为fft点数）不能被频率分量整除时，则可能导致估计不准确，而通过补零来改变DFT的频率分辨率使其与信号频率匹配，如含有文中信号$15\mathrm{HZ}$和$100\mathrm{HZ}$频率分量的信号，当采样点$nfft=n=400$时，$f_s/nfft=3/4$，此时$100\mathrm{HZ}$的幅值不能准确估计（如下图），将$nftt$改为800后$1000/2000=0.5$，此时两分量的幅值都能被更准确估计。另外示例中信号是没有噪声的，在有噪声的情况下估计的幅值通常与真实幅值也会存在一定的差异，一般较长的信号会产生更好的频率近似值。

![wQH4HO.png](https://s1.ax1x.com/2020/09/08/wQH4HO.png)

#### 相位谱
相位谱反映了信号的相位随频率分布分情况。
在Octave中使用`angle`可以方便的计算复数的相位角，FFT结果中存在许多很小的幅值会影响相位谱的解决，计算前需要先剔除。

```matlab
tol = 1e-6;
z=fftshift(x_fft);
z(abs(z) < tol) = 0;
theta = angle(z);
stem(fx0,theta/pi,'Markersize',1);
title('Phase')
xlabel 'Frequency (Hz)'
ylabel 'Phase / \pi'
```
下图是绘制的相位谱，图中在$15\mathrm{HZ}$和$100\mathrm{HZ}$处分别有$-0.7\pi$和$-0.25\pi$的相位值，这里的相位用余弦表示的。

![wQHRjx.png](https://s1.ax1x.com/2020/09/08/wQHRjx.png)

完整Octave代码[fft_ap.m](/assets/code/fft_ap.m)

### 功率谱

**功率谱**也称功率谱密度（PSD），描述了一个信号或时间序列的功率随频率的分布。功率谱有两种求法：

1. (信号傅立叶变换的模的平方)/(采样点数) 或 (信号傅立叶变换的模的平方)/(采样点数\*采样频率) ；
2. 信号自相关函数的傅里叶变换 。

功率谱的单位是$\mathrm{W/Hz}$，单位是$$\mathrm{dB/Hz}$$时是做了对数处理（$10\lg(X)$）对于以$\mathrm{dB}$为单位$\mathrm{dB} = \mathrm{dB}/\mathrm{Hz}*\mathrm{Bandwidth(Hz)}$。取对数的目的是使那些振幅较低的成分相对高振幅成分得以拉高，以便观察掩盖在低幅噪声中的周期信号。

功率谱和能量谱用于描述信号的频域特性。能量谱常用于描述能量信号，而功率谱则用于描述功率信号；一般来说，周期信号和随机信号是功率信号，而非周期的确定信号是能量信号。**能量谱**也叫能量谱密度，能量谱密度描述了信号或时间序列的能量如何随频率分布；能量谱是原信号傅立叶变换的平方。

Octave/Matlab中有`periodogram`函数可以方便的绘出信号的功率密度谱，周期图（periodogram）是广义平稳随机过程功率谱密度的非参数估计，是自相关序列有偏估计的傅里叶变换。对于信号$x_n$采样率为$f_s$，周期图的定义为：
$$
\hat{P}(f)=\frac{\Delta t}{N}\left| \sum_{n=0}^{N-1} x_ne^{-j2\pi f \Delta tn}\right|^2，-1/2\Delta t<f\le1/2\Delta t,
$$
其中，$\Delta t$是采样间隔（$1/f_s$）。对于单边周期图，除了0和Nyquist（$1/\Delta t$）频率外所有的频率都需要乘2，以保持总功率不变。

如果频率使用radians/sample表示，周期图定义可以表示为：
$$
\hat{P}(\omega)=\frac{1}{2\pi N}\left| \sum_{n=0}^{N-1} x_ne^{-j\omega n}\right|^2，-\pi<\omega\le\pi,
$$

下面分别使用周期图函数`periodogram`直接绘制功率谱，快速傅里叶变换的模的平方/采样点数（`fft`）以及自相关函数的傅里叶变换（`xcorr`）的方法来绘制功率谱。

构造一个含有噪声的信号，并绘制出其图像及样本序列的幅度谱：

```matlab
S = @(t) 3*sin(2*pi*15*t-pi/5) ...
    + 7*cos(2*pi*100*t-pi/4)+randn(size(t)); % 信号函数
fs = 300;  % 采样频率
n = 600;   % 采样点数
t = (0:n-1)/fs;    % 样本数据的时间范围
x = S(t);         % 样本数据
nfft=2048
df = fs/nfft;     % 频率增量
x_fft = fft(x,nfft);
fx = (0:nfft-1)*df;

% 绘制信号及FFT结果
plot(t,x,'linewidth',0.5)

plot(fx,abs(fftshift(x_fft))/n);
```

![w3wE8J.png](https://s1.ax1x.com/2020/09/09/w3wE8J.png)

周期图函数在没有指定返回参数时会在绘制功率密度谱，纵轴单位是：$\mathrm{dB/Hz}$。`'onesided' `、 `'twosided'`、`'centered'`分别单边、双边频谱以及以0频为中心频率的双边频率。

```matlab
window = boxcar(length(x));  %矩形窗
% 双边
periodogram(x,window,nfft,fs,'twosided'); % 'onesided' | 'twosided' 
% 单边
periodogram(x,window,nfft,fs); % 默认是单边谱
```

![w3wnDx.png](https://s1.ax1x.com/2020/09/09/w3wnDx.png)

使用FFT计算结果绘制功率谱，前面提到，这种计算方式是$FFT结果的模的平方/采样点数$，为了方便与周期图函数结果对比，纵轴也转换为以$\mathrm{dB/Hz}$为单位，所以这里功率谱的计算方式应为$FFT结果的模的平方/(采样点数*采样频率)$，并把功率谱结果`X`作对数处理`10*log10(X)`，下图左右分别为双边功率谱和单边功率谱。与频谱处理方式类似，这里为了保持总功率不变，将同时在两组（正频率和负频率）中出现的所有频率乘以因子 2。因为图中结果是取了对数的，单、双边功率谱的峰值不能直接看出2倍的关系。
```matlab
% 使用fft结果计算
% 为了与periodogram函数的输出结果相同，使用w/hz,
% 取10倍的对数后即为dB/Hz
psd_fft = abs(x_fft).^2/(n*fs); % 以w/Hz表示
% psd_fft = abs(x_fft).^2/(n); % 以w表示
% abs(x_fft).^2 == x_fft.*conj(x_fft)
plot(fx,10*log10(psd_fft))

psd_fft_one = psd_fft(1:nfft/2+1);
% 为了保持总功率不变，将同时在两组（正频率和负频率）中出现的所有频率乘以因子 2。
psd_fft_one(2:end-1) = 2*psd_fft_one(2:end-1);
plot(fx(1:nfft/2+1),10*log10(psd_fft_one));
```
![w3wF5F.jpg](https://s1.ax1x.com/2020/09/09/w3wF5F.jpg)

根据维纳-辛钦定理（Wiener–Khinchin theorem）平稳随机过程的功率谱密度与其自相关函数互为傅里叶变换。对样本序列做自相关计算，并做傅里叶变换，求其模即可得到功率谱。这里为了与前面周期图对应，结果除以采样频率，并取对数。

```matlab
% 自相关法
% 双边功率谱
cx = xcorr(x,'unbiased');
cx_nfft = 2^nextpow2(length(cx)); % 使FFT点数为2的幂次
cx_fft = fft(cx,cx_nfft);
% FFT 点数做了改边，频率关系也需要重新调整
cx_df = fs/cx_nfft
cx_fx = (0:cx_nfft-1)*cx_df;
cx_psd = abs(cx_fft)/fs;
plot(cx_fx,10*log10(cx_psd))

% 单边功率谱
cx_psd_one = cx_psd(1:cx_nfft/2+1);
cx_psd_one(2:end-1) = 2*cx_psd_one(2:end-1);
plot(cx_fx(1:cx_nfft/2+1),10*log10(cx_psd_one))
```
![w3KGge.png](https://s1.ax1x.com/2020/09/09/w3KGge.png)

对比前三种方式绘制的功率谱，峰值看不出明显差异，FFT计算的结果与周期图结果差值小于1e-19，而二者与自相关计算结果差异都比较大，在0.1~0.01量级以内。不过，可以看出自相关计算得到的功率谱结果更为平滑一些。

完成Octave代码[fft_power.m](/assets/code/fft_power.m)

## 倒频谱

倒频谱（Cepstrum）也叫倒谱、二次谱和对数功率谱等。倒频谱的工程型定义是：信号功率谱对数值进行傅立叶逆变换的结果。（信号→求功率谱→求对数→求傅里叶逆变换）。该分析方法方便提取、分析原频谱图上肉眼难以识别的周期性信号，能将原来频谱图上成族的边频带谱线简化为单根谱线，受传感器的测点位置及传输途径的影响小。



---



[频谱分析练习题](http://ccftp.scu.edu.cn/Download/20180419110519896.pdf)

**参考**

1. [信号频域分析方法的理解（频谱、能量谱、功率谱、倒频谱、小波分析） - 知乎](https://zhuanlan.zhihu.com/p/34989414)
2. [能量信号、功率信号、频谱、能量谱、功率谱、及一些定理 - htj10 - 博客园](https://www.cnblogs.com/htj10/p/8638275.html)
3. [快速傅里叶变换 - MATLAB fft - MathWorks 中国](https://ww2.mathworks.cn/help/matlab/ref/fft.html)
4. [傅里叶变换 - MATLAB & Simulink - MathWorks 中国](https://ww2.mathworks.cn/help/matlab/math/fourier-transforms.html) 
5. [基本频谱分析 - MATLAB & Simulink - MathWorks 中国](https://ww2.mathworks.cn/help/matlab/math/basic-spectral-analysis.html)
6. [幅值估计和填零 - MATLAB & Simulink - MathWorks 中国](https://ww2.mathworks.cn/help/signal/ug/amplitude-estimation-and-zero-padding.html)
7. [使用 FFT 获得功率频谱密度估计 - MATLAB & Simulink - MathWorks 中国](https://ww2.mathworks.cn/help/signal/ug/power-spectral-density-estimates-using-fft.html?s_tid=srchtitle)
8. [信号分析与处理技术基础](/assets/doc/信号分析与处理技术基础(FT).pdf)
9. [频谱中幅值的意义 - dxmake](https://dxmake.com/post/amplitude-of-spectrum/)
10. [关于实信号的双边谱和单边谱_从前有个花果山-CSDN博客](https://blog.csdn.net/terrencestark/article/details/78030192)
11. [（一）功率谱密度（PSD Power Spectral density）学习笔记 - 知乎](https://zhuanlan.zhihu.com/p/50272016)
12. [Periodogram power spectral density estimate - MATLAB periodogram - MathWorks 中国](https://ww2.mathworks.cn/help/signal/ref/periodogram.html#btt8at0-1)
