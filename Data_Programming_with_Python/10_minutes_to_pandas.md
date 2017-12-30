
<img src="http://blog.welcomege.com/wp-content/uploads/2017/07/jupyter.png"
style="width:120px;height:30px;float:right">

# Pandas Tutorial

Created on 29/12/2017, Fan Li


```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

## 创建对象

**Series 是一个值的序列，它只有一个列，以及索引。下面的例子中，就用默认的整数索引**


```python
s = pd.Series([1,3,5,np.nan,6,8])
```


```python
s
```




    0    1.0
    1    3.0
    2    5.0
    3    NaN
    4    6.0
    5    8.0
    dtype: float64



**DataFrame 是有多个列的数据表，每个列拥有一个 label，当然，DataFrame 也有索引**


```python
dates = pd.date_range('20180101', periods=6)
```


```python
dates
```




    DatetimeIndex(['2018-01-01', '2018-01-02', '2018-01-03', '2018-01-04',
                   '2018-01-05', '2018-01-06'],
                  dtype='datetime64[ns]', freq='D')




```python
df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
```


```python
df
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2018-01-01</th>
      <td>-0.840159</td>
      <td>0.919306</td>
      <td>-0.425277</td>
      <td>-0.284685</td>
    </tr>
    <tr>
      <th>2018-01-02</th>
      <td>0.389555</td>
      <td>-0.703242</td>
      <td>0.880569</td>
      <td>-0.948373</td>
    </tr>
    <tr>
      <th>2018-01-03</th>
      <td>0.053589</td>
      <td>0.899564</td>
      <td>0.665736</td>
      <td>-2.184503</td>
    </tr>
    <tr>
      <th>2018-01-04</th>
      <td>2.327503</td>
      <td>-0.565789</td>
      <td>-0.274481</td>
      <td>-1.172040</td>
    </tr>
    <tr>
      <th>2018-01-05</th>
      <td>-0.447019</td>
      <td>2.166920</td>
      <td>0.385466</td>
      <td>-1.546954</td>
    </tr>
    <tr>
      <th>2018-01-06</th>
      <td>-1.927569</td>
      <td>-1.023112</td>
      <td>0.407856</td>
      <td>-1.292750</td>
    </tr>
  </tbody>
</table>
</div>



**如果参数是一个 dict，每个 dict 的 value 会被转化成一个 Series**


```python
df2 = pd.DataFrame({
    'A' : 1.,
    'B' : pd.Timestamp('20180102'),
    'C' : pd.Series(1, index=list(range(4)), dtype='float32'),
    'D' : np.array([3]*4, dtype="int32"),
    'E' : pd.Categorical(["test", "train", "test", "train"]),
    'F' : 'Fan'
})
```


