# DSAI 2022 HW1 - Electricity-Forcasting
## Overview
**NCKU DSAI HW1 - Electricity Forecasting**

根據台電提供過去電力的供需資訊，使用 Support Vector Regression 模型，預測 2022/03/30 ~ 2022/04/13 的電力備轉容量(MW)。

## Data
### 電力
* 資料：台灣電力公司_過去電力供需資訊、台灣電力公司_本年度每日尖峰備轉容量率
* 時間範圍：2019/01/01 - 2022/02/28（備轉容量至 2022/03/26）
* 說明：「台灣電力公司_過去電力供需資訊」包含淨尖峰供電能力、尖峰負載、備轉容量、備轉容量率、工業用電、民生用電等資訊；「台灣電力公司_本年度每日尖峰備轉容量率」僅包含日期、備轉容量、備轉容量率的資訊。

### 工作日
* 資料：中華民國政府行政機關辦公日曆表
* 時間範圍：2019 - 2022
* 說明：紀錄台灣政府行政機關當日是否辦公，資料中包含西元日期、星期、是否放假（0：工作日；2：放假）。

### 資料使用
使用「台灣電力公司_過去電力供需資訊」中，2019 年至 2021 年二月至五月的資料加上工作日的資訊作為訓練資料，且使用 2022 年一月至二月以及「台灣電力公司_本年度每日尖峰備轉容量率」中三月的資料作為測試資料。

## Data Analysis
使用 heatmap 尋找與備轉容量 (operating reserve) 關聯度較高的特徵。

![GITHUB]()

## Feature Selection
從 heatmap 中選擇備轉容量率(%)、民生用電與太陽能發電作為訓練的特徵，並加入當日是否為工作日（holiday）的特徵。

## Data Preprocessing
將這些關聯度高的特徵中，刪除 10 筆在訓練資料中偏差較大的數值。

![GITHUB]()

![GITHUB]()

## Model Training
模型使用的是 Scikit-learn 中的 Support Vector Regression 模型，此 model 設有 5 種 kernel 包含 linear, poly, rbf, sigmoid, precomputed。

本模型參數設定為kernel=poly，Kernel coefficient也就是gamma=0.1、C=1e1。 將訓練資料做Standard Scaler輸入至SVR模型中。

## Run

環境 Python "3.7.1"

```
conda create -n test python=="3.7"
```
```
activate test
```
路徑移至requirements.txt所在的資料夾，輸入安裝套件指令:
```
conda install --yes --file requirements.txt
```
將app.py、train.csv、test.csv、submission.csv載下後(需在同資料夾內)

輸入以下指令:
```
python app.py --training train.csv --output submission.csv
```
