### GameManager

游戏进程

### Listeners

监听者：监听所有的 event 并有给出响应的能力。

- 方法：`listen`  `post`

### Entity

实体：具有实体、需要绘制的对象

- 父类：`Listeners`
- 方法：`draw`

### Scene

场景：在每个时刻都会被渲染

- 父类：`Listeners`

### Menu

菜单界面

- 父类：`Listeners`

- 方法：`handle` `check_mouse_click` 