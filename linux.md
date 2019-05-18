### 后台挂起任务

```bash
nohup [command] [file] > /dev/null 2>&1&
```

### 硬盘擦除

注意事项：

切记对硬盘操作之前要先umount！！

硬盘可以通过lsblk命令查看！下面以/dev/sda为例

看清楚再执行命令！

如果是对外接ssd进行操作，一定要注意散热问题！

#### gparted

gparted是带GUI版本的parted，如果只是需要快速格式化，用gparted就可以了

#### Shred 命令

```bash
shred -n [num] -z -v [dir]
```
Shred命令可以用来擦除数据。

-n 是写入随机数据的次数，默认为3次

-z 是填充0

-v 是显示进度

例如下方命令就是先填充两次随机数，最后填充一次0

```bash
shred -n 2 -z -v /dev/sda
```
#### dd 命令

这个命令用来烧录过镜像，但是发现也可以用来擦除数据

```bash
dd bs=[size] if=[dir] of=[dir]
```
bs(block size)就是一次读写多少数据，例如bs=64k

if(input file)就是输入的内容，例如if=/dev/zero

of(output file)就是输出的内容，例如of=/dev/sda

例如下方命令就是一次读写4MB数据，往/dev/sda（目标硬盘）填充随机数

```bash
dd bs=4M if=/dev/urandom of=/dev/sda
```

### sudo免密码

1. 打开/etc/sudoers文件（不能用其它文本编辑器去编辑）

```bash
sudo visudo
```

2. 在/etc/sudoers文件的尾部，加上下面这行

```bash
username     ALL=(ALL) NOPASSWD:ALL
```

记得将username替换成自己的用户名

### 搜狗输入法

已经在Ubuntu 19.04成功安装，针对当前版本进行了一些删改

#### 首先安装fcitx

1. 安装fcitx

检测是否有fcitx，因为搜狗拼音依赖fcitx

```bash
fcitx
```

安装fcitx

```bash
sudo apt-get install fcitx-bin
sudo apt-get install fcitx-table
```

相关的依赖库和框架都会自动安装上

2. 配置fcitx

默认iBus（非常难用），安装完fcixt后在“设置 > 区域和语言 > 管理已安装的语言 > 键盘输入法系统”处把它替换为fcitx，然后重启Ubuntu。

接着选择需要的输入法，点击Ubuntu右上角顶栏的小键盘图标，选择“配置”，把“拼音”调整到最上面，此时已经可以使用拼音输入法。

3. 安装搜狗拼音

访问(搜狗输入法For Linux)[https://pinyin.sogou.com/linux/?r=pinyin]，点击立即下载64bit，下载安装文件。

直接双击.deb文件安装，完成后重启Ubuntu。

点击Ubuntu右上角小键盘 > 配置，把搜狗拼音调到最上面，就可以使用了。

4. 卸载iBus

```bash
sudo apt-get purge ibus
sudo apt-get autoremove
```

据说Ubuntu老版本的桌面跟ibus有依赖关系，如果桌面菜单栏都消失了，那么就进命令行输入下面的提供的代码。

```bash
sudo apt-get update
sudo apt-get install --reinstall ubuntu-desktop
sudo apt-get install unity
```

#### 原文链接

https://blog.csdn.net/fx_yzjy101/article/details/80243710


### VSCode

#### VSCode在Ubuntu 19.04下无法输入中文 

不要从Ubuntu软件中心安装snap软件包，软件中心的版本存在无法调出中文输入法（例如搜狗）输入中文的bug。

解决方案：直接去(VSCode官网)[https://code.visualstudio.com/docs/setup/linux]下载“.deb package (64-bit)”。

#### VSCode空格宽度非常小

这个问题是Droid Sans Mono字体导致的。

在设置里头找到“Editor: Font Family”，把monospace放在最前面即可。