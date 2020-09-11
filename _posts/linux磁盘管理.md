---
title: linux磁盘管理
tag: ['linux']
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover0.jpg
---

abstract

<!--more-->

## 开机自动挂载

1. 查看磁盘信息（分区的UUID及格式）

   ```shell
   sudo blkid
   # /dev/sda1: UUID="985d292c-acbc-47f5-b6b5-0ee82c5ee1ad" TYPE="ext4" PARTLABEL="primary" PARTUUID="7c3ff7b8-d49d-4179-bf7c-8087ad81de68"
   #/dev/sdb1: LABEL="hdisk" UUID="9e1c6ab1-b841-4e7c-a5a8-f4e8aa9f901f" TYPE="ext4" PARTUUID="61c34aa3-99bf-1d4a-accb-6629f86091f4"
   ```

2. 配置fstab文件
   将目标磁盘分区的UUID及TYPE添加到fstab条目中

   ```shell
   sudo nano /etc/fstab
   # 在新的一行填入下面内容
   # UUID=9e1c6ab1-b841-4e7c-a5a8-f4e8aa9f901f  /hdisk ext4 0 0
   ```

   ```
   <fs spec> <fs file> <fs vfstype> <fs mntops> <fs freq> <fs passno>
   具体说明，以挂载/dev/sdb1为例：
   <fs spec>：分区定位，可以给UUID或LABEL，例如：UUID=6E9ADAC29ADA85CD或LABEL=software
   <fs file>：具体挂载点的位置，例如：/data
   <fs vfstype>：挂载磁盘类型，linux分区一般为ext4，windows分区一般为ntfs
   <fs mntops>：挂载参数，一般为defaults
   <fs freq>：磁盘检查，默认为0
   <fs passno>：磁盘检查，默认为0，不需要检查
   ```

3. 验证配置
   
运行下面命令，如果不报错即可，**如配置错误，可能会无法进入系统**。
   
   ```
   sudo mount -a
```
   
如显示：
   
   ```
   mount: /hdisk: mount point does not exist.
```
   
   则说明，指定的挂载点不存在，检查是否写错或没有创建挂载点目录。再次运行`mount -a`

---

**参考**
1. [title](url)
