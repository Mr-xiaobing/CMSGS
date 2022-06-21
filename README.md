# 			CMSGS（Cheap motion-sensing game simulator）

# 									低成本体感游戏模拟器

> 一个可以让人使用动作来操作电脑的软件。可以实现，模拟体感游戏，手势控制等功能。

#### 开发进度：

- [x] 可以使用软件，并不需要操作代码来定义一套动作，并且可以控制动作对应的电脑键盘输出。
- [x] 加入手势部分的识别，添加射击模式
- [x] 添加了B站的观影模式。
- [ ] 使用更加底层的库来操作键盘鼠标的库
- [ ] 添加健身模式 （考虑）
- [ ] 添加忍术结印识别，可以尝试做一套定义忍术的添加页面。（考虑）
- [ ] 收录常见的手势，让用户可以定义手势的输出 （考虑）
- [ ] 与手机连接，让手机作为传感器实现 跑步和跳跃的识别功能。**（实现了这个就可以玩3D游戏了）本功能受到B站UP非洲小白皮视频的启发。**[视频地址](https://www.bilibili.com/video/BV1ML4y1K7Ty?spm_id_from=333.999.0.0&vd_source=8d591f7672e81310a860321bf62ee2a0)

#### build：

环境：windows系统，python3.9。

第三方库：

```
PyQt6~=6.1.0
jsonpickle~=2.1.0
mediapipe~=0.8.10
opencv-python~=4.5.5.64
PyAutoGUI~=0.9.53
numpy~=1.22.3
```

运行：

1.`git clone git@github.com:Mr-xiaobing/CMSGS.git`

2.下载第三库后，点击运行。

#### 下载使用（本应用只支持windows系统）：

**软件的下载安装：**

点击此处下 [应用](https://wws.lanzouw.com/iTJhm06mjjif)

下载完成后请务必查看使用说明。并且把软件解压到一个全英文的目录下（mediapipe调用模型的时候在中文的目录下会报错，我还未解决）。

**软件的使用和功能：**

**1.如何自定义一套动作：**

主页面：

![image-20220519200241589](https://s2.loli.net/2022/06/22/soi3H4jFxqnTchM.png)

**添加动作：**

![image-20220519200319956](https://s2.loli.net/2022/06/22/SLwMHInph4zWTq3.png)

点击添加动作按钮会在下方多出一行，可以填上对应的动作名称，动作的优先级，（**越小优先级越高，识别成功多个动作的时候，会执行优先级高的动作**）

输出按键（多个输出按键用+号连接）

**支持的按键输出：**

```
'a','b','c','A','C','1','2','3',    单个字符的键
'!','@','#'等
'enter'                             回车
‘esc'                              ESC键
'shiftleft','shiftright'            左右Shift键
'altleft','altright'                左右Alt键
'ctrlleft','ctrlright'              左右Ctrl键
‘tab'(or '\t')                     Tab键
'backspace','delete'                Backspace键和Delete键
'pageup','pagedown'                 Page Up 和Page Down键
'home','end'                        Home键和End键
'up','down','left','right'          上下左右箭头键
'f1','f2','f3'等                    F1至F12键
'volumemute','volumeup',volumedown' 静音，放大音量和减小音量键
'pause'                             暂停键
'capslock','numlock','scrolllock'   Caps Lock，Num Lock和 Scroll Lock键
'insert'                            Insert键
'printscreen'                       Prtsc或Print Screen键
'winleft','winright'                左右Win键(在windows上)
'command'                           Command键(在OS X上)
'option'                            Option键(在OS X上)
```

接着点击编辑，来定义动作，也就是判定条件这边：

![image-20220519202457857](https://s2.loli.net/2022/06/22/9HFcpfxRDKJnY86.png)

大家可以点击添加位置判断或者角度判断来定义动作。

**解释上图中定义的动作的含义：**

位置判断：这是一个升龙拳的动作，需要右手举起。这里的15表示的下图中15的这个关节点，0表示的是鼻子。上就表示右手要高过鼻子就认为是升龙拳了。

![image-20220519202325485](https://s2.loli.net/2022/06/22/u9dBnQPhmOvFHTS.png)

角度判断：向量1的方向是13->15  向量2的方向 13->11

组成的夹角在150到180就认为是判断成功了。

**一个动作里面需要所有的角度判断，位置判断都成功才认为是成功。有一个不符合都认为是失败的，不会执行对应的按键输出。**

大家也可以点击本地动作仓库的编辑动作，看看我定义好的那几套动作。定义的越准确识别的率越高。

**2.软件的使用。**

**使用定义的好的一套动作**：

点击开始游戏即可使用定义好动作。检测到符合判断条件的话，会进行对应按键的输出。

![](https://s2.loli.net/2022/06/22/Rgr9aS8vT5c6ut1.png)

**使用模式：**

直接点击对应的模式即可。