```python
df2
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
      <th>E</th>
      <th>F</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1.0</td>
      <td>2018-01-02</td>
      <td>1.0</td>
      <td>3</td>
      <td>test</td>
      <td>Fan</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1.0</td>
      <td>2018-01-02</td>
      <td>1.0</td>
      <td>3</td>
      <td>train</td>
      <td>Fan</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1.0</td>
      <td>2018-01-02</td>
      <td>1.0</td>
      <td>3</td>
      <td>test</td>
      <td>Fan</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1.0</td>
      <td>2018-01-02</td>
      <td>1.0</td>
      <td>3</td>
      <td>train</td>
      <td>Fan</td>
    </tr>
  </tbody>
</table>
</div>



**每列的格式用 dtypes 查看**


```python
df2.dtypes
```




    A           float64
    B    datetime64[ns]
    C           float32
    D             int32
    E          category
    F            object
    dtype: object



**可以理解为‘DataFrame 是由 Series 组成的’**


```python
df2.A
```




    0    1.0
    1    1.0
    2    1.0
    3    1.0
    Name: A, dtype: float64




```python
df2.B
```




    0   2018-01-02
    1   2018-01-02
    2   2018-01-02
    3   2018-01-02
    Name: B, dtype: datetime64[ns]



## 查看数据

**用head和tail查看顶端和底端的几列**


```python
df.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2018-01-01</th>
      <td>-0.840159</td>
      <td>0.919306</td>
      <td>-0.425277</td>
      <td>-0.284685</td>
    </tr>
    <tr>
      <th>2018-01-02</th>
      <td>0.389555</td>
      <td>-0.703242</td>
      <td>0.880569</td>
      <td>-0.948373</td>
    </tr>
    <tr>
      <th>2018-01-03</th>
      <td>0.053589</td>
      <td>0.899564</td>
      <td>0.665736</td>
      <td>-2.184503</td>
    </tr>
    <tr>
      <th>2018-01-04</th>
      <td>2.327503</td>
      <td>-0.565789</td>
      <td>-0.274481</td>
      <td>-1.172040</td>
    </tr>
    <tr>
      <th>2018-01-05</th>
      <td>-0.447019</td>
      <td>2.166920</td>
      <td>0.385466</td>
      <td>-1.546954</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.tail(3)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2018-01-04</th>
      <td>2.327503</td>
      <td>-0.565789</td>
      <td>-0.274481</td>
      <td>-1.172040</td>
    </tr>
    <tr>
      <th>2018-01-05</th>
      <td>-0.447019</td>
      <td>2.166920</td>
      <td>0.385466</td>
      <td>-1.546954</td>
    </tr>
    <tr>
      <th>2018-01-06</th>
      <td>-1.927569</td>
      <td>-1.023112</td>
      <td>0.407856</td>
      <td>-1.292750</td>
    </tr>
  </tbody>
</table>
</div>



**实际上，DataFrame 内部用 numpy 格式存储数据。你也可以单独查看 index 和 columns**


```python
df.index
```




    DatetimeIndex(['2018-01-01', '2018-01-02', '2018-01-03', '2018-01-04',
                   '2018-01-05', '2018-01-06'],
                  dtype='datetime64[ns]', freq='D')




```python
df.columns
```




    Index(['A', 'B', 'C', 'D'], dtype='object')




```python
df.values
```




    array([[-0.84015939,  0.91930594, -0.42527729, -0.28468528],
           [ 0.38955499, -0.70324159,  0.8805686 , -0.94837273],
           [ 0.05358902,  0.89956369,  0.66573647, -2.18450302],
           [ 2.32750259, -0.56578856, -0.27448112, -1.17204047],
           [-0.44701914,  2.1669201 ,  0.38546628, -1.5469544 ],
           [-1.92756927, -1.02311198,  0.40785571, -1.29275047]])



**describe() 显示数据的概要 [count, means, (min, q1, median, q3, max)]**


```python
df.describe()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>6.000000</td>
      <td>6.000000</td>
      <td>6.000000</td>
      <td>6.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>-0.074017</td>
      <td>0.282275</td>
      <td>0.273311</td>
      <td>-1.238218</td>
    </tr>
    <tr>
      <th>std</th>
      <td>1.425499</td>
      <td>1.243642</td>
      <td>0.517985</td>
      <td>0.631088</td>
    </tr>
    <tr>
      <th>min</th>
      <td>-1.927569</td>
      <td>-1.023112</td>
      <td>-0.425277</td>
      <td>-2.184503</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>-0.741874</td>
      <td>-0.668878</td>
      <td>-0.109494</td>
      <td>-1.483403</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>-0.196715</td>
      <td>0.166888</td>
      <td>0.396661</td>
      <td>-1.232395</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>0.305563</td>
      <td>0.914370</td>
      <td>0.601266</td>
      <td>-1.004290</td>
    </tr>
    <tr>
      <th>max</th>
      <td>2.327503</td>
      <td>2.166920</td>
      <td>0.880569</td>
      <td>-0.284685</td>
    </tr>
  </tbody>
</table>
</div>



**和 numpy 一样，可以方便的得到转置**


```python
df.T
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>2018-01-01 00:00:00</th>
      <th>2018-01-02 00:00:00</th>
      <th>2018-01-03 00:00:00</th>
      <th>2018-01-04 00:00:00</th>
      <th>2018-01-05 00:00:00</th>
      <th>2018-01-06 00:00:00</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>A</th>
      <td>-0.840159</td>
      <td>0.389555</td>
      <td>0.053589</td>
      <td>2.327503</td>
      <td>-0.447019</td>
      <td>-1.927569</td>
    </tr>
    <tr>
      <th>B</th>
      <td>0.919306</td>
      <td>-0.703242</td>
      <td>0.899564</td>
      <td>-0.565789</td>
      <td>2.166920</td>
      <td>-1.023112</td>
    </tr>
    <tr>
      <th>C</th>
      <td>-0.425277</td>
      <td>0.880569</td>
      <td>0.665736</td>
      <td>-0.274481</td>
      <td>0.385466</td>
      <td>0.407856</td>
    </tr>
    <tr>
      <th>D</th>
      <td>-0.284685</td>
      <td>-0.948373</td>
      <td>-2.184503</td>
      <td>-1.172040</td>
      <td>-1.546954</td>
      <td>-1.292750</td>
    </tr>
  </tbody>
