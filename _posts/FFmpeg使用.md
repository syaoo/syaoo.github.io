FFmpeg使用

## 音视频截取

```css
ffmpeg -ss 00:00:00 -t 00:00:30 -i test.mp4 -vcodec copy -acodec copy output.mp4
* -ss 指定从什么时间开始
* -t 指定需要截取多长时间
* -i 指定输入文件
```

## ffmpeg合并音频和视频

提取视频

ffmpeg -i uipb.mp4 -vcodec copy -an uipb_out.mp4

合并音频、视频

ffmpeg -iuipb_out.mp4 -i ybpb.mp3 -vcodec coyp -acodec copy out.mp4

**淡入效果器的使用**

ffmpeg -i output.wav -filter_complex afade=t=in:ss=0:d=5 gradient.wav

前5s做淡入效果

 **淡出效果器的使用**

ffmpeg -i output.wav -filter_complex afade=t=out:st=20:d=5 gradient_out.wav

从20s开始，做5s的淡出效果

降低音量为原来的一半
ffmpeg -i output.wav -af volume=0.5 low_volume.wav

偏移音频
ffmpeg -i input_vid.mp4 -itsoffset 00:00:05.0 -i input_audio.wav -vcodec copy -acodec copy output.mp4