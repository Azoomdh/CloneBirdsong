
import pandas as pd;

def convertDfToMean(dfVf :pd.DataFrame) :
    # Để chọn các cột không phải là kiểu số trong một DataFrame (df), bạn dùng: 🟥 df.select_dtypes(exclude='number')
    dfVf_ChuaSo = dfVf.select_dtypes(include= "number")

    dfVf_ChuaSo_Mean = dfVf_ChuaSo.mean().reset_index();

    dfVf_ChuaSo_Mean.columns = ['column_name', 'mean_value']
    
    return dfVf_ChuaSo_Mean;
#

# def saveMeanFromDf(dfVf :pd.DataFrame, duongDanCsvFvMean :str) :
#     dfVf_Mean = convertDfToMean(dfVf= dfVf)

#     dfVf_Mean.to_csv(path_or_buf= duongDanCsvFvMean)
# #

def convertDfToStd(dfVf :pd.DataFrame) :
    dfVf_ChuaSo = dfVf.select_dtypes(include= "number")

    dfVf_ChuaSo_Std = dfVf_ChuaSo.std().reset_index()

    dfVf_ChuaSo_Std.columns = ['column_name', 'std_value']

    return dfVf_ChuaSo_Std
#

# def saveStdFromDf(dfVf :pd.DataFrame, duongDanCsvFvStd :str) :
#     dfVf_Std = convertDfToStd(dfVf= dfVf)

#     dfVf_Std.to_csv(path_or_buf= duongDanCsvFvStd)
# #

def saveMeanVaStd(duongDanCsvFv :str, duongDanCsvFvMeanStd :str):
    dfVf = pd.read_csv(filepath_or_buffer= duongDanCsvFv)

    dfVf_Mean = convertDfToMean(dfVf= dfVf)
    dfVf_Std = convertDfToStd(dfVf= dfVf)

    dfVf_MeanStd = pd.merge(dfVf_Mean, dfVf_Std, on='column_name', how= 'inner')

    dfVf_MeanStd.to_csv(path_or_buf= duongDanCsvFvMeanStd, index= False)

    # saveMeanFromDf(dfVf, duongDanCsvFvMean)
    # saveStdFromDf(dfVf, duongDanCsvFvStd)
#

"""

Để nối hai DataFrame bằng một cột chung (ví dụ: 'column_name'), bạn có thể sử dụng phương thức merge() trong pandas. Đây là cách để thực hiện việc nối (merge) hai DataFrame theo một cột chung:

Giả sử bạn có hai DataFrame là df1 và df2, bạn có thể làm như sau:

python
Sao chép
Chỉnh sửa

import pandas as pd

# Ví dụ về hai DataFrame
df1 = pd.DataFrame({
    'column_name': [1, 2, 3],
    'A': ['a1', 'a2', 'a3']
})

df2 = pd.DataFrame({
    'column_name': [2, 3, 4],
    'B': ['b2', 'b3', 'b4']
})

# Nối hai DataFrame theo cột 'column_name'
df_merged = pd.merge(df1, df2, on='column_name', how='inner')

# Kết quả
print(df_merged)
Ở đây:

on='column_name': chỉ định cột nào để nối.

how='inner': loại nối sẽ được thực hiện (bạn có thể thay đổi giá trị how thành 'left', 'right', hoặc 'outer' tùy theo yêu cầu của bạn).

Các kiểu nối (how):
'inner': Nối chỉ những giá trị chung trong cả hai DataFrame (mặc định).

'left': Lấy tất cả dữ liệu từ DataFrame bên trái và nối với dữ liệu từ DataFrame bên phải.

'right': Lấy tất cả dữ liệu từ DataFrame bên phải và nối với dữ liệu từ DataFrame bên trái.

'outer': Nối tất cả dữ liệu từ cả hai DataFrame, điền giá trị NaN cho các phần không có dữ liệu tương ứng.

Nếu bạn muốn tôi giải thích thêm về cách thức hoạt động của các kiểu nối này, hoặc có câu hỏi cụ thể nào khác, cứ thoải mái hỏi nhé!

"""