# DSAI2022_HW1-Electricity-Forcasting
NCKU DSAI HW1 - Electricity Forecasting
選擇台電提供過去的2019、2020、2021年的"1至3月"的發電量資訊包含淨尖峰供電能力、淨尖峰用電量、民生用電、工業用電等.. 並使用"       "迴歸模型，預測2022/03/30~2022/04/13的備轉容量(MW)。

## Data analysis
使用heatmap尋找與operating reserve關聯度較高的特徵

![GITHUB]()

## Feature selection
從heatmap中選擇"備轉容量率(%)、麥寮第二發電廠與通霄發電廠"作為訓練的特徵

## Data pre-processing
將這些關聯度高的特徵中，刪除"2"筆在訓練資料集中偏差較大的數值

![GITHUB]()

![GITHUB]()

## Model training
這此使用的是scikit-learn中的SVR model，此model設有5種kernel包含linear, poly, rbf, sigmoid, precomputed。 本次模型參數設定為kernel=poly，Kernel coefficient也就是gamma=0.1、C=1e1。 將2019年、2020年1月~3月的資料作為training data,並將資料做Standard Scaler輸入至SVR模型中。

## Run the code

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
