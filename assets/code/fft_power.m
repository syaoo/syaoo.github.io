%%% 功率谱能量谱
clf
clear
if isempty(strfind(version,'R'))
  1
  pkg('load', 'signal') % 在Octave中需要先载入signal模块才能使用boxcar
end
randn('seed',1)
S = @(t) 3*sin(2*pi*15*t-pi/5) ...
    + 7*cos(2*pi*100*t-pi/4)+randn(size(t)); % 信号函数
fs = 300;  % 采样频率
n = 600;   % 采样点数
t = (0:n-1)/fs;    % 样本数据的时间范围
x = S(t);         % 样本数据
nfft=2048;
df = fs/nfft;     % 频率增量
x_fft = fft(x,nfft);
fx = (0:nfft-1)*df;

figure(1)
% 绘制信号及FFT结果
subplot(421)
plot(t,x,'linewidth',0.5)
title('data')
xlabel('time/s');
ylabel('Amplitude');
set(gca,'fontsize',6)
grid
subplot(422);
plot(fx,abs(fftshift(x_fft))/n);
title('Amplitude')
xlabel('Frequency/HZ');
ylabel('Amplitude|y/(2*n)|');
set(gca,'fontsize',6)
grid

%#########################
% 使用周期图函数计算功率谱
subplot(423)
window = boxcar(length(x));  %矩形窗
% 双边
periodogram(x,window,nfft,fs,'twosided'); % 'onesided' | 'twosided' 
set(gca,'fontsize',6)
subplot(424)
% 单边
periodogram(x,window,nfft,fs); % 默认是单边谱
set(gca,'fontsize',6)
xlim([0,max(fx/2)])

%#########################
% 使用fft结果计算
% 为了与periodogram函数的输出结果相同，使用w/hz,
% 取10倍的对数后即为dB/Hz
psd_fft = abs(x_fft).^2/(n*fs); % 以w/Hz表示
% psd_fft = abs(x_fft).^2/(n); % 以w表示
% abs(x_fft).^2 == x_fft.*conj(x_fft)

subplot(425)
plot(fx,10*log10(psd_fft))
title('Two-sided PSD(FFT)')
xlabel('Frequency/[HZ]');
ylabel('Power density/[dB/Hz]');
set(gca,'fontsize',6)
grid
subplot(426)
psd_fft_one = psd_fft(1:nfft/2+1);
% 为了保持总功率不变，将同时在两组（正频率和负频率）中出现的所有频率乘以因子 2。
psd_fft_one(2:end-1) = 2*psd_fft_one(2:end-1);
plot(fx(1:nfft/2+1),10*log10(psd_fft_one));
title('One-sided PSD(FFT)')
xlabel('Frequency/[HZ]');
ylabel('Power density/[dB/Hz]');
xlim([0,max(fx/2)])
set(gca,'fontsize',6)
grid

%%#########################
%% 自相关法
%subplot(427)
%cx = xcorr(x,'unbiased');
%cx_fft = fft(cx,nfft);
%cx_psd = abs(cx_fft)/fs;
%plot(10*log10(cx_psd))
%title('Two-sided PSD(autocorrelation)')
%xlabel('Frequency/[HZ]');
%ylabel('Power density/[dB/Hz]');
%set(gca,'fontsize',6)
%grid
%subplot(428)
%cx_psd_one = cx_psd(1:nfft/2+1);
%cx_psd_one(2:end-1) = 2*cx_psd_one(2:end-1);
%plot(fx(1:nfft/2+1),10*log10(cx_psd_one))
%title('One-sided PSD(autocorrelation)')
%xlabel('Frequency/[HZ]');
%ylabel('Power density/[dB/Hz]');
%xlim([0,max(fx/2)])
%set(gca,'fontsize',6)
%grid

%#########################
% 自相关法
% 双边功率谱
subplot(427)
cx = xcorr(x,'unbiased');
cx_nfft = 2^nextpow2(length(cx)); % 使FFT点数为2的幂次
cx_fft = fft(cx,cx_nfft);
% FFT 点数做了改边，频率关系也需要重新调整
cx_df = fs/cx_nfft;
cx_fx = (0:cx_nfft-1)*cx_df;
cx_psd = abs(cx_fft)/fs;
plot(cx_fx,10*log10(cx_psd))
title('Two-sided PSD(autocorrelation)')
xlabel('Frequency/[HZ]');
ylabel('Power density/[dB/Hz]');
set(gca,'fontsize',6)
grid
% 单边功率谱
subplot(428)
cx_psd_one = cx_psd(1:cx_nfft/2+1);
cx_psd_one(2:end-1) = 2*cx_psd_one(2:end-1);
plot(cx_fx(1:cx_nfft/2+1),10*log10(cx_psd_one))
title('One-sided PSD(autocorrelation)')
xlabel('Frequency/[HZ]');
ylabel('Power density/[dB/Hz]');
set(gca,'fontsize',6);
xlim([0,max(cx_fx/2)]);
grid

% 计算差异
psd_cx = abs(fft(cx,nfft)/fs);
% 周期图与fft差异
fft_pd = max(psd_fft'-periodogram(x,window,nfft,fs,'twosided'))
% fft与自相关差异
fft_cx = max(psd_fft-psd_cx)
%自相关与周期图差异
cx_pd = max(psd_cx'-periodogram(x,window,nfft,fs,'twosided'))
periodogram(x,window,cx_nfft,fs,'twosided')