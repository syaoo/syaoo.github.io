clear
##close all
S = @(t) 3*sin(2*pi*15*t-pi/5) ...
    + 7*cos(2*pi*100*t-pi/4); % 信号函数
fs = 300;  % 采样频率
n = 602;   % 采样点数
t = (0:n-1)/fs;    % 样本数据的时间范围
x = S(t);         % 样本数据
nfft=n
df = fs/nfft;     % 频率增量

x_fft = fft(x,nfft);
% 原始数据图像
figure(1)
subplot(4,2,1)
plot(t,x,'linewidth',0.5)
title('data')
xlabel('time/s');
ylabel('Amplitude');
%% 双边频谱
%% 绘制频谱
subplot(422);
fx = (0:nfft-1)*df;
plot(fx,abs(x_fft));
title('Amplitude')
xlabel('Frequency/HZ');
ylabel('Amplitude|y|');
grid
% 校正幅度
subplot(423);
x_fft_cor = x_fft/(n);
plot(fx,abs(x_fft_cor));
title('Corrected Amplitude')
xlabel('Frequency/HZ');
ylabel('Amplitude|y/n|');
grid
% 
% 将零频分量移到频谱中心
x_fftshift = fftshift(x_fft);
fx0 = fx-fs/2; % 将频率范围调整到以0为中心
subplot(424);
plot(fx0,abs(x_fftshift/(n)));
title('After FFTshit')
xlabel('Frequency/HZ');
ylabel('Amplitude|y/n|');
grid
%% 单边频谱
% 截取fft[0,fs/2]
x_side_fft = x_fft(1:nfft/2+1);
x_side_fft = abs(x_side_fft/n);
x_side_fft(2:end-1) = x_side_fft(2:end-1)*2; % 除了0和Nyquist频率外乘2； 
fx_side = fx(1:nfft/2+1);
subplot(425)
plot(fx_side,x_side_fft);
title('From FFT')
xlabel('Frequency/HZ');
ylabel('Amplitude|y/(2*n)|');
xlim([0,fs/2]);
grid
% 截取fftshit [0,fs/2]
x_side_fftshift = x_fftshift(nfft/2+1:end);
x_side_fftshift = abs(x_side_fftshift/n);
x_side_fftshift(2:end-1) = x_side_fftshift(2:end-1)*2; % 除了0和Nyquist频率外乘2；
subplot(426)
plot(fx_side,x_side_fft);
title('From FFTshift')
xlabel('Frequency/HZ');
ylabel('Amplitude|y/(2*n)|'); 
xlim([0,fs/2]);
grid
%% 绘制相位谱
tol = 1e-6;
z=fftshift(x_fft);
##z  = x_fftshift;
z(abs(z) < tol) = 0;
theta = angle(z);
subplot(427)
stem(fx0,theta/pi,'Markersize',1);
title('Phase')
xlabel 'Frequency (Hz)'
ylabel 'Phase / \pi'
grid
