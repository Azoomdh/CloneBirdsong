
import ConvertFvToFvZ

import pandas as pd;
import numpy as np;
from scipy.spatial import distance


def doKhoangCach2DfFvZ(dfFvZ1 :pd.DataFrame, dfFvZ2 :pd.DataFrame):
    dfFvZ1_ChuaSo = dfFvZ1.select_dtypes(include= 'number').values[0]
    dfFvZ2_ChuaSo = dfFvZ2.select_dtypes(include= 'number').values[0]

    khoangCach= distance.euclidean(dfFvZ1_ChuaSo, dfFvZ2_ChuaSo)

    return khoangCach
#


def doKhoangCach2DfFv(dfFv1 :pd.DataFrame, dfFv2 :pd.DataFrame, dfFvMeanStd :pd.DataFrame) :
    dfFv1_Z = ConvertFvToFvZ.convertFvToFvZ(dfFvRow= dfFv1.iloc[[0]], dfFv_MeanStd= dfFvMeanStd)
    dfFv2_Z = ConvertFvToFvZ.convertFvToFvZ(dfFvRow= dfFv2.iloc[[0]], dfFv_MeanStd= dfFvMeanStd)

    khoangCach = doKhoangCach2DfFvZ(dfFvZ1= dfFv1_Z, dfFvZ2= dfFv2_Z)

    return khoangCach
#

"""
dfFvRow = dfFv2.iloc[[0]]
✅ Ý nghĩa:
Dòng này lấy dòng đầu tiên (vị trí 0) của DataFrame dfFv2 và giữ nguyên dạng là một DataFrame (không bị chuyển thành Series).

Vì bạn dùng dấu [[0]] (hai cặp ngoặc vuông), kết quả là một DataFrame một dòng, chứ không phải một Series.
"""


"""
Cách bạn viết gặp lỗi ValueError: Input vector should be 1-D trong dòng:

python
Sao chép mã
khoangCach= distance.euclidean(dfFvZ1_ChuaSo, dfFvZ2_ChuaSo)
❌ Lý do:
dfFvZ1_ChuaSo và dfFvZ2_ChuaSo là DataFrame một dòng, nên .values trả về mảng 2D có shape (1, 28) — và euclidean() cần 2 vector 1D.


✅ Cách sửa:
    dfFvZ1_ChuaSo = dfFvZ1.select_dtypes(include='number').values[0]
    dfFvZ2_ChuaSo = dfFvZ2.select_dtypes(include='number').values[0]
"""