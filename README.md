# 猜数字游戏规则
1. 本游戏为情怀而制作，还原了多年以前文曲星中的猜数字游戏；
2. 数字共有4位，每个数字最多出现一次，0可以出现在第一位；
3. 每猜一次会获得相应的提示，格式为aAbB，aA表示所猜数字有a个既猜对了数字又猜对了位置，bB则代表有b个只猜对了数字而猜错了位置；

* 举个栗子：

谜底 | 猜测 | 提示 | 解析
---- | ---- | ---- | -------------
1234 | 5612 | 0A2B | 你猜中了两个数字，但是位置都错了，请换两个数字试试
1234 | 1423 | 1A3B | 你4个数字都猜中了，但是只有1个数字的位置是对的，其他3个位置错了，请调整数字的顺序直到猜中4A

4. 当玩家猜到4A0B时游戏结束，并记录猜的总次数；
5. 游戏一旦开始，若玩家中途退出(未能猜到4A0B)，则视为逃跑并记录在案；
6. 英雄榜取平均次数进行升序排名，且玩家至少需要完成10场游戏才能进入英雄榜；
7. 祝你游戏愉快！

[Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
