### 右键cmd

Win10中Shift+右键打开cmd被替换成了PowerShell，就找到了这段代码在右键菜单中增加cmd选项。

用法：将下面代码复制到空文本文档，然后保存为“文件名.reg”，之后双击运行即可。

```cmd
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\Directory\shell\OpenCmdHere]
@="cmd"
"Icon"="cmd.exe"

[HKEY_CLASSES_ROOT\Directory\shell\OpenCmdHere\command]
@="cmd.exe /s /k pushd "%V""

[HKEY_CLASSES_ROOT\Directory\Background\shell\OpenCmdHere]
@="cmd"
"Icon"="cmd.exe"

[HKEY_CLASSES_ROOT\Directory\Background\shell\OpenCmdHere\command]
@="cmd.exe /s /k pushd \"%V\""

[HKEY_CLASSES_ROOT\Drive\shell\OpenCmdHere]
@="cmd"
"Icon"="cmd.exe"

[HKEY_CLASSES_ROOT\Drive\shell\OpenCmdHere\command]
@="cmd.exe /s /k pushd \"%V\""

[HKEY_CLASSES_ROOT\LibraryFolder\background\shell\OpenCmdHere]
@="cmd"
"Icon"="cmd.exe"

[HKEY_CLASSES_ROOT\LibraryFolder\background\shell\OpenCmdHere\command]
@="cmd.exe /s /k pushd \"%V\""
```

### Windows10 家庭版开启组策略

将下面内容粘贴到空文本文档，后缀名改为bat，管理员权限运行即可

```cmd
pushd "%~dp0"
dir /b C:\Windows\servicing\Packages\Microsoft-Windows-GroupPolicy-ClientExtensions-Package~3*.mum >List.txt
dir /b C:\Windows\servicing\Packages\Microsoft-Windows-GroupPolicy-ClientTools-Package~3*.mum >>List.txt
for /f %%i in ('findstr /i . List.txt 2^>nul') do dism /online /norestart /add-package:"C:\Windows\servicing\Packages\%%i"
```


### Word 设置“选择性粘贴”快捷键

使用下面的宏：

```cmd
Sub 无格式粘贴()
'
'无格式粘贴
Selection.PasteSpecial Link:=False, DataType:=wdPasteText, Placement:=wdInLine, DisplayAsIcon:=False
End Sub
```

注：宏功能在“视图”选项卡中

然后绑定快捷键，具体操作如下：

1. 按 Alt+F、T 以打开“Word 选项”对话框。

2. 选择“自定义功能区”，然后点击下方的“自定义”按钮。

3. 在“指定命令” > “类别”中选中“宏”

4. 在右侧找到刚刚保存的宏，并在下方“请按新快捷键”处指定热键
