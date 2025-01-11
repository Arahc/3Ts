# SI100B-project-game
qty：

- 添加了 `Main.py`, `Settings.py`, `Menu.py` 和 `GameManager.py`，搭建了初步框架，并且实现了初步的菜单功能。
- 添加了 `settings` 内的调节音量功能。
- 添加了返回菜单功能，调整了依赖问题，创建了 `Utility.py`。

hzy：

- 添加地图和移动板块 `Map.py`, `Move.py`,  `MoveMain.py`
  - 其中 `Map.py` 是用来编辑地图的，可以用来编辑关卡
  - `Move.py` 是移动相关函数
  - `MoveMain.py` 主要是用来展示如何使用 `Move`
- 添加了地图和人物素材

cza:

- 搭建了卡牌战斗系统，包括：底层机制的实现以及游戏界面化

qty：

- 修改了移动板块的部分设置，将地图、移动部分和主函数关联，现在游戏可以作为一个整体开跑了。（去除了 `MoveMain.py`，修改了部分文件名）
- 将字体改为华文宋体
- 更改了大量素材，并对人物移动模型进行了优化

- 增加了转换界面时切换背景音乐的功能

- 增加了冲刺的功能
  - 一些细节：冲刺中不受重力加速度的作用，并且不可以中途改变方向。在空中最多只能冲刺一次，落地后重置冲刺次数

- 为人物添加了冲刺动画

- 添加了 npc

hzy：

- 生成了地图的基本要素：跳台，陷阱，宝箱（修改 `GenMap.py`）
- 使npc跟随地图边界移动（修改 `MapPage.py`）

qty:

- 完成了 `chatbox` （对话框）的制作
- 实现了 AI 驱动 npc 进行对话
- 新增了打开箱子的效果，现在可以获得钱了
- 整理了 `MapPage.py`，将其中和 `Player` 有关的部分提出为 `Player.py`
