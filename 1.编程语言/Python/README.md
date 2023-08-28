[首页](/)
# Python精进

## 版本更新

* Python 3.5 使用 async 和 await 语法实现协程

## 性能优化

* 尽量使用 generator（生成器），如 xrange, yield, dict.iteritems(), itertools
* 排序尽量使用 .sort()， 其中使用 key 比 cmp 效率更高
* 适当使用 list 迭代表达式，如[i for i in xrane(10)]
* 使用 set 来判断元素的存在
* 使用 dequeue 来做双端队列
