# DSAI 2022 HW1 - Electricity-Forcasting
## Overview
### NCKU DSAI HW1 - Electricity Forecasting

根據台電提供過去電力的供需資訊，使用 Support Vector Regression 模型，預測 2022/03/30 - 2022/04/13 的電力備轉容量(MW)。

## Data
### Electricity
* 資料：台灣電力公司_過去電力供需資訊、台灣電力公司_本年度每日尖峰備轉容量率
* 時間：2019/01/01 - 2022/02/28（備轉容量至 2022/03/26）
* 說明：「台灣電力公司_過去電力供需資訊」包含淨尖峰供電能力、尖峰負載、備轉容量、備轉容量率、工業用電、民生用電等資訊；「台灣電力公司_本年度每日尖峰備轉容量率」僅包含日期、備轉容量、備轉容量率的資訊。


### Working Days
* 資料：中華民國政府行政機關辦公日曆表
* 時間：2019 - 2022
* 說明：紀錄台灣政府行政機關當日是否辦公，資料中包含西元日期、星期、是否放假（0：工作日；2：放假）。參考以下[論文](https://www.sciencedirect.com/science/article/pii/S2666792421000184?via%3Dihub)的 fig.8 可得知是否為工作日對於用電量有所影響。
> Wang, Z., Hong, T., Li, H. and Piette, M.A., 2021. Predicting City-Scale Daily Electricity Consumption Using Data-Driven Models. Advances in Applied Energy, p.100025.


### Training Data and Test Data
使用「台灣電力公司_過去電力供需資訊」中，2019 年至 2021 年二月至五月的資料加上工作日的資訊作為訓練資料，且使用 2022 年一月至二月以及「台灣電力公司_本年度每日尖峰備轉容量率」中三月的資料作為測試資料。


## Data Analysis
使用 heatmap 尋找與備轉容量 (operating reserve) 關聯度較高的特徵。

![GITHUB](https://github.com/fylin625/DSAI2022_HW1-Electricity-Forcasting/blob/main/images/heatmap.png)

## Feature Selection
從 heatmap 中選擇備轉容量率(%)、麥寮#2、林口#2、和平#1與民生用電作為訓練的特徵，並加入當日是否為工作日（holiday）的特徵。

## Data Preprocessing
將這些關聯度高的特徵中，依資料分布刪除 2 到 10 筆訓練資料中偏差較大的數值。
```
<script src="https://gist.github.com/fylin625/49fd49d27487579de846cde48517576e.js"></script>
```

### 資料處理前
![GITHUB](https://github.com/fylin625/DSAI2022_HW1-Electricity-Forcasting/blob/main/images/pairplot.png)

### 資料處理後
![GITHUB](https://github.com/fylin625/DSAI2022_HW1-Electricity-Forcasting/blob/main/images/pairplot_dropped.png)


## Model
在測試 LightGBM, XGBoost, 後，SVR 的 RMSE 相對其他模型較低，因此選擇使用 SVR 作為本次的模型。

Scikit-learn 中的 Support Vector Regression 模型，設有 5 種 kernel 包含 linear, poly, rbf, sigmoid, precomputed。

本模型參數設定為 kernel=poly，Kernel coefficient 也就是 gamma=0.01、C=1e1、epsilon=0。將訓練資料做 Standard Scaler 輸入至模型中。

## Run

環境 Python "3.7.1"

```
conda create -n elec_pred python=="3.7"
```
```
activate elec_pred
```
路徑移至 requirements.txt 所在的資料夾，輸入安裝套件指令
```
conda install --yes --file requirements.txt
```
將 app.py、train.csv、test.csv、submission.csv 下載至同資料夾內

輸入以下指令
```
python app.py --training train.csv --output submission.csv
```
## Result
[submission.csv](https://github.com/fylin625/DSAI2022_HW1-Electricity-Forcasting/blob/main/submission.csv)

