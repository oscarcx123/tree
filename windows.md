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