# 逆向工程学习记录

最近对Unity的逆向工程比较感兴趣，于是就开始自学，并把学习心得分享在这里。

注：本篇内容仅供学习交流，请勿用于违法用途。本人所有逆向研究学习而产生的最终成品内容均不会进行发布和传播！如果你是想来下载各种破解APP的，可以点关闭了。

## 0x00 软件清单

操作环境如下：

* Windows 10 (Build 18362)
* JDK 12.0.2
* IDA pro 7.2 (这个自行解决，IDA普通版不清楚是否可行)
* dnSpy v6.0.5 (64-bit)
* HxD 2.3.0.0
* apktool 2.4.0

## 0x01 旅行青蛙 v1.0.4 (2019/09/02)

我在进行逆向的过程参考了[《旅行的青蛙Unity游戏逆向修改--Android篇》](http://www.alonemonkey.com/2018/02/02/unity-reverse-android/)这篇非常棒的文章，现在将要点提炼在下方。

0. 获取旅行青蛙1.0.4版本

网上一搜一大把，我下载之后重命名为`frog_104.apk`

1. 首先将apk用`apktool`进行反编译

```cmd
java -jar apktool.jar d frog_104.apk
```

2. 找到Assembly-CSharp.dll

查看`assets/bin/Data/Managed`文件夹下面的dll文件，其中`Assembly-CSharp.dll`便是游戏中的C#脚本

3. 使用dnSpy反编译找到的C#脚本

这个不用多说，把dll拖入dnSpy即可。左侧是对应的类，点击类就可以看到反编译出来的代码，然后根据游戏里面的一些特征来分析反编译出来的脚本。

4. 汉化（替换游戏中字符串）

没有看到下方的搜索框的话，点击`编辑->搜索程序集`。

搜索需要替换的关键字词（例如“名前”），搜索时选择“数字/字符串”。搜索结果可以直接双击进去查看内容。

这里搜索出来的是`CallTutorial`方法，下面是节选的一部分。

```csharp
case Step.a2_MO_GoHome:
{
	component4.Frog.SetActive(true);
	UI_Cmp.FrogCursorUI.SetActive(false);
	this.seTime = 0f;
	HelpPanel help = UI_Cmp.HelpUI.GetComponent<HelpPanel>();
	help.OpenPanel("かえるがいます\n名前をつけてあげましょう");
	help.ResetOnClick_Screen();
	help.SetOnClick_Screen(delegate
	{
		help.ClosePanel();
	});
	help.SetOnClick_Screen(delegate
	{
		UI_Cmp.blockUI(true, new Color(0f, 0f, 0f, 0f));
	});
	help.SetOnClick_Screen(delegate
	{
		this.seTime = -1E-06f;
	});
	help.SetOnClick_Screen(delegate
	{
		UI_Cmp.FrogCursorUI.SetActive(false);
	});
	break;
}
```

修改需要鼠标点击对应代码，选择`编辑IL指令`，然后直接修改对应字符串即可。

5. 修改三叶草数

要修改三叶草数可以从购买的时候入手，比如提示三叶草不足的时候！

直接搜索对应字符串（这里搜索“足”）找到代码

```csharp
if (SuperGameMaster.CloverPointStock() >= itemDataFormat.price)
{
    if (SuperGameMaster.FindItemStock(shopDataFormat.itemId) < 99)
    {
        base.GetComponent<FlickCheaker>().stopFlick(true);
        ConfilmPanel confilm = this.ConfilmUI.GetComponent<ConfilmPanel>();
        if (itemDataFormat.type == Item.Type.LunchBox)
        {
            confilm.OpenPanel_YesNo(string.Concat(new object[]
            {
                itemDataFormat.name,
                "\nを買いますか？\n（所持数\u3000",
                SuperGameMaster.FindItemStock(shopDataFormat.itemId),
                "）"
            }));
        }
        else
        {
            confilm.OpenPanel_YesNo(itemDataFormat.name + "\nを買いますか？");
        }
        confilm.ResetOnClick_Yes();
        confilm.SetOnClick_Yes(delegate
        {
            confilm.ClosePanel();
        });
        confilm.SetOnClick_Yes(delegate
        {
            this.GetComponent<FlickCheaker>().stopFlick(false);
        });
        confilm.SetOnClick_Yes(delegate
        {
            this.BuyItem();
        });
        confilm.ResetOnClick_No();
        confilm.SetOnClick_No(delegate
        {
            confilm.ClosePanel();
        });
        confilm.SetOnClick_No(delegate
        {
            this.GetComponent<FlickCheaker>().stopFlick(false);
        });
    }
    else
    {
        base.GetComponent<FlickCheaker>().stopFlick(true);
        ConfilmPanel confilm = this.ConfilmUI.GetComponent<ConfilmPanel>();
        confilm.OpenPanel("みつ葉が足りません");
        confilm.ResetOnClick_Screen();
        confilm.SetOnClick_Screen(delegate
        {
            confilm.ClosePanel();
        });
        confilm.SetOnClick_Screen(delegate
        {
            this.GetComponent<FlickCheaker>().stopFlick(false);
        });
    }
}
```

关键在于进行比较的`SuperGameMaster.CloverPointStock()`，点进去查看

```csharp
public static int CloverPointStock()
{
    return SuperGameMaster.saveData.CloverPoint;
}
```

这里是获取玩家三叶草数量，我直接修改成`return 9999`即可。

进入`编辑IL指令`，因为只需要两条指令，所以删去多余的指令，然后指令1的操作码应为`idc.i4`，操作符是9999，指令2就是`ret`，不需要改动。

修改之后每次读取玩家三叶草数量，都会返回9999

6. 修改抽奖券

跟修改三叶草数方法一模一样

7. 修改抽奖概率

搜索`白玉`找到如下代码

```csharp
public static readonly Dictionary<Rank, string> PrizeBallName = new Dictionary<Rank, string>
{
    {
        Rank.White,
        "白玉"
    },
    {
        Rank.Blue,
        "青玉"
    },
    {
        Rank.Green,
        "緑玉"
    },
    {
        Rank.Red,
        "赤玉"
    },
    {
        Rank.Gold,
        "黄玉"
    }
};
```

右键点击`PrizeBallName`选择“分析”找到在哪里被读取的，然后就会找出`PushRollButton`方法。

```csharp
public void PushRollButton()
{
    if (SuperGameMaster.TicketStock() < 5)
    {
        ConfilmPanel confilm = this.ConfilmUI.GetComponent<ConfilmPanel>();
        confilm.OpenPanel("ふくびき券が足りません");
        confilm.ResetOnClick_Screen();
        confilm.SetOnClick_Screen(delegate
        {
            confilm.ClosePanel();
        });
        return;
    }
    SuperGameMaster.GetTicket(-5);
    SuperGameMaster.set_FlagAdd(Flag.Type.ROLL_NUM, 1);
    base.GetComponentInParent<UIMaster>().freezeObject(true);
    base.GetComponentInParent<UIMaster>().blockUI(true, new Color(0f, 0f, 0f, 0.3f));
    this.LotteryCheck();
    this.ResultButton.GetComponent<RollResultButton>().CngImage((int)this.result);
    this.ResultButton.GetComponent<RollResultButton>().CngResultText(Define.PrizeBallName[this.result] + "がでました");
    this.LotteryWheelPanel.GetComponent<LotteryWheelPanel>().OpenPanel(this.result);
    SuperGameMaster.SetTmpRaffleResult((int)this.result);
    SuperGameMaster.SaveData();
    SuperGameMaster.audioMgr.PlaySE(Define.SEDict["SE_Raffle"]);
    this.BackFunc();
}
```

在`PushRollButton`方法中找出下面这行代码，其中调用了`PrizeBallName`。

```csharp
this.ResultButton.GetComponent<RollResultButton>().CngResultText(Define.PrizeBallName[this.result] + "がでました");
```

看到`Define.PrizeBallName[this.result]`，就右键单击`result`，分析，点开“被赋值于”，可以看到`RaffelPanel.LotteryCheck()`和`RaffelPanel.SetTmpResult()`方法，分别双击点开。

```csharp
public void LotteryCheck()
	{
		int num = UnityEngine.Random.Range(0, Define.PrizeBalls[Rank.RankMax]);
		this.result = Rank.White;
		int i = 0;
		int num2 = 0;
		while (i < 5)
		{
			num2 += Define.PrizeBalls[(Rank)i];
			if (num < num2)
			{
				this.result = (Rank)i;
				break;
			}
			i++;
		}
	}
  
public void SetTmpResult()
	{
		this.result = (Rank)SuperGameMaster.GetTmpRaffleResult();
		this.BackFunc();
	}
```

看名字很明显应该是`RaffelPanel.LotteryCheck()`，其中`PrizeBalls`应该就放了概率了，点开查看

```csharp
public static readonly Dictionary<Rank, int> PrizeBalls = new Dictionary<Rank, int>
{
    {
        Rank.White,
        60
    },
    {
        Rank.Blue,
        27
    },
    {
        Rank.Green,
        9
    },
    {
        Rank.Red,
        3
    },
    {
        Rank.Gold,
        1
    },
    {
        Rank.RankMax,
        100
    }
};
```

到这里应该就没有难度了。

8. 修改农场四叶草数

这次直接搜索关键词`clover`。

```csharp
public void checkCloverCreate()
{
    this.cloverList = SuperGameMaster.GetCloverList();
    bool flag = false;
    if (this.cloverList.Count == 0)  
    {
        flag = true;
        //这句话翻译的意思就是:有了四叶草的初期化标志。四叶草生成
        //也就是flag为true的时候会生成四叶草
        Debug.Log("[CloverFarm] クローバーの初期化フラグが立ちました。四葉を生成します");
    }
    if (this.cloverList.Count < this.cloverMax)
    {
        Debug.Log(string.Concat(new object[]
        {
            "[CloverFarm] クローバーの数を調整します：",
            this.cloverList.Count,
            " > ",
            this.cloverMax
        }));
    }
    while (this.cloverList.Count < this.cloverMax)
    {
        CloverDataFormat cloverDataFormat = new CloverDataFormat();
        cloverDataFormat.lastHarvest = new DateTime(1970, 1, 1);
        cloverDataFormat.timeSpanSec = -this.cloverList.Count - 1;
        cloverDataFormat.newFlag = true;
        this.cloverList.Add(cloverDataFormat);
    }
    if (this.cloverList.Count > this.cloverMax)
    {
        Debug.Log(string.Concat(new object[]
        {
            "[CloverFarm] クローバーの数を調整します：",
            this.cloverList.Count,
            " > ",
            this.cloverMax
        }));
        this.cloverList.RemoveRange(this.cloverMax - 1, this.cloverList.Count - this.cloverMax);
    }
    List<GameObject> list = new List<GameObject>();
    for (int i = 0; i < this.cloverList.Count; i++)
    {
        if (!this.cloverList[i].newFlag && this.cloverList[i].timeSpanSec <= 0)
        {
            list.Add(this.LoadCloverObject(i, this.cloverList[i]));
        }
    }
    int num = 0;
    for (int j = 0; j < this.cloverList.Count; j++)
    {
        if (this.cloverList[j].newFlag)
        {
            //这里根据flag调用不同的函数，
            if (!flag)
            {
                //生成三叶草
                list.Add(this.NewCloverObject(j, this.cloverList[j], list));
            }
            else
            {
                //生成四叶草，不同的是第四个参数为true
                list.Add(this.NewCloverObject(j, this.cloverList[j], list, true));
                flag = false;
            }
            this.cloverList[j].x = list[list.Count - 1].transform.localPosition.x;
            this.cloverList[j].y = list[list.Count - 1].transform.localPosition.y;
            Clover component = list[list.Count - 1].GetComponent<Clover>();
            this.cloverList[j].element = component.element;
            this.cloverList[j].spriteNum = component.spriteNum;
            this.cloverList[j].point = component.point;
            this.cloverList[j].newFlag = false;
            num++;
        }
    }
    foreach (GameObject gameObject in list)
    {
        int num2 = this.cloverOrderInLayer;
        foreach (GameObject gameObject2 in list)
        {
            if (gameObject.transform.position.y < gameObject2.transform.position.y)
            {
                num2++;
            }
        }
        gameObject.GetComponent<SpriteRenderer>().sortingOrder = num2;
    }
    Debug.Log(string.Concat(new object[]
    {
        "[CloverFarm] クローバー生成完了：",
        list.Count,
        "\u3000/ (新規：",
        num,
        ")"
    }));
}
```

其中`this.NewCloverObject(j, this.cloverList[j], list)`就是生成新草的方法，跟进去看看

```csharp
public GameObject NewCloverObject(int index, CloverDataFormat cloverData, List<GameObject> cloversObj)
{
    return this.NewCloverObject(index, cloverData, cloversObj, false);
}
```

继续跟。

```csharp
public GameObject NewCloverObject(int index, CloverDataFormat cloverData, List<GameObject> cloversObj, bool fourLeafFlag)
{
    Vector2 size = base.GetComponent<BoxCollider2D>().size;
    PolygonCollider2D component = base.GetComponent<PolygonCollider2D>();
    Vector2 vector;
    vector..ctor(base.GetComponent<BoxCollider2D>().offset.x - size.x / 2f, base.GetComponent<BoxCollider2D>().offset.y - size.y / 2f);
    int num = 0;
    bool flag;
    Vector3 vector2;
    do
    {
        flag = false;
        vector2 = new Vector2(vector.x + Random.Range(0f, size.x), vector.y + Random.Range(0f, size.y));
        if (!component.OverlapPoint(vector2 + base.transform.position))
        {
            flag = true;
        }
        else
        {
            for (int i = 0; i < cloversObj.Count; i++)
            {
                Vector2 size2 = cloversObj[i].GetComponent<BoxCollider2D>().size;
                if (Mathf.Abs(vector2.x - cloversObj[i].transform.localPosition.x) < size2.x / 2f && Mathf.Abs(vector2.y - cloversObj[i].transform.localPosition.y) < size2.y / 4f)
                {
                    flag = true;
                }
            }
            num++;
            if (num >= 100)
            {
                break;
            }
        }
    }
    while (flag);
    GameObject gameObject = Object.Instantiate<GameObject>(this.basePrefab, Vector3.zero, Quaternion.identity);
    CloverDataFormat cloverDataFormat = new CloverDataFormat();
    cloverDataFormat.point = 1;
    cloverDataFormat.element = 0;
    //如果第四个参数是false，这里就是四叶草生成的概率，是fourLeaf_percent是1那这个概率就是1/100
    if (Random.Range(0f, 10000f) < this.fourLeaf_percent * 100f)
    {
        cloverDataFormat.element = 1;
    }
    //如果传了这个参数为true直接生成四叶草
    if (fourLeafFlag)
    {
        cloverDataFormat.element = 1;
    }
    int element = cloverDataFormat.element;
    if (element != 0)
    {
        if (element == 1)
        {
            cloverDataFormat.spriteNum = Random.Range(0, this.fourCloverSprite.Length);
            gameObject.GetComponent<SpriteRenderer>().sprite = this.fourCloverSprite[cloverDataFormat.spriteNum];
        }
    }
    else
    {
        cloverDataFormat.spriteNum = Random.Range(0, this.cloverSprite.Length);
        gameObject.GetComponent<SpriteRenderer>().sprite = this.cloverSprite[cloverDataFormat.spriteNum];
    }
    gameObject.GetComponent<Clover>().SetCloverData(index, cloverDataFormat);
    gameObject.transform.parent = base.transform;
    gameObject.transform.localScale = Vector3.one;
    gameObject.transform.localPosition = vector2;
    return gameObject;
}
```

这里有两种方法，一种改概率，一种直接永远为true。

这里重点看改true的方法

```csharp
//如果传了这个参数为true直接生成四叶草
if (fourLeafFlag)
{
    cloverDataFormat.element = 1;
}
```

这里首先取`fourLeafFlag`判断然后跳转，所以修改为`true`即可。修改`ldarg.s fourLeafFlag`为`ldc.i4 1`，修改后的代码如下:

```csharp
if (true)
{
    cloverDataFormat.element = 1;
}
```

注：值得一提的是，`idc.i4 1`是true，`idc.i4 0`是false。

9. 保存修改成果

文件 > 保存模块 > 确定

10. apktool重新打包

```cmd
java -jar apktool.jar b ./frog_104
```

11. 签名

这个时候安装APP会提示“该软件包似乎已损坏”，这是因为还没签名。

不要使用`signapk.jar`这个工具，因为它只支持到JDK 8。

直接在cmd中使用jdk自带的`jarsigner`即可。

但是，在首次使用之前，需要生成一个自己的key。

```cmd
keytool -genkey -alias myKeyStore -keyalg RSA -validity 20000 -keystore myKeyStore
```

内容都可以随意填写，“密钥库口令”得记住，后面要用到。最后会询问“内容是否正确”，输入`y`即可。

生成密钥文件之后，可以进行签名了，这里会被要求输入刚才的“密钥库口令”。

```cmd
jarsigner -verbose -keystore myKeyStore -signedjar frog_104_signed.apk frog_104.apk myKeyStore
```

签名完成之后，就可以安装APP了。

12. 收获

通过这次简单的逆向之旅，我初步了解了简易的逆向过程以及逆向工具的使用。

13. 参考链接

* [旅行的青蛙Unity游戏逆向修改--Android篇](http://www.alonemonkey.com/2018/02/02/unity-reverse-android/)

* [简单Unity3D类安卓游戏逆向思路](https://blog.csdn.net/weixin_44058342/article/details/87940908)

* [Signapk.jar giving error java.lang.ClassNotFoundException: sun.misc.BASE64Encoder
](https://stackoverflow.com/questions/47095088/signapk-jar-giving-error-java-lang-classnotfoundexception-sun-misc-base64encode/47139732)

* [用jarsigner对android apk进行签名](https://blog.51cto.com/sunzeduo/1438368)

## 0x02 旅行青蛙 v1.6.2 (2019/09/03)

虽然还是旅行青蛙，但是这次要攻克的是它的最新版本 v1.6.2（于2019-06-24发布）。显然，这次难度会比上次要大一些。

0. 获取旅行青蛙1.6.2版本

网上一搜一大把，我下载之后重命名为`frog_162.apk`

1. 首先将apk用`apktool`进行反编译

```cmd
java -jar apktool.jar d frog_162.apk
```

2. 找到Assembly-CSharp.dll

嗯？这次在`assets/bin/Data/Managed`下面怎么没找到`Assembly-CSharp.dll`？

因为之前也看过一些逆向文章，很快就认出这个是IL2cpp打包过的游戏。

IL2cpp打包特征有两个：

* 在`assets/bin/Data/Managed/Metadata`下面找到`global-metadata.dat`。
* 在`lib/arm64-v8a`下面找到`libil2cpp.so`。除了`arm64-v8a`还可以是`armeabi-v7a`，`x86`等等。

3. 使用Il2CppDumper还原信息

双击运行Il2CppDumper.exe程序，先选择`libil2cpp.so`文件，再选择`global-metadata.dat`文件。

Unity版本写`2018.3`，选择模式3，如下所示。

```cmd
Input Unity version:
2018.3
Initializing metadata...
Select Mode: 1.Manual 2.Auto 3.Auto(Plus) 4.Auto(Symbol)
Initializing il2cpp file...
Applying relocations...
Searching...
CodeRegistration : ea5158
MetadataRegistration : ea51c8
Dumping...
Done !
Create DummyDll...
Done !
Press any key to exit...
```

在同一个目录下会生成`DummyDll`这个文件夹，以及`dump.cs`和`script.py`两个文件。

4. 用IDA打开`libil2cpp.so`文件

这个没啥好说，就是在打开文件之后记得加载（File > Script File）`script.py`。IDA分析需要一段时间，所以就先让它挂着跑，我去干别的。

5. 使用文本编辑器打开`dump.cs`

这里不使用dnSpy反编译找到的C#脚本，因为这些脚本实际上没啥用。

然后就开始搜索关键词了，实际上为了效率，可以利用前面1.0.4版本的未加密C#脚本来搜寻目标，但是现在是学习钻研逆向，当然不能偷懒。

这里想修改三叶草的数量，那就搜索关键词`clover`，翻一翻就会发现有个方法叫做`getCloverPoint`，下面内容节选自`dump.cs`

```csharp
public static DateTime Get_LoadDeviceTime(); // RVA: 0x49C504 Offset: 0x49C504
public static DateTime GetLastDateTime(); // RVA: 0x49C724 Offset: 0x49C724
public static float getGameTimer(); // RVA: 0x49C870 Offset: 0x49C870
public static Scenes GetNowScenes(); // RVA: 0x49C8D8 Offset: 0x49C8D8
public static void setNextScene(Scenes _NextScene); // RVA: 0x499B2C Offset: 0x499B2C
public static void SetStartScene(Scenes setScene); // RVA: 0x49C940 Offset: 0x49C940
public static bool GetIAPCallBackCntEnable(); // RVA: 0x49C9AC Offset: 0x49C9AC
public static void IAPCallBackCntReset(); // RVA: 0x49CA2C Offset: 0x49CA2C
public static void IAPCallBackCntUse(); // RVA: 0x49CAA8 Offset: 0x49CAA8
public static void MathTime_Clover(int addTimer); // RVA: 0x49CB40 Offset: 0x49CB40
public static List`1<CloverDataFormat> GetCloverList(); // RVA: 0x49D184 Offset: 0x49D184
public static void SaveCloverList(List`1<CloverDataFormat> cloverList); // RVA: 0x49D36C Offset: 0x49D36C
public static void getCloverPoint(int num); // RVA: 0x49D534 Offset: 0x49D534
public static int CloverPointStock(); // RVA: 0x49ADC0 Offset: 0x49ADC0
public static int TicketStock(); // RVA: 0x49AEB0 Offset: 0x49AEB0
public static void GetTicket(int getTicket); // RVA: 0x49D99C Offset: 0x49D99C
public static int GetTmpRaffleResult(); // RVA: 0x49DB24 Offset: 0x49DB24
public static void SetTmpRaffleResult(int _val); // RVA: 0x49DB9C Offset: 0x49DB9C
public static int CouponStock(); // RVA: 0x49AE38 Offset: 0x49AE38
public static void GetCoupon(int getCoupon); // RVA: 0x49DC18 Offset: 0x49DC18
public static int RequestCountStock(); // RVA: 0x49DDA4 Offset: 0x49DDA4
```

之前我的方向就出现了错误。我选择了`CloverPointStock()`这个方法来修改，但是后来却发现特别难弄。道理就是修改这个函数的返回值为一个固定数值，我感觉思路是对的，但是改了几次都没有成功，估计是技术还不过关吧，于是果断放弃，选择了后来证明可行的办法。

因此，要的就是下面这一行。

```csharp
public static void getCloverPoint(int num); // RVA: 0x49D534 Offset: 0x49D534
```

Offset要记下来，下面要用到。

6. 在IDA中定位对应代码

在IDA中按G键（或者Jump > Jump to address），然后输入刚才得到的Offset（本例中就是0x49D534），就可以定位到代码了。

此时看到下面内容（这里节选一段）

```assembly
; Attributes: bp-based frame

SuperGameMaster$$getCloverPoint

var_20= -0x20
var_10= -0x10
var_s0=  0

; __unwind {
STP             X22, X21, [SP,#-0x10+var_20]!
STP             X20, X19, [SP,#0x20+var_10]
STP             X29, X30, [SP,#0x20+var_s0]
ADD             X29, SP, #0x20
ADRP            X20, #byte_F48D6A@PAGE
LDRB            W8, [X20,#byte_F48D6A@PAGEOFF]
MOV             W19, W0
TBNZ            W8, #0, loc_49D56C
```

其实里头说了啥，现在不用太关心，需要看看这个方法是被谁调用了。

使用快捷键`Ctrl+X`可以查看那些地方调用了`getCloverPoint`这个方法。果不其然，找到了一个叫`DisplayPanel$$BuyItem`的方法，点进去看看。

```assembly
loc_5DA8C0
LDR             W8, [X20,#0x34]
MOV             X1, XZR
NEG             W0, W8
BL              SuperGameMaster$$getCloverPoint
LDR             W0, [X21,#0x10]
MOV             W1, #1
MOV             X2, XZR
BL              SuperGameMaster$$GetItem
ADRP            X28, #off_EBE6A0@PAGE
LDR             X28, [X28,#off_EBE6A0@PAGEOFF]
MOV             X0, X19
LDR             X1, [X28]
BL              Component$$GetComponentInParent_10897408
MOV             X21, X0
CBNZ            X21, loc_5DA900
```

在调用方法之前，这里有一个NEG操作。这句的意思就是把W8 * (-1)，然后赋值给W0，其实就是说W0就是W8的相反数。结合方法名称叫做`getCloverPoint`，可以大胆推测，买东西的时候就是“获取负数量的三叶草”。

```assembly
NEG             W0, W8
```

为了证实猜想，进去另一个调用了`getCloverPoint`的方法看看。我选择了`IAPPanel$$IAP_Complete`，因为一看就知道这个方法就是内购完成后进行的操作。代码如下。显而易见这里所使用的就是`MOV W0, W22`了。

```assembly
loc_51B294
MOV             W0, W22
MOV             X1, XZR
BL              SuperGameMaster$$getCloverPoint
CBZ             X21, loc_51B2B8
```

那么目标很明确了，就是把刚刚那个NEG改成MOV，这样就是把每次购买时的商品价格直接加到玩家的三叶草上。

注：最后跟1.0.4的C#代码作比较，再次证实了猜想的正确性。

附上对应的C#代码

```csharp
public static void getCloverPoint(int num)
{
	SuperGameMaster.saveData.CloverPoint += num;
	if (num > 0)
	{
		SuperGameMaster.set_FlagAdd(Flag.Type.CLOVER_NUM, num);
	}
}
```

```csharp
public void BuyItem()
{
	ShopDataFormat shopDataFormat = SuperGameMaster.sDataBase.get_ShopDB(this.selectShopIndex);
	ItemDataFormat itemDataFormat = SuperGameMaster.sDataBase.get_ItemDB_forId(shopDataFormat.itemId);
	SuperGameMaster.getCloverPoint(-itemDataFormat.price);
	SuperGameMaster.GetItem(shopDataFormat.itemId, 1);
	base.GetComponentInParent<UIMaster>().OnSave();
	//以下略
```

```csharp
public void IAP_Complete(int getId)
	{
		int num = 0;
		switch (getId)
		{
		case 1:
			num = 400;
			break;
		case 2:
			num = 1000;
			break;
		case 3:
			num = 1800;
			break;
		case 4:
			num = 2800;
			break;
		}
		SuperGameMaster.getCloverPoint(num);
	        //以下略
```

7. 把目标代码转换成hex

```assembly
MOV             W0, W8
```

随手一搜就有“Online ARM To Hex Converter”，那就再好不过了，直接丢进去转换即可，转换结果是`E003082A`。

8. 替换原有hex

回到IDA，鼠标选中需要修改的那行代码，在下面就能看到代码位置，我这里显示的是005DA8C8。

使用Hxd打开`libil2cpp.so`文件，`Ctrl+G`或者搜索 > 跳转，然后输入刚刚获取的位置信息（005DA8C8）。

在此处你应该能看到`E0 03 08 4B`，对了，这个就是`NEG W0, W8`。

把光标移动到`E0 03 08 4B`的头部（E前面），然后直接输入`E003082A`即可，输入的时候会自动覆盖掉原来的内容。改完记得保存。

9. 打包 & 签名

清理掉一些不必要的文件，例如IDA生成的文件，hxd生成的bak文件等等。

然后打包签名。

```cmd
java -jar apktool.jar b ./frog_104
```

```cmd
jarsigner -verbose -keystore myKeyStore -signedjar frog_162_signed.apk frog_162.apk myKeyStore
```

安装APP，在进行新手教程的时候会需要买东西，此时三叶草不减反增，证明逆向成功！

12. 收获

这次花的时间稍微长一些，研究学习了从汇编码层面来修改逻辑。

13. 参考链接

* [记录一次Unity3d-il2cpp游戏修改](https://www.52pojie.cn/thread-982655-1-1.html)

* [Keil-Search](https://developer.arm.com/keil-search)

* [ARM汇编之解惑条件标志，条件码，条件执行](https://www.jianshu.com/p/0c6192da2fd0)

* [ARM汇编指令(ARM寻址方式、汇编指令、伪指令)](https://blog.csdn.net/cwcwj3069/article/details/7948078)

## 0x03 神庙逃亡 v1.9.6 (2019/09/03)

本来想尝试逆向神庙逃亡最新版的，无奈从v1.10.0开始就对游戏进行了加密，因此挑选最后一个无加密的版本进行练习。

0. 获取神庙逃亡v1.9.6版本

网上一搜一大把，我下载之后重命名为`temple_196.apk`。

还是先进行如下常规步骤。

1. 首先将apk用`apktool`进行反编译

2. 找到Assembly-CSharp.dll

3. 使用dnSpy反编译找到的C#脚本

4. 寻找目标

这里搜索了`Buy`，然后发现了一个叫`BuyItem`的方法。

```csharp
private void BuyItem()
	{
		int num = this.RecordManager.GetCoinCount(this.PlayerManager.GetActivePlayer());
		if (this.Price <= num)
		{
			num -= this.Price;
			this.RecordManager.SetCoinCount(this.PlayerManager.GetActivePlayer(), num);
			if (this.Type == RecordManager.StoreItemType.kStoreItemDisableAds)
			{
			}
			int playerLevelForUpgradeType = this.RecordManager.GetPlayerLevelForUpgradeType(this.PlayerManager.GetActivePlayer(), this.Type);
			if ((this.Type == RecordManager.StoreItemType.kStoreItemCoinBonus || this.Type == RecordManager.StoreItemType.kStoreItemVacuum || this.Type == RecordManager.StoreItemType.kStoreItemInvincibility || this.Type == RecordManager.StoreItemType.kStoreItemBoost) && playerLevelForUpgradeType >= 7)
			{
				this.RecordManager.SetPlayerLevelForUpgradeType(this.PlayerManager.GetActivePlayer(), this.Type, 6);
			}
			else
			{
				this.RecordManager.SetPlayerLevelForUpgradeType(this.PlayerManager.GetActivePlayer(), this.Type, playerLevelForUpgradeType + 1);
			}
			base.SendMessageUpwards("AdjustCoins");
			this.RecordManager.SaveRecords();
			this.Reconfigure();
			AudioManager.Instance.PlayFX(AudioManager.Effects.cashRegister, 1f);
			if (this.Type == RecordManager.StoreItemType.kStoreItemAngelWings && playerLevelForUpgradeType == 0)
			{
				this.AlertView.ShowAlert(Strings.Txt("StoreItemResurrectionWingsPopupTitle"), Strings.Txt("StoreItemResurrectionWingsPopupText"), Strings.Txt("Ok"), null);
			}
			if (this.Type == RecordManager.StoreItemType.kStoreItemPermaWings && playerLevelForUpgradeType == 0)
			{
				this.AlertView.ShowAlert(Strings.Txt("StoreItemPermaWingsPopupTitle"), Strings.Txt("StoreItemPermaWingsPopupText"), Strings.Txt("Ok"), null);
			}
			if (this.Type == RecordManager.StoreItemType.kStoreItemHeadStart && playerLevelForUpgradeType == 0)
			{
				this.AlertView.ShowAlert(Strings.Txt("StoreItemHeadStartPopupTitle"), Strings.Txt("StoreItemHeadStartPopupText"), Strings.Txt("Ok"), null);
			}
			if (this.Type == RecordManager.StoreItemType.kStoreItemHeadStartMega && playerLevelForUpgradeType == 0)
			{
				this.AlertView.ShowAlert(Strings.Txt("StoreItemHeadStartMegaPopupTitle"), Strings.Txt("StoreItemHeadStartMegaPopupText"), Strings.Txt("Ok"), null);
			}
			if (this.Class == StoreItem.StoreItemClass.Character)
			{
				this.ActivateCharacter(this.Type);
			}
			if (this.Class == StoreItem.StoreItemClass.Wallpaper)
			{
				this.GrabWallpaper(this.Type);
			}
		}
		else
		{
			this.AlertView.ShowAlert(Strings.Txt("StoreItemNotEnoughCoinsTitle"), Strings.Txt("StoreItemNotEnoughCoinsText"), Strings.Txt("No"), Strings.Txt("Yes"), null, delegate()
			{
				StoreGUI.Instance.HideAll();
				VCGUI.Instance.SlideIn(StoreGUI.Instance);
			});
		}
	}
```

关键在这一小段。游戏使用GetCoinCount方法获取金币数量，然后跟价格作比较，如果金币大于等于价格就扣除。这里有很多思路，比如可以把扣钱改成加钱，我这里走的是修改获取金币的方法的返回值的路线。

```csharp
int num = this.RecordManager.GetCoinCount(this.PlayerManager.GetActivePlayer());
		if (this.Price <= num)
		{
			num -= this.Price;
```

那就跟进去GetCoinCount方法看看。

```csharp
public int GetCoinCount(int playerId)
	{
		RecordManager.cPlayerRecord cPlayerRecord = this.FindPlayerRecord(playerId);
		return (cPlayerRecord == null) ? 0 : cPlayerRecord.coinCount;
	}
```

这里很明显了，直接把`return (cPlayerRecord == null) ? 0 : cPlayerRecord.coinCount;`替换成`return 99999;`即可。

点击需要修改的那行代码，右键编辑IL指令，然后直接删除高亮指令（就是选中的代码），新建指令`idc.i4 99999`和`ret`。

5. 保存，签名，打包，真机测试成功。

6. 收获

这次花的时间就非常短了，有了之前的经验，这次可以很快定位到目标并且完成修改。其实除了修改金币，还可以尝试修改别的东西，比如各种道具效果。

7. 后记

试着改了下道具效果，没有测试，但是地方应该是对了。

搜索`Boost`，发现有个方法叫`StartBoost`，点进去看看。

```csharp
public void StartBoost(float distance, bool isMega)
	{
		DebugEx.Log("PICKUP: BOOST of " + distance);
		bool hasBoost = this.HasBoost;
		this.HasBoost = true;
		this.IsMegaBoost = isMega;
		if (!hasBoost)
		{
			this.VelocityBeforeBoost = ((!this.IsMegaBoost) ? this.GetRunVelocity() : this.MaxRunVelocity);
			this.StartInvcibility(4f);
		}
		this.BoostDistanceLeft = distance + 50f;
		this.TimeSinceLastPowerup = 0f;
		this.StumbleKillTimer += 10f;
	}
```

右键分析被谁调用，发现有个叫`UseHeadStartMega`，感觉像是我想要的，点进去看看。

```csharp
public void UseHeadStartMega()
	{
		if (!this.IsPaused && !this.IsInCountdown && !this.IsGameOver && !this.IsTutorialMode && !this.IsIntroScene && !this.GamePlayer.IsDead && !this.GamePlayer.IsFalling && this.DistanceTraveled > this.HeadStartStartDistance && this.DistanceTraveled < this.HeadStartEndDistance)
		{
			this.Audio.PlayFX(AudioManager.Effects.bonusPickup, 1f);
			this.RecordManager.AdjustPlayerLevelForUpgradeType(this.PlayerManager.GetActivePlayer(), RecordManager.StoreItemType.kStoreItemHeadStartMega, -1);
			this.RecordManager.SaveRecords();
			float distance = this.HeadStartMegaBoostDistance - this.DistanceTraveled;
			this.GamePlayer.StartBoost(distance, false);
			this.UsedHeadStart = true;
			if (!this.UsedPowers)
			{
				this.UsedPowers = true;
				this.ScoreWhenFirstUsedPowers = this.GamePlayer.Score;
			}
		}
	}
```

然后发现有个字段叫`HeadStartMegaBoostDistance`，这个应该就是道具冲刺的距离了，点进去看看。

```csharp
public float HeadStartMegaBoostDistance = 2350f;
```

如果觉得原本的冲刺距离不够爽，那就改成235000f好了~

## 0x04 神庙逃亡2 v1.12.1 (2019/09/05)

既然逆向了神庙逃亡1，那就顺手把神庙逃亡2也逆向了吧~

这次选择了老旧的1.12.1版本，因为这个版本没有进行加密。

0. 获取神庙逃亡v1.12.1版本

网上一搜一大把，我下载之后重命名为`temple2_1121.apk`。

先进行常规步骤：用`apktool`进行反编译，找到Assembly-CSharp.dll，使用dnSpy反编译找到的C#脚本，寻找目标。

注：后面为了节约时间，常规步骤会直接略过不写。

在神庙逃亡2中，可以通过点击“关注Facebook”和“关注Twitter”来获取一定的资源，我的目标就是把这两个按钮变成无限提款机。

1. 修改“关注Facebook”相关方法

这里直接搜索方法`Facebook`，然后发现了一个叫`PerformLikeOnFacebook`的方法。

```csharp
private void PerformLikeOnFacebook()
	{
		UIConfirmDialog.onNegativeResponse -= this.CanceledLike;
		UIConfirmDialog.onPositiveResponse -= this.PerformLikeOnFacebook;
		EtceteraAndroid.showWebView("http://www.facebook.com/Tem****un");
		GameProfile.SharedInstance.ProfileData.HasLikedOnFacebook = true;
		if (this.FacebookGiftType == CostType.Coin)
		{
			GameProfile.SharedInstance.Player.coinCount += this.FacebookGiftAmount;
		}
		else if (this.FacebookGiftType == CostType.Special)
		{
			GameProfile.SharedInstance.Player.specialCurrencyCount += this.FacebookGiftAmount;
		}
		GameProfile.SharedInstance.Serialize();
		this.FillInFreeOffers();
	}
```

关键逻辑很明显，判断礼物类型，然后根据类型发放对应数额。但是既然要重复领取，总不能每次都弹出Facebook页面。所以直接把`EtceteraAndroid.showWebView("http://www.facebook.com/Tem****un");`对应的IL指令删掉即可。

然后看到下一行是`GameProfile.SharedInstance.ProfileData.HasLikedOnFacebook = true;`，这个很明显就是用来记录是否领取过的flag，当然是要改成false啦。编辑IL指令，把`idc.i4.1`改成`idc.i4.0`即可。

其实到这里就可以直接把`this.FacebookGiftAmount`替换成想要的数字就可以了，因为`this.FacebookGiftType`大概率不是`Coin`就是`Special`，但是我还是想直接把`if (this.FacebookGiftType == CostType.Coin)`替换成`if(true)`。因此单独把关键段落拿出来并看看IL代码。

```csharp
if (this.FacebookGiftType == CostType.Coin)
		{
			GameProfile.SharedInstance.Player.coinCount += this.FacebookGiftAmount;
		}
		else if (this.FacebookGiftType == CostType.Special)
		{
			GameProfile.SharedInstance.Player.specialCurrencyCount += this.FacebookGiftAmount;
		}
```

我把IL代码加了空行，这样可以跟C#代码对应起来。

```IL
14	003C	ldarg.0
15	003D	ldfld	valuetype CostType UIFreeStuffViewController::FacebookGiftType
16	0042	brtrue	26 (0068) ldarg.0 

17	0047	ldsfld	class GameProfile GameProfile::SharedInstance
18	004C	callvirt	instance class PlayerStats GameProfile::get_Player()
19	0051	dup
20	0052	ldfld	int32 PlayerStats::coinCount
21	0057	ldarg.0
22	0058	ldfld	int32 UIFreeStuffViewController::FacebookGiftAmount
23	005D	add
24	005E	stfld	int32 PlayerStats::coinCount
25	0063	br	38 (0090) ldsfld class GameProfile GameProfile::SharedInstance

26	0068	ldarg.0
27	0069	ldfld	valuetype CostType UIFreeStuffViewController::FacebookGiftType
28	006E	ldc.i4.1
29	006F	bne.un	38 (0090) ldsfld class GameProfile GameProfile::SharedInstance

30	0074	ldsfld	class GameProfile GameProfile::SharedInstance
31	0079	callvirt	instance class PlayerStats GameProfile::get_Player()
32	007E	dup
33	007F	ldfld	int32 PlayerStats::specialCurrencyCount
34	0084	ldarg.0
35	0085	ldfld	int32 UIFreeStuffViewController::FacebookGiftAmount
36	008A	add
37	008B	stfld	int32 PlayerStats::specialCurrencyCount
```

先看源代码第一句`if (this.FacebookGiftType == CostType.Coin)`。

```IL
14	003C	ldarg.0
15	003D	ldfld	valuetype CostType UIFreeStuffViewController::FacebookGiftType
16	0042	brtrue	26 (0068) ldarg.0 
```

这个`ldarg.0`就是this，下面这个`valuetype CostType UIFreeStuffViewController::FacebookGiftType`很明显就是比较的内容，`ldfld`顾名思义就是“Load Field”，作用大概就是获取对象的值（Push the value of field of object (or value type) obj, onto the stack.）。`brtrue`顾名思义就是“Branch True”，就是如果为真跳转到指定目标（Branch to target if value is non-zero (true).）

直接改成下面这样，这时候C#代码就是`if(true)`。brfalse就是如果为假跳转到指定目标（Branch to target if value is zero (false).）

```IL
14	003C	ldc.i4.1
15	003D	brfalse	25 (0063) ldarg.0 
```

接下来，我想让这个这个true分支中给钻石而不是给金币，那么就可以看看那一段的关键IL代码

```IL
20	0052	ldfld	int32 PlayerStats::coinCount
21	0057	ldarg.0
22	0058	ldfld	int32 UIFreeStuffViewController::FacebookGiftAmount
23	005D	add
24	005E	stfld	int32 PlayerStats::coinCount
```

用大白话说就是取出coinCount，取出FacebookGiftAmount，两个相加，然后赋值给coinCount。

stfld应该就是赋值（Replace the value of field of the object obj with value.）。

要修改ldfld内容的话也很容易。首先单击`20	0052	ldfld	int32 PlayerStats::coinCount`这行，选择“字段”，搜索`specialCurrencyCount`，在下方搜索结果选中，点击确定即可。

最后结果就是下面这样，输入`ldc.i4	888888`会自动被转换成`ldc.i4	0xD9038`。此时C#代码是`GameProfile.SharedInstance.Player.specialCurrencyCount += 888888;`。

```IL
19	004D	ldfld	int32 PlayerStats::specialCurrencyCount
20	0052	ldc.i4	0xD9038
21	0057	add
22	0058	stfld	int32 PlayerStats::specialCurrencyCount
```

这里针对点击“关注Facebook”按钮的修改就完成了。修改后的这个方法的C#代码如下：

```csharp
private void PerformLikeOnFacebook()
	{
		UIConfirmDialog.onNegativeResponse -= this.CanceledLike;
		UIConfirmDialog.onPositiveResponse -= this.PerformLikeOnFacebook;
		GameProfile.SharedInstance.ProfileData.HasLikedOnFacebook = false;
		if (true)
		{
			GameProfile.SharedInstance.Player.specialCurrencyCount += 888888;
		}
		else if (this.FacebookGiftType == CostType.Special)
		{
			GameProfile.SharedInstance.Player.specialCurrencyCount += this.FacebookGiftAmount;
		}
		GameProfile.SharedInstance.Serialize();
		this.FillInFreeOffers();
	}
```

2. 修改“关注Twitter”相关方法

方法是跟修改“关注Facebook”完全一样的。

原始的`PerformLikeOnTwitter`方法如下：

```csharp
private void PerformLikeOnTwitter()
	{
		UIConfirmDialog.onNegativeResponse -= this.CanceledFollow;
		UIConfirmDialog.onPositiveResponse -= this.PerformLikeOnTwitter;
		EtceteraAndroid.showWebView("http://twitter.com/tem****un");
		GameProfile.SharedInstance.ProfileData.HasLikedOnTwitter = true;
		if (this.TwitterGiftType == CostType.Coin)
		{
			GameProfile.SharedInstance.Player.coinCount += this.TwitterGiftAmount;
		}
		else if (this.TwitterGiftType == CostType.Special)
		{
			GameProfile.SharedInstance.Player.specialCurrencyCount += this.TwitterGiftAmount;
		}
		GameProfile.SharedInstance.Serialize();
		this.FillInFreeOffers();
	}
```

修改之后应该是下面这样。

```csharp
private void PerformLikeOnTwitter()
	{
		UIConfirmDialog.onNegativeResponse -= this.CanceledFollow;
		UIConfirmDialog.onPositiveResponse -= this.PerformLikeOnTwitter;
		GameProfile.SharedInstance.ProfileData.HasLikedOnTwitter = false;
		if (true)
		{
			GameProfile.SharedInstance.Player.coinCount += 999999;
		}
		else if (this.TwitterGiftType == CostType.Special)
		{
			GameProfile.SharedInstance.Player.specialCurrencyCount += this.TwitterGiftAmount;
		}
		GameProfile.SharedInstance.Serialize();
		this.FillInFreeOffers();
	}
```

3. 改开局冲刺距离

这个很简单，搜索“Mega”就找到一个叫`OnMegaHeadStart`的方法，如下所示。

```csharp
public void OnMegaHeadStart()
	{
		GameProfile.SharedInstance.Player.coinCount -= GameProfile.SharedInstance.Player.GetMegaHeadStartCost();
		GamePlayer.SharedInstance.StartBoost();
		GamePlayer.SharedInstance.BoostDistanceLeft = 2500f;
		GameController.SharedInstance.HeadStartsThisRun++;
		TRAnalytics.logEvent("MegaHeadStart", true, false);
		if (this.headStartRoot != null)
		{
			NGUITools.SetActive(this.headStartRoot.gameObject, false);
		}
		if (this.megaHeadStartRoot != null)
		{
			NGUITools.SetActive(this.megaHeadStartRoot.gameObject, false);
		}
		AudioManager.SharedInstance.PlayFX(AudioManager.Effects.cashRegister, 1f, 1f);
	}
```

很明显，直接修改`BoostDistanceLeft`即可。

4. 内购

内购其实也不难，毕竟资源发放逻辑在本地。不够由于技术比较菜，找了半天才发现目标。

突破口在于断网尝试内购的字符串“Cannot connect to the internet.”

直接搜索“Cannot Connect”会发现叫做`ShowNetworkErrorDialog`的方法。点进去看看。

```csharp
public void ShowNetworkErrorDialog()
	{
		if (this.confirmDialog == null)
		{
			return;
		}
		this.confirmDialog.ShowInfoDialog("Error!", "Cannot connect to\nthe internet.", "Close");
	}
```

嗯，这个就是蹦个对话框出来，跟观察到的相符。看看被谁调用了，发现有两个可疑方法，`TryRealMoneyPurchase`和`OnBuyIAP`。

观察发现关键代码如下：

```csharp
this.PurchaseSuccessfulWithProductID(charData.ProductId, string.Empty);
```

接下来就简单了，直接修改对应逻辑，让上面两个方法直接执行“购买成功”的代码。修改后的代码就不贴了。

5. 保存，签名，打包，真机测试成功。

6. 收获

这次学习了更加多的IL指令。而且通过逆向发现，内购其实就是跟内购服务通信之后，通过返回的内容决定是否发放对应物品。。。。。。比想象中的机制要简单很多啊~

7. 参考链接

* [OpCodes Class (System.Reflection.Emit) | Microsoft Docs](https://docs.microsoft.com/en-us/dotnet/api/system.reflection.emit.opcodes?view=netframework-4.8)

* [List of CIL instructions - Wikipedia](https://en.wikipedia.org/wiki/List_of_CIL_instructions)

* [Why do I have to do ldarg.0 before calling a field in MSIL?](https://stackoverflow.com/questions/1785372/why-do-i-have-to-do-ldarg-0-before-calling-a-field-in-msil)
