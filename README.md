# just_clicker
一款趁手的鼠标点击工具，支持跟随点击，固定位置点击，录制回放和找图点击模式。
主要利用的pyside6实现，截图用的是mss，鼠标键盘操作用的pynput，图片处理和匹配是opencv 和 numpy
点击radiobutton就可以切换不同模式。开启点击 shift+K  停止 shift+L

# 截图：
![Image text](https://raw.githubusercontent.com/hongmaju/light7Local/master/img/productShow/20170518152848.png)
![Image text](https://raw.githubusercontent.com/hongmaju/light7Local/master/img/productShow/20170518152848.png)
![Image text](https://raw.githubusercontent.com/hongmaju/light7Local/master/img/productShow/20170518152848.png)
![Image text](https://raw.githubusercontent.com/hongmaju/light7Local/master/img/productShow/20170518152848.png)

# 开发环境
win11
python 3.12

# 目前
1，还只是支持点击。
2，开启快捷键固定，暂不支持自定义
3，找图模式任务是临时的，切换模式或者重启就会消失，无法重新利用
3，当多屏幕时，各个模式需要在那个屏幕启动后，才能对那个屏幕生效，否则坐标定位会乱

# 后续优化：
1，支持配置快捷键
2，找图模式支持项目，可以持久化项目
3，目前找图模式载入还是需要截图路径去加载，后续改成直接换成numpy数组去存，方便持久化项目