</table>
</div>



**对 axis 按照 index 排序（axis=1 是指第二个维度，即：列; ascending = False 即：降序）**


```python
df.sort_index(axis=1, ascending=False)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>D</th>
      <th>C</th>
      <th>B</th>
      <th>A</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2018-01-01</th>
      <td>-0.284685</td>
      <td>-0.425277</td>
      <td>0.919306</td>
      <td>-0.840159</td>
    </tr>
    <tr>
      <th>2018-01-02</th>
      <td>-0.948373</td>
      <td>0.880569</td>
      <td>-0.703242</td>
      <td>0.389555</td>
    </tr>
    <tr>
      <th>2018-01-03</th>
      <td>-2.184503</td>
      <td>0.665736</td>
      <td>0.899564</td>
      <td>0.053589</td>
    </tr>
    <tr>
      <th>2018-01-04</th>
      <td>-1.172040</td>
      <td>-0.274481</td>
      <td>-0.565789</td>
      <td>2.327503</td>
    </tr>
    <tr>
      <th>2018-01-05</th>
      <td>-1.546954</td>
      <td>0.385466</td>
      <td>2.166920</td>
      <td>-0.447019</td>
    </tr>
    <tr>
      <th>2018-01-06</th>
      <td>-1.292750</td>
      <td>0.407856</td>
      <td>-1.023112</td>
      <td>-1.927569</td>
    </tr>
  </tbody>
</table>
</div>



**按指定值(某行某列)排序**


```python
df.sort_values(by='B')
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2018-01-06</th>
      <td>-1.927569</td>
      <td>-1.023112</td>
      <td>0.407856</td>
      <td>-1.292750</td>
    </tr>
    <tr>
      <th>2018-01-02</th>
      <td>0.389555</td>
      <td>-0.703242</td>
      <td>0.880569</td>
      <td>-0.948373</td>
    </tr>
    <tr>
      <th>2018-01-04</th>
      <td>2.327503</td>
      <td>-0.565789</td>
      <td>-0.274481</td>
      <td>-1.172040</td>
    </tr>
    <tr>
      <th>2018-01-03</th>
      <td>0.053589</td>
      <td>0.899564</td>
      <td>0.665736</td>
      <td>-2.184503</td>
    </tr>
    <tr>
      <th>2018-01-01</th>
      <td>-0.840159</td>
      <td>0.919306</td>
      <td>-0.425277</td>
      <td>-0.284685</td>
    </tr>
    <tr>
      <th>2018-01-05</th>
      <td>-0.447019</td>
      <td>2.166920</td>
      <td>0.385466</td>
      <td>-1.546954</td>
    </tr>
  </tbody>
</table>
</div>




```python

```


```python

```


```python

```


```python

```


```python

```


```python

```


```python

```


```python

```


```python

```


```python

```


```python

```
