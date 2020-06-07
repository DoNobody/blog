# NLP实战高手课

## 极客时间课程

* 预测性建模
  * 预测性建模:只关注模型的预测准确性
  * 统计学模型:主要关注模型的可解释性
* 优化问题
  * 增强学习  
    如何在动态环境下做出正确的决定

## 另一种分类

* 结构化数据
* 文本数据

  * 常见的中文分词器  
    * Hanlp  
    > 1.维特比(viterbi)：效率和效果的最佳平衡。也是最短路分词，HanLP最短路求解采用Viterbi算法  
    > 2.双数组trie树 (dat)：极速词典分词，千万字符每秒（可能无法获取词性，此处取决于你的词典）  
    > 3.条件随机场(crf)：分词、词性标注与命名实体识别精度都较高，适合要求较高的NLP任务  
    > 4.感知机(perceptron)：分词、词性标注与命名实体识别，支持在线学习  
    > 5.N最短路 (nshort)：命名实体识别稍微好一些，牺牲了速度  
    * Stanford 分词  
    * ansj 分词器  
    * 哈工大 LTP  
    * KCWS分词器  
    * jieba  
    * IK  
    * 清华大学THULAC  
    * ICTCLAS  
  * 常见的英文分词工具：
    * Keras
    * Spacy
    * Gensim
    * NLTK

* 图像、视频数据
* 语音数据

## How

* 钻
* 快
* 深 夯实基础、数学与编程
* 广 广泛涉猎、抓住本质

## 损失函数

> **损失函数**

* 连续数据：
  L2 Loss:  
  $L_2(\widehat{y}, y) = (\widehat{y} - y)^2$  
  L2 Loss:  
  $L_2(\widehat{y}, y) = |\widehat{y} - y|$
* 离散数据  
  $p(y, \theta) = \left\{\begin{aligned} \theta, y = 1 = \theta^y(1-\theta)^{1-y} \\ 1-\theta y=0 \end{aligned}\right.$

> **全连接**

* softmax 转换  
  
> **激活函数**
  $$sigmoid(x) = \frac{e^x}{1+e^x}$$
  $$ f(x) = tanh(x) $$
  $$ f(x) = Relu(x)$$

> **Dropout**
> **Batch Normalization**

## 编码

* one-hot 方式

## Embedding

* Embedding 是一个将离散变量转为连续向量表示的一个方式

## RNN

* 马尔科夫过程
* 隐马尔科夫过程
  * HMM
* RNN (Recurrent Neural Networks)
* LSTM

### 半自动特征构建 Categorical Encoders

* 离散数据编码：
  * 编码（Target Mean Encoding）:
  * groupby 函数
    `df.groupby([A,B])[C].agg(func)`
    * 残差
  * One-hot Encoder
  * Ordinal Encoder
  * 其他Encoder
    * Count Encoder
    * HashMap
  
* 连续变量离散化
  > 衡量指标：纯度
  * 为什么做离散化： 
    * 捕捉非线性效应
    * 捕捉交叉效应
  * 常见的离散化：
    * Uniform
      * 不平衡线性
    * 基于Quantile
      * 占比范围
    * 基于聚类
      * kmeans
    * 基于树
      * 基于维度

* Entity Embedding
  * level 映射成一个数组
  * 全连接
  * 矩阵转换
    * 分块矩阵计算
  * 使用方式
    * vincinal information
      * 实现：
        * 了解数学表达
          * $$e: N * M $$
            * x
        * 逐步验证
        * 测试
* 连续变量的转换
  * 函数转换
    * log函数
    * exp
    * max，min，mean，std
  * 标准化
    * 对输入数据进行标准化
      * 方差，标准差
    * 基于ECDF的方法(对输入变换)
      * $F_x(x)$
        * $P(X<=x) = F_x(x)$
    * Box-Cox变换 和 Yeo-Johnson Trasform（对输出Y进行转换）
* 缺失值和异常值的处理
  * 概述
    * 定义难以确定
  * 常见的方法
    * EDA 加上业务逻辑
    * 可以使用中位数，分位数
  * 缺失值的填充可以根据业务决定，可以采用平均值，中位数和众数进行填充，也可以单独构建模型进行预测
  * 缺失值和异常本身是有信息量的，可以构造哑变量进行处理。

### 自动特征构建方法

* 应用
  * 开始前数据探索
  * 达到瓶颈后，进行特征探索
* 方法
  * 遗传算法
  * Symbolic Learning
    * gplean 库
  * AutoCross
    * Beam Search
    * 简化的逻辑回归求解方式
* 难点：
  * 组合优化问题

### 降维方式

* 为什么降维（防止过拟合）
  * 找到更加宏观信息（防止局部效果放大）
  * 找到交叉效应
  * 不建议先降维再拟合模型
* 常见模型
  * PCA
    * https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
  * NMF
    * https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.NMF.html
  * tSNE
    * https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html
* 应用
  * 进行预处理
    * 标准化
    * 选取重要变量
    * 去掉过于稀疏的个别变量
    * 构建2折和3折交叉效应
  * 降维方法中的参数并不十分重要
* 降维方法：Denoising AutoEncoder(DAE)
* 降维方法：Variational AutoEncoder(VAE)

### 变量选择方法

* 方法：
  * 初步选择，数据特征
    * 最重要的指标缺失值和变化率
  * “去一” 的选择方法
    * 控制变量对比法
      * 常常用逻辑回归来进行对比
    * 问题

### 集成树模型

## PDF课件

### 第一章：AI及NLP基础

```pdf
3.Hacker/NLP实战高手课/PDF/第一章：AI及NLP基础.pdf
```

### 第二章：深度学习简介和NLP试水

```pdf
3.Hacker/NLP实战高手课/PDF/第二章：深度学习简介和NLP试水.pdf
```

### 第三章：表格化数据挖掘

```pdf
3.Hacker/NLP实战高手课/PDF/第三章：表格化数据挖掘.pdf
```
