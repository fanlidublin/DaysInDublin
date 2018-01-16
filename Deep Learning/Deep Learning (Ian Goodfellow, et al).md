
# Deep Learning 
**Ian Goodfellow, Yoshua Bengio and Aaron Courville**

![](http://t2.gstatic.com/images?q=tbn:ANd9GcRq9yUJmITp5UfjgEIHlsAi34WXhk8P13CCQoKjIRqleVZQI8uq)

## Contents 目录

#### 1. Introduction
    1.1 Who Should Read This Book?  本书面向的读者
    1.2 Historicak Trends in Deep Learning  深度学习的历史趋势

### *<font color="#0000CC">Applied Math and Machine Learning Basics</font>*
#### 2. Linear Algebra
    2.1 Scalars, Vectors, Matrices and Tensors  标量、向量、矩阵和张量
    2.2 Multiplying Matrices and Vectors  矩阵与向量相乘
    2.3 Identity and Inverse Matrices  单位矩阵与逆矩阵
    2.4 Linear Dependence and Span  线性相关与生成子空间
    2.5 Norms  范数
    2.6 Special Kinds of Matrices and Vectors  特殊类型的矩阵和向量
    2.7 Eigendecpmposition  特征分解
    2.8 Singular Value Decomposition  奇异值分解
    2.9 The Moore-Penrose Pseudoinverse  Moore-Penrose 伪逆
    2.10 The Trace Operator  逆运算
    2.11 The Determinant  行列式
    2.12 Example: Principal Components Analysis (PCA)  实例：主成分分析
    
#### 3. Probability and Information Theory
    3.1 Why Probability?  使用概率的原因
    3.2 Random Variables  随机变量
    3.3 Probability Distributions  概率分布
        3.3.1 Discrete Variables and Probability Mass Functions  离散型变量和概率质量函数
        3.3.2 Continuous Variables and Probability Density Function  连续型变量和概率密度函数
    3.4 Marginal Probability  边缘概率
    3.5 Conditional Probabiliyu  条件概率
    3.6 The Chain Rule of Conditional Probabilities  条件概率的链式法则
    3.7 Independence and Conditional Independence  独立性和条件独立性
    3.8 Expectation, Variance and Covariance  期望、方差和协方差
    3.9 Common Probability Distributions  常用概率分布
        3.9.1 Bernoulli Distribution  Bernoulli 分布
        3.9.2 Multinoulli Distribution  Multinoulli 分布
        3.9.3 Gaussian Distribution  高斯分布
        3.9.4 Exponential and Laplace Distributions  指数分布和Laplace分布
        3.9.5 The Dirac Distribution and Empirical Distribution  Dirac分布和经验分布
        3.9.6 Mixtures of Distributions  分布的混合
    3.10 Useful Properties of Common Functions  常用函数的有用性质
    3.11 Bayes'Rule  贝叶斯规则
    3.12 Technical Details of Continuous Variables  连续型变量的技术细节
    3.13 Information Theory  信息论
    3.14 Structured Probabilitic Models  结构化概率模型

#### 4. Numerical Computions
    4.1 Overflow and Uderflow  上溢和下溢
    4.2 Poor Conditioning  病态条件
    4.3 Gradient-Based Optimization  基于梯度的优化方法
        4.3.1 Beyond the Gradient: Jacobian and Hessian Matrices  梯度之上：雅可比和海森矩阵
    4.4 Constrained Optimization  约束优化
    4.5 Example: Linear Least Squares  实例：线性最小二乘
    
#### 5. Machine Learning Basics
    5.1 Learning Algorithms  学习算法
        5.1.1 The Task, T  任务T
        5.1.2 The Performance Measure, P  性能度量P
        5.1.3 The Experience, E  经验E
        5.1.4 Example: Linear Regression  实例：线性回归
    5.2 Capacity, Overfitting and Underfitting  容量、过拟合与欠拟合
        5.2.1 The No Free Lunch Theorem  没有免费午餐定律
        5.2.2 Regularization  正则化
    5.3 Hyperparameters and Validation Sets  超参数与验证集
        5.3.1 Cross-Validation  交叉验证
    5.4 Estimators, Bias and Variance  估计、偏差与方差
        5.4.1 Point Estimation  点估计
        5.4.2 Bias  偏差
        5.4.3 Variance and Standard Error  方差与标准差
        5.4.4 Trading off Bias and Variance to Minimize Mean Squared Error  权衡偏差与方差以最小化均方误差
        5.4.5 Consistency  一致性
    5.5 Maximum Likelihood Estimation  最大似然估计
        5.5.1 Conditional Log-Likelihood and Mean Squared Error  条件对数似然与均方误差
        5.5.2 Properties of Maximum Likelihood  最大似然的性质
    5.6 Bayesian Statistics  贝叶斯统计
        5.6.1 Maximum-a-Posteriori (MAP) Estimation  最大后验估计
    5.7 Supervised Learning Algorithms  监督学习算法
        5.7.1 Probabilistic Supervised Learning  概率监督学习
        5.7.2 Support Vector Machines  支持向量机
        5.7.3 Other Simple Supervised Learning Algorithms  其他简单的监督学习算法
    5.8 Unsupervised Learning Algorithms  无监督学习算法
        5.8.1 Principal Components Analysis  主成分分析
        5.8.2 K-means Clustering  K-均值聚类
    5.9 Stochastic Gradient Descent  随机梯度下降
    5.10 Building a Machine Learning Algorithm  构建机器学习算法
    5.11 Challenges Motivating Deep Learning  促使深度学习发展的挑战
        5.11.1 The Curse of Dimensionality  维度灾难
        5.11.2 Local Constancy and Smoothness Regularization  局部不变性与平滑正则化
        5.11.3 Manifold Learning  流形学习
    
### *<font color="#0000CC">Deep Networks: Modern Practices</font>*
#### 6. Deep Feedforward Networks
    6.1 Example: Learning XOR  实例：学习XOR
    6.2 Gradient-Based Learning  基于梯度的学习
        6.2.1 Cost Function  代价函数
            6.2.1.1 Learning Conditional Distributions with Maximum Likelihood  使用最大似然学习条件分布
            6.2.1.2 Learning Conditional Statistics  学习条件统计量
        6.2.2 Output Units  输出单元
            6.2.2.1 Linear Units for Gaussian Output Distributions  用于高斯输出分布的线性单元
            6.2.2.2 Sigmoid Units for Bernoulli Output Distributions  用于伯努利输出分布的sigmoid单元
            6.2.2.3 Softmax Units for Multinoulli Output Distributions  用于Multinoulli输出分布的softmax单元
            6.2.2.4 Other Output Types  其他的输出类型
    6.3 Hidden Units  隐藏单元
        6.3.1 Rectified Linear Units and Their Generalizations  整流线性单元及其拓展
        6.3.2 Logistic Sigmoid and Hyperbolic Tangent  逻辑S函数与双曲正切函数
        6.3.3 Other Hidden Units  其他隐藏单元
    6.4 Architecture Design  架构设计
        6.4.1 Universal Approximation Properties and Depth  万能近似性质和深度
        6.4.2 Other Architectural Considerations  其他架构上的考虑
    6.5 Back-Propagation and Other Differentiation Algorithms  反向传播和其他的微分算法
        6.5.1 Computational Graphs  计算图
        6.5.2 Chain Rule of Calculus  微积分中的链式法则
        6.5.3 Recursively Applying the Chain Rule to Obtain Backprop  递归地使用链式法则来实现反向传播
        6.5.4 Back-Propagation Computation in Fully-Connected MLP 全连接MLP中的反向传播
        6.5.5 Symbol-to-Symbol Derivatives  符号到符号的导数
        6.5.6 General Back-Propagation  一般化的反向传播
        6.5.7 Example: Back-Propagation for MLP Training  实例：用于MLP训练的反向传播
        6.5.8 Complications  复杂化
        6.5.9 Differentiation outside the Deep Learning Community  深度学习界以外的微分
        6.5.10 Higher-Order Derivatives  高阶微分
    6.6 Historical Notes  发展历史
    
#### 7. Regularization for Deep Learning
    7.1 Parameter Norm Penalties  参数范数惩罚
        7.1.1 L2 Parameter Regularization  L2参数正则化
        7.1.2 L1 Regularization  L1参数正则化
    7.2 Norm Penalties as Constrained Optimization  作为约束优化的范数惩罚
    7.3 Regularization and Under-Constrained Problems  正则化与欠约束问题
    7.4 Dataset Augmentation  数据集增强
    7.5 Noise Robustness  噪声鲁棒性
        7.5.1 Injecting Noise at the Output Targets  向输出目标注入噪声
    7.6 Semi-Supervised Learning  半监督学习
    7.7 Multitask Learning  多任务学习
    7.8 Early Stopping  提前终止
    7.9 Parameter Tying and Parameter Sharing  参数绑定与参数共享
    7.10 Sparse Representations  稀疏表示
    7.11 Bagging and Other Ensemble Methods Bagging与其他集成方法
    7.12 Dropout  
    7.13 Adversarial Training  对抗训练
    7.14 Tangent Distance, Tangent Prop and Manifold Tangent Classifier  切面距离、正切传播与流形正切分类器
    
#### 8. Optimization for Training Deep Models
    8.1 How Learning Differs from Pure Optimization  学习与纯优化的不同
        8.1.1 Empirical Risk Minimization  经验风险最小化
        8.1.2 Surrogate Loss Functions and Early Stopping  代理损失函数与提前终止
        8.1.3 Batch and Minibatch Algorithms  批量与小批量算法
    8.2 Challenges in Neural Network Optimization  神经网络中的挑战
        8.2.1 Ill-Conditioning  病态
        8.2.2 Local Minima  局部最小化
        8.2.3 Plateaus, Saddle Points and Other Flat Regions  高原、鞍点与其他平坦区域
        8.2.4 Cliffs and Exploding Gradients  悬崖与梯度爆炸
        8.2.5 Long-Term Dependencies  长期依赖
        8.2.6 Inexact Gradients  非精度梯度
        8.2.7 Poor Correspondence between Local and Global Structure  局部与全局结构间的弱对应
        8.2.8 Theoretical Limits of Opmization  优化的理论限制
    8.3 Basic Algorithms  基本算法
        8.3.1 Stochastic Gradient Descent  随机梯度下降
        8.3.2 Momentum  动量
        8.3.3 Nesterov Momentum  Nesterov动量
    8.4 Parameter Initialization Strategies  参数初始化策略
    8.5 Algorithms with Adaptive Learning Rates  自适应学习率算法
        8.5.1 AdaGrad  
        8.5.2 RMSProp
        8.5.3 Adam
        8.5.4 Choosing the Right Optimization Algorithm  选择正确的优化算法
    8.6 Approximate Second-Order Methods  二阶近似方法
        8.6.1 Newton's Method  牛顿法
        8.6.2 Conjugate Gradients  共轭梯度
        8.6.3 BFGS
    8.7 Optimization Strategies and Meta-Algorithms  优化策略与元算法
        8.7.1 Batch Normalization  批标准化
        8.7.2 Corrdinate Descent  坐标下降
        8.7.3 Polyak Averaging  Polyak平均
        8.7.4 Supervised Pretraining  监督预训练
        8.7.5 Designing Models to Aid Optimization  设计有助于优化的模型
        8.7.6 Continuation Methods and Curriculum Learning  延拓法与课程学习

#### 9. Convolutional Networks
    9.1 The Convolution Operation


```python

```
