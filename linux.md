### 好用的命令

#### tldr

精简实用版的man，懒人专属

```bash
sudo apt-get install tldr
```

#### thefuck

自动纠正终端命令错误

```bash
sudo pip3 install thefuck
```

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

访问[搜狗输入法For Linux](https://pinyin.sogou.com/linux/?r=pinyin)，点击立即下载64bit，下载安装文件。

直接双击.deb文件安装，完成后重启Ubuntu。

点击Ubuntu右上角小键盘 > 配置，把搜狗拼音调到最上面，就可以使用了。

4. 卸载iBus

iBus还是要卸载的，倒不是因为两个输入法同时在右上角，而是因为搜狗输入法的“Shift键切换中英文”没法用。

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

5. 疑难杂症

Q: 搜狗输入法（fcitx）CPU占用100%，风扇狂转。在终端使用htop命令查看，具体表现为“/usr/bin/fcitx -d”占用率居高不下。

A: 是搜狗云输入的锅，在fcitx配置里把搜狗云拼音这个选项去掉就行。具体操作为“Ubuntu右上角小键盘 > 配置 > 附加组件 > （勾选）高级 > 取消勾选搜狗云拼音”

据说Google Pinyin也会有这个问题，解决方法跟这个完全相同。

#### 原文链接

[安装部分主要来自这篇](https://blog.csdn.net/fx_yzjy101/article/details/80243710)

[搜狗输入法100%CPU占用解决方法](https://blog.csdn.net/sunhaobo1996/article/details/80526140)


### VSCode

#### VSCode在Ubuntu 19.04下无法输入中文 

不要从Ubuntu软件中心安装snap软件包，软件中心的版本存在无法调出中文输入法（例如搜狗）输入中文的bug。

解决方案：直接去[VSCode官网](https://code.visualstudio.com/docs/setup/linux)下载“.deb package (64-bit)”。

#### VSCode空格宽度非常小

这个问题是Droid Sans Mono字体导致的。

在设置里头找到“Editor: Font Family”，把monospace放在最前面即可。

### Xfce

#### 安装Xfce

```bash
sudo apt install xfce4
```

安装过程中会被要求选择登录管理器（Display Manager，显示管理器），一般是从gdm3和lightdm中选择一个，我选择了lightdm。

安装完之后重启，在登录界面选择Xfce即可。

#### 疑难杂症

Q: Xfce在Ubuntu 19.04下无法打开默认应用（preferred applications），具体表现为点击桌面下方的终端、浏览器图标时弹出报错窗口，报错内容为“Failed to launch preferred application for category TerminalEmulator. Failed to execute child process /usr/lib/x86_64-linux-gnu/xfce4/exo-1/exo-helper-1 (No such file or directory).) Directory exo-1 does not exist.”

A: 是bug，可以在[Debian bugs list](http://debian.2.n7.nabble.com/Bug-892010-exo-utils-exo-preferred-applications-does-not-run-with-error-quot-exo-helper-1-not-found--td4289016.html)找到，执行下面代码即可。

```bash
sudo apt install libexo-1-0
```

Q: 字体跟图标在高分屏下太小了

A: 左上角所有应用程序 > 设置 > 设置管理器。

找到面板，其中面板1是上面的任务栏，面板2是下面的快捷图标栏。我把面板1的“行大小”调成35像素。

找到外观 > 字体 > DPI，自行调节至合适的大小，调节完后注销再登录即可见效。我把DPI改成了128。

Q: 声音无法用键盘控制

A: 右键单击上方任务栏 > 面板 > 添加新项目，找到PulseAudio插件，添加即可。

Q: 亮度无法用键盘控制

A: 终端执行下面代码

```bash
sudo apt-get install xfce4-battery-plugin
```

右键单击上方任务栏 > 面板 > 添加新项目，找到电量管理插件，添加即可。这个插件既能显示电量，还能控制亮度，所以原先的“电源监视器”插件可以换下来了。点击电池图标 > 电源管理器设置 可以开启电源管理。

Q: Ctrl + Alt + T 不打开终端

A: 左上角所有应用程序 > 设置 > 设置管理器 > 键盘 > 应用程序快捷键，点击添加。如果没看到添加按钮，最大化窗口即可。

如果想继续用GNOME终端，在命令框输入“exo-open --launch TerminalEmulator”

如果想用xfce的终端，在终端安装“xfce4-terminal”，然后在命令框输入“xfce4-terminal”

最后，按下对应要设置的快捷键（Ctrl + Alt + T）即可

### Deepin Wine

#### winecfg

需要安装wine

官方源提供的wine是4.0版本，目前最新版是4.8，因此我们进行下面操作获取新版

1. 添加wine的apt仓库

```bash
wget -nc https://dl.winehq.org/wine-builds/winehq.key && sudo apt-key add winehq.key
```

2. 添加Ubuntu 19.04的wine仓库

```bash
sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ disco main'
```

注：如果不是Ubuntu 19.04，自行将上面disco替换掉，比如Ubuntu 18.04是bionic。

3. 解决依赖libfaudio0

wine开发版需要libfaudio0，但是Ubuntu仓库里头没有，因此添加下面这个第三方PPA

```bash
sudo add-apt-repository ppa:cybermax-dexter/sdl2-backport
```

4. 安装wine 4.8

```bash
sudo apt install --install-recommends winehq-devel
```

5. （以后）卸载

```bash
sudo apt remove --auto-remove winehq-devel
```

然后删除之前添加的源即可。

原文：[How to Install Wine Devel 4.8 in Ubuntu 19.04 / 18.04](http://ubuntuhandbook.org/index.php/2019/05/nstall-wine-4-8-ubuntu-19-04-18-04/)

#### TIM在Ubuntu 19.04 & GNOME 3.32下不显示最小化托盘

1. 在火狐浏览器安装GNOME Shell integration插件

2. 终端运行

```bash
sudo apt-get install chrome-gnome-shell
```

不安装会导致插件报错，报错内容为“Unable to locate GNOME Shell settings or version. Make sure it is installed and running.”

3. 找到[topicons插件](https://extensions.gnome.org/extension/1031/topicons/)，虽然Ubuntu 19.04用的的GNOME 3.32，我们在这里的“Shell Version”选择3.30就可以，“Extension Version”选择22。安装完重启即可。

#### TIM字体太小

1. 先退出deepin-tim或deepin-qq，否则会提示错误。

2. 终端运行下面代码

```bash
env WINEPREFIX="$HOME/.deepinwine/Deepin-TIM" winecfg
```

如果是修改QQ界面字体大小，就把Deepin-TIM改成Deepin-QQ。

如果没有winecfg，先安装wine。

3. wine设置的显示 > 屏幕分辨率，然后将屏幕分辨率拖放到合适的大小。

原文：[Deepin-TIM或Deepin-QQ调整界面DPI字体大小的方法](https://www.lulinux.com/archives/4642)

### Firefox

#### 设置默认缩放

安装Default zoom插件。

### Ubuntu & Windows 双系统时间问题

#### 让Ubuntu禁用UTC（使用本地时间）

1. **Ubuntu 16.04 之前**

终端执行下面命令

```bash
sudo nano /etc/default/rcS
```

把utc=yes改成no

2. **Ubuntu 16.04 之后**

终端执行下面命令

```bash
timedatectl set-local-rtc 1 --adjust-system-clock
```

查看是否使用本地时间，可以在终端输入“timedatectl”

要改回UTC，在终端输入

```bash
timedatectl set-local-rtc 0
```

#### 让Windows用UTC（不建议）

在cmd中执行下面命令

1. 32位Windows

```cmd
Reg add HKLM\SYSTEM\CurrentControlSet\Control\TimeZoneInformation /v RealTimeIsUniversal /t REG_DWORD /d 1
```

2. 64位Windows

```cmd
Reg add HKLM\SYSTEM\CurrentControlSet\Control\TimeZoneInformation /v RealTimeIsUniversal /t REG_QWORD /d 1
```

原文：[How to Fix Time Differences in Ubuntu 16.04 & Windows 10 Dual Boot](http://ubuntuhandbook.org/index.php/2016/05/time-differences-ubuntu-1604-windows-10/)

### TLP

TLP 提供优秀的 Linux 高级电源管理功能，而且开箱即用。

英文简介：[ArchWiki - TLP](https://wiki.archlinux.org/index.php/TLP)

#### 安装TLP

```bash
sudo apt-get install tlp
```

#### 安装TLPUI

```bash
sudo add-apt-repository ppa:linuxuprising/apps
sudo apt update
sudo apt install tlpui
```

### tar

Linux下经常会见到各种tar.xx的压缩包，tar是打包的格式，后面那个才是压缩的方式。

#### 解压

对于这种形式的压缩包，其实直接一句命令就可以通吃了。

```bash
tar xf filename.tar.xx
```

搜索一番得知，从1.15起tar就可以自动识别压缩的格式，因此无需输入“-z”等参数来指定压缩格式。

“-v”参数其实也可以省略，因为详细信息刷刷刷的过，用处好像也不是很大。

实际上“-”本身也可以省略，因为这些“参数”都是必要的，如果没有参数，单纯使用“tar”是不行的。

从man里头节选部分命令翻译如下：

-x, --extract, --get 解压

-f, --file=ARCHIVE 要处理的压缩包名

#### 打包

如果只是打包的话，那么利用下面这个命令即可（打包当前目录下所有文件到pack.tar，星号可以自行替换成需要打包的内容）。

```bash
tar cf pack.tar *
```

从man里头节选部分命令翻译如下：

-c, --create 创建新的包

-r, --append 在已有包的尾部追加文件

-t, --list 列出包中的文件

-u, --update 更新文件（新文件不会取代旧文件，而是被追加到包的尾部，此时包中存在不同版本的同名文件）

#### 压缩

压缩就是在打包基础上增加一个指定压缩方法的参数

-a, --auto-compress （根据用户给定的后缀名来压缩，懒人专用）

-j, --bzip2

-J, --xz

-z, --gzip, --gunzip, --ungzip

-Z, --compress, --uncompress

### Apache2

#### 给目录加密码

1. 在希望加密的目录下创建 .htaccess 文件，内容如下

```bash
AuthName 'blablabla' # 这里填验证说明
AuthType Basic
AuthUserFile /path/.htpasswd # 这里是密码文件的路径，根据你的实际位置填写
require valid-user
```

2. 然后到你希望存放 .htpasswd 文件的目录下，输入如下命令

```bash
htpasswd -c .htpasswd [username] # 填上用户名
```

3. 开启 .htaccess 功能

打开Apache2配置文件（此处为Ubuntu 16.04的配置文件路径）

```bash
sudo nano /etc/apache2/apache2.conf
```

找到“<Directory "/var/www">”，将其下方的AllowOverride None改为AllowOverride All。

最后重启Apache2

```bash
sudo service apache2 restart
```

### aria2

#### 基础用法

普通下载

```bash
aria2c [target]
```

多线程下载

```bash
aria2c -s 16 -x 16 [target]
```

下载多个文件

```bash
aria2c [target1] [target2]
```

从文件中读取全部下载url，并下载

```bash
aria2c -i [filename]
```

进行限速

```bash
aria2c --max-download-limit=[SPEED] [target]
```

* SPEED的单位是B/s

带Auth下载文件（例如Apache加密目录）

```bash
aria2c http://[username]:[password]@[ip(url)]
```
