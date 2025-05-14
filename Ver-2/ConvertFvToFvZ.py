

import AudioInfo
import pandas as pd

def getMeanStdDf(duongDanCsvMeanStd :str) :
    dfFv_MeanStd = pd.read_csv(filepath_or_buffer= duongDanCsvMeanStd)

    return dfFv_MeanStd;
#

def convertFvToFvZ(dfFvRow :pd.DataFrame, dfFv_MeanStd :pd.DataFrame) :

    dfFvRow_Z= dfFvRow.copy()

    for column1 in dfFvRow_Z.select_dtypes(include= "number").columns :
        mean = dfFv_MeanStd.loc[ dfFv_MeanStd['column_name']== str(column1), 'mean_value'].values[0]

        std = dfFv_MeanStd.loc[ dfFv_MeanStd['column_name']== str(column1), 'std_value'].values[0]

        value = dfFvRow_Z[column1]

        value = (value- mean)/std

        dfFvRow_Z[str(column1)]= value
    #

    return dfFvRow_Z;
#

    

"""
ChatGPT đã nói:
Để duyệt qua mọi cột và mọi dòng trong DataFrame, bạn có thể sử dụng một số phương pháp khác nhau trong pandas. Dưới đây là một số cách phổ biến:

1. Duyệt qua từng dòng (row) bằng iterrows():
Phương thức iterrows() giúp duyệt qua từng dòng của DataFrame, trả về chỉ mục của dòng và nội dung của dòng đó dưới dạng một Series.

python
Sao chép mã
import pandas as pd

# Tạo DataFrame mẫu
data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
df = pd.DataFrame(data)

# Duyệt qua từng dòng
for index, row in df.iterrows():
    print(f"Row index: {index}")
    for column in df.columns:
        print(f"Column: {column}, Value: {row[column]}")

        
2. Duyệt qua từng cột (column) bằng iteritems():
Nếu bạn chỉ muốn duyệt qua mỗi cột của DataFrame, bạn có thể sử dụng phương thức iteritems(). Phương thức này sẽ trả về tên cột và Series của cột đó.

python
Sao chép mã
# Duyệt qua từng cột
for column, series in df.iteritems():
    print(f"Column: {column}")
    for value in series:
        print(f"Value: {value}")
"""

"""
Để set giá trị cho một ô trong DataFrame khi đã biết row và column, bạn có thể sử dụng .at[] hoặc .iat[]. Cả hai đều là cách đơn giản và nhanh chóng để truy cập và thay đổi một giá trị trong một ô cụ thể.
"""

"""
clone = chỉ duyệt các cột số

    for column1 in dfFvRow_Z.select_dtypes(include= "number").columns :
        # ...
    #
"""