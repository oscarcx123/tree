# 逆向工程学习记录

最近对Unity的逆向工程比较感兴趣，于是就开始自学，并把学习心得分享在这里。

注：本篇内容仅供学习交流，请勿用于违法用途

## 0x00 软件清单

操作环境如下：

* Windows 10 (Build 18362)
* JDK 12.0.2
* IDA pro 7.2 (这个自行解决，IDA普通版不清楚是否可行)
* dnSpy v6.0.5 (64-bit)
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

这里是获取玩家三叶草数量，我们直接修改成`return 9999`即可。

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
