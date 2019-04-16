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
