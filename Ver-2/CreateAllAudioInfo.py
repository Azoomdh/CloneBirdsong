
import os;
import AudioInfo;
import pandas as pd

def insertDfToCsv(df : pd.DataFrame, duongDanFileCsv : str):
    csvDaTonTai = os.path.exists(path= duongDanFileCsv)
    themHeaderVaoCsv = False
    
    if csvDaTonTai== True :
        themHeaderVaoCsv = False
    #
    else :
        themHeaderVaoCsv = True
    #

    df.to_csv(path_or_buf= duongDanFileCsv, index=False, mode= 'a', header= themHeaderVaoCsv)
#

def saveFeatureAudioToCsv(duongDanFileNhac : str, duongDanFileCsv : str) :
    # ...
    audioInfo1 = AudioInfo.AudioInfo(duongDan= duongDanFileNhac)

    dataframeAudio1 = audioInfo1.getVectorFeature()

    insertDfToCsv(df= dataframeAudio1, duongDanFileCsv= duongDanFileCsv);
#

def createAllAudio(duongDanThuMuc : str, duongDanFileCsv : str) :
    # file-birdsong\songs\songs
    for subdir, dirs, files in os.walk(duongDanThuMuc):
        for file in files :
            filepath = subdir + os.sep + file

            if filepath.endswith(".wav")== True :
                saveFeatureAudioToCsv(duongDanFileNhac= filepath, duongDanFileCsv= duongDanFileCsv)
            #

            else :
                continue
            #
        #
    #
#