
import pandas as pd;
from sklearn.preprocessing import StandardScaler;

def getDfFromPath(duongDanCsv : str) :
    df = pd.read_csv(duongDanCsv)

    return df;
#

def convertVfdfToZsdf(vfdf :pd.DataFrame) :

    vfdf_ColumnChuaSo = vfdf.select_dtypes(include="number").columns
    vfdf_ColumnChuaChu = vfdf.select_dtypes(include= "object").columns

    scaler1= StandardScaler()
    vfdf_z = pd.DataFrame(
        scaler1.fit_transform(vfdf[vfdf_ColumnChuaSo]), 
        columns= vfdf_ColumnChuaSo
    )

    df_Zs = pd.concat(
        [
            vfdf[vfdf_ColumnChuaChu],
            vfdf_z
        ],
        axis= 1
    )

    return df_Zs
#

def convertVfFileToZsFile(duongDanCsvFeature :str, duongDanCsvZscore : str) :
    dfVectorFeature = getDfFromPath(duongDanCsv= duongDanCsvFeature)

    df_Zs = convertVfdfToZsdf(vfdf= dfVectorFeature);

    df_Zs.to_csv(duongDanCsvZscore, index= False)
#