
import TinhKhoangCachVector

import pandas as pd

class KetQuaWrapper :
    def __init__(self, duongDan :str, khoangCach :float):
        self.duongDan= duongDan
        self.khoangCach= khoangCach
    #

    def getDataFrame(self):
        ketQua1 = {}

        ketQua1['duongDan']= self.duongDan
        ketQua1['khoangCach']= self.khoangCach
        
        dfKetQua= pd.DataFrame([ketQua1])

        return dfKetQua;
    #
#

def taoDataFrameMoi() :
    duongDan1= []
    khoangCach1= []
    ketQuaTimKiem = pd.DataFrame(
        {
            'duongDan'      : duongDan1,
            'khoangCach'    : khoangCach1
        }
    )

    return ketQuaTimKiem;
#


def tinhKhoangCachMoiVector(duongDanCsvLuuKetQuaTimKiem :str, dfFv :pd.DataFrame, dfFvMeanStd :pd.DataFrame, dfFvFileTruyVan :pd.DataFrame) :
    ketQuaTimKiem = taoDataFrameMoi()

    for i in range(0, len(dfFv)):
        row= dfFv.iloc[i : (i+1)]

        duongDan1 = row['duongDan'].iloc[0]
        khoangCach1 = TinhKhoangCachVector.doKhoangCach2DfFv(
            dfFv1= row,
            dfFv2= dfFvFileTruyVan,
            dfFvMeanStd= dfFvMeanStd
        )
        df1RowKetQuaTimKiem = KetQuaWrapper(duongDan= duongDan1, khoangCach= khoangCach1).getDataFrame()

        ketQuaTimKiem = pd.concat(
            [ketQuaTimKiem, df1RowKetQuaTimKiem],
            ignore_index= True
        )
    #

    ketQuaTimKiem = ketQuaTimKiem.sort_values(by= ['khoangCach'], ascending= True)

    ketQuaTimKiem.to_csv(path_or_buf= duongDanCsvLuuKetQuaTimKiem, index= False, mode='w')

    return ketQuaTimKiem;
#


"""
Để duyệt mọi hàng của một DataFrame trong pandas, và mỗi hàng được coi như là một DataFrame riêng biệt (thay vì Series), 
bạn có thể làm như sau:

# Duyệt từng hàng dưới dạng DataFrame
for i in range(len(df)):
    row_df = df.iloc[i:i+1]  # slicing để giữ dạng DataFrame
    print(row_df)
    print("---")
"""