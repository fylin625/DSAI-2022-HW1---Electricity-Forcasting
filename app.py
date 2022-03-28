import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn.svm import SVR


#選擇春季的月份，包含 2019、2020、2021 年的 2~5 月 + 2022 年 1~3 月的 dataset 訓練 SVR 回歸模型，預測 2021/03/30 ~ 04/13 的備轉容量
    
def heatmap(train):
    #heatmap
    corr=train.corr()
    # The number of columns to be displayed in the heat map
    k = 5
    # Calculate for the top 5 columns with the highest correlation with operating reserve
    cols = corr.nlargest(k, 'operating reserve')['operating reserve'].index
    cm = np.corrcoef(train[cols].values.T) 
    # Font size of the heatmap
    sns.set(font_scale=1.25)
    # View in a heat map
    hm = sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, 
                     yticklabels=cols.values, xticklabels=cols.values)
    
    #觀察資料分布狀況，發現有些特徵存在較大的偏差值
    sns.set()
    cols = ['operating reserve', 'rate', 'sun','people','holiday']
    # cols = ['operating reserve', 'rate']
    sns.pairplot(train[cols],size=1.2)
   
    print(train.sort_values(by='rate',ascending=False))
    
    #將顯示前一筆最大的數據，並將其刪除，試圖減少偏差值
    train=train.drop(index=train.sort_values(by='rate',ascending=False)['date'][:10].index)
    train=train.drop(index=train.sort_values(by='sun',ascending=False)['date'][:40].index)
    train=train.drop(index=train.sort_values(by='people',ascending=False)['date'][:40].index)
        
    sns.set()
    cols = ['operating reserve', 'rate', 'sun','people','holiday']
    sns.pairplot(train[cols],size=1.2)
    plt.show()
    return train
    
def sub(pred):
    name = ['operating reserv(MW)']
    pred=pred.flatten('C')
    pred = pd.DataFrame(pred, columns=name)
    date = [['date'],['2022/3/30'],['2022/3/31'],['2022/4/1'],
            ['2022/4/2'],['2022/4/3'],['2022/4/4'],['2022/4/5'],
            ['2022/4/6'],['2022/4/7'],['2022/4/8'],['2022/4/9'],
            ['2022/4/10'],['2022/4/11'],['2022/4/12'],['2022/4/13']]

    name = date.pop(0)
    date_df = pd.DataFrame(date,columns=name)
    res = pd.concat([date_df,pred],axis = 1)
    res.to_csv(args.output,index=0)

def forecasting():
    #import data
    train = pd.read_csv(args.training)
    train_new = heatmap(train)

    #建立training dataset
    
    X = train_new[['rate', 'sun','people','holiday']]
    
    # X.copy().fillna(-1).reset_index(drop=True)
    Y = train_new[['operating reserve']]
    # Y = Y.reset_index(drop=True)
    Y = Y.values.reshape(-1,1)
    
    
    #Feature scaling
    scaler_x = StandardScaler()
    scaler_y = StandardScaler()

    train_x = scaler_x.fit_transform(X)
    train_y = scaler_y.fit_transform(Y)
    
    reg = SVR(kernel='poly', C=1e1, gamma=0.01)               
    reg.fit(train_x, train_y)

    
    test = pd.read_csv('test.csv', encoding= 'unicode_escape')
    test_y = test[['operating reserve']][30:60]
    pred_x = test[['rate', 'sun','people','holiday']][:30]
    pred_x = scaler_x.fit_transform(pred_x)
    pred = reg.predict(pred_x)
    pred = [pred]
    
    pred = scaler_y.inverse_transform(pred)
    pred=pred.flatten('C')
    print("RMSE:", np.sqrt(metrics.mean_squared_error(test_y, pred)))
    
    pred_x = test[['rate', 'sun','people','holiday']][:15]
    pred_x = scaler_x.fit_transform(pred_x)
    pred = reg.predict(pred_x)
    pred = [pred]
    pred = scaler_y.inverse_transform(pred)
    pred=pred.flatten('C')
    sub(pred)
    

#main
if __name__ =='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--training',
                        default='train.csv',
                        help='training')
    parser.add_argument('--output',
                        default='submission.csv',
                        help='prediction')
    args = parser.parse_args()
    forecasting()