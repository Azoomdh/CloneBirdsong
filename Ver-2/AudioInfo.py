
import numpy as np;
import librosa;
import librosa.display;
import matplotlib.pyplot as plt;
import IPython.display as ipd;
from scipy.io import wavfile;
import pandas as pd;

class ConfigAudio :
    def __init__(self, chieuRongPlot, chieuCaoPlot, hop_length, frame_length, n_mfcc, n_chroma) :
        self.chieuRongPlot = chieuRongPlot
        self.chieuCaoPlot = chieuCaoPlot
        self.hop_length = hop_length
        self.frame_length = frame_length
        self.n_mfcc= n_mfcc
        self.n_chroma= n_chroma
    #
#

class AudioInfo :
    def __init__(self, duongDan):
        self.duongDan= duongDan;
        self.y , self.sr = librosa.load(self.duongDan);

        self.config = ConfigAudio(
            chieuRongPlot= 14, 
            chieuCaoPlot= 5, 
            hop_length=512, 
            frame_length= 2048,
            n_mfcc= 13,
            n_chroma= 12
        )
        
        self.zcrMean= None; 
        self.setZcr();
        
        self.specCentMean = None; 
        self.setSpecCent();
    
        self.specRolloffMean = None;
        self.setSpecRolloff();
    
        self.listMfccMean = []
        self.setListMfcc()

        self.listChromaMean = []
        self.setListChroma()
    #

    def createNullPlot(self):
        fig, ax= plt.subplots(figsize=(self.config.chieuRongPlot, self.config.chieuCaoPlot));
        return fig, ax;
    #

    def hienThiFile(self):
        ipd.display( ipd.Audio(self.y, self.sr)); # 🟩 cái này chỉ là in dòng lệnh, chưa phải là return mp3
    #

    def getDangSongPlot(self):
        fig, ax = self.createNullPlot();
        
        librosa.display.waveshow(self.y, sr=self.sr, ax=ax );
        
        ax.set_title("audio wave show");
        ax.set_xlabel("time");
        ax.set_ylabel("biên độ");
    
        return fig;
    #

    def getSpectrogramPlot(self):
        D = librosa.stft(self.y); # Stft của y
        S_db = librosa.amplitude_to_db( np.abs(D), ref= np.max) # convert to deci ben

        # hien thi
        fig, ax = self.createNullPlot();

        librosa.display.specshow(
            S_db, 
            sr= self.sr, 
            x_axis="time", 
            y_axis="Hz (hezt)", 
            ax= ax
        );
        
        fig.colorbar(format="%+2.0f dB");
        ax.set_title("spectrogram");
        
        return fig;
    #

    def getMelSpectrogramPlot(self):
        S = librosa.feature.melspectrogram(y= self.y, sr= self.sr, n_mels= 128);
        S_db_mel = librosa.power_to_db(S, ref= np.max);

        fig, ax = self.createNullPlot();

        librosa.display.specshow(
            S_db_mel, 
            sr= self.sr, 
            x_axis="time", 
            y_axis= "thang mel"
        );
        
        fig.colorbar(format= "%+2.0f dB");

        ax.set_title("Mel spectrogram");

        return fig
    #

    #🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩

    def getZcrAllTime(self):
        return librosa.feature.zero_crossing_rate(
            self.y, 
            frame_length= self.config.frame_length, 
            hop_length= self.config.hop_length
        );
    #

    def setZcr(self):
        zcrAllTime= self.getZcrAllTime();
        self.zcrMean = np.mean(zcrAllTime);
    #

    def getZcrPlot(self):
        zcrAllTime= self.getZcrAllTime();
    
        fig, ax= self.createNullPlot();

        times = librosa.times_like(zcrAllTime, sr= self.sr, hop_length= self.config.hop_length);

        ax.plot(times, zcrAllTime[0]);
        ax.set_title("zero crossing rate")
        ax.set_xlabel("time (giây)")
        ax.set_ylabel("zero crossing rate")

        return fig;
    #

    #🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩

    #🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥

    def getSpecCentAllTime(self):
        return librosa.feature.spectral_centroid(
            y= self.y,
            sr= self.sr,
            hop_length= self.config.hop_length
        );
    #

    def setSpecCent(self):
        specCentAllTime= self.getSpecCentAllTime();
        self.specCentMean = np.mean(specCentAllTime);
    #

    def getSpecCentPlot(self):
        specCentAllTime= self.getSpecCentAllTime();

        fig, ax= self.createNullPlot();

        times = librosa.times_like(
            specCentAllTime, 
            sr= self.sr, 
            hop_length= self.config.hop_length
        )

        #semilogy = trục Oy là hàm log = semi-log-y
        ax.semilogy(
            times,
            specCentAllTime[0],
            label= 'spectral centroid'
        )

        ax.set_ylabel("Hz")
        ax.set_xlabel("Time")
        ax.legend(); #là cái ô chú thích "đường màu xanh là tâm phổ"
        ax.set_title("spectral centroid")

        return fig;
    #

    #🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥

    #🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩

    def getSpecRolloffAllTime(self):
        return librosa.feature.spectral_rolloff(
            y= self.y,
            sr= self.sr,
            hop_length= self.config.hop_length
        );
    #

    def setSpecRolloff(self):
        specRolloffAllTime = self.getSpecRolloffAllTime()

        self.specRolloffMean = np.mean(specRolloffAllTime);
    #

    def getSpecRolloffPlot(self):
        specRolloffAllTime = self.getSpecRolloffAllTime();

        fig, ax = self.createNullPlot()

        times = librosa.times_like(
            specRolloffAllTime, 
            sr= self.sr, 
            hop_length= self.config.hop_length
        )

        ax.semilogy(
            times,
            specRolloffAllTime[0],
            label= "spectral roll off"
        )

        ax.set_ylabel("Hz")
        ax.set_xlabel("Time")
        ax.set_title("spectral roll off")

        return fig;
    #

    #🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩


    #🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥

    def getListMfccAllTime(self):
        return librosa.feature.mfcc(
            y= self.y,
            sr= self.sr,
            n_mfcc = self.config.n_mfcc
        );
    #

    def setListMfcc(self):
        listMfccAllTime = self.getListMfccAllTime()

        self.listMfccMean = np.mean(listMfccAllTime, axis=1)
    #

    def getListMfccPlot(self):
        listMfccAllTime = self.getListMfccAllTime()

        fig, ax = self.createNullPlot()

        librosa.display.specshow(
            listMfccAllTime,
            sr= self.sr,
            x_axis= 'time',
            ax= ax
        )

        fig.colorbar(format= "%+2.0f dB")

        ax.set_title("mfcc")

        return fig;
    #

    #🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥

    #🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩

    def getListChromaAllTime(self):
        return librosa.feature.chroma_stft(
            y= self.y,
            sr= self.sr,
            n_chroma= self.config.n_chroma
        );
    #

    def setListChroma(self):
        listChromaAllTime = self.getListChromaAllTime();
        self.listChromaMean = np.mean(listChromaAllTime, axis=1);
    #

    def getListChromaPlot(self):
        listChromaAllTime = self.getListChromaAllTime()

        fig, ax = self.createNullPlot()

        librosa.display.specshow(
            listChromaAllTime,
            sr= self.sr,
            x_axis= "time",
            y_axis= "chroma",
            ax= ax
        )

        fig.colorbar()

        ax.set_title("chromagram")

        return fig;
    #
    #🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩

    #🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥

    def getVectorFeature(self):
        vectorFeature = {}

        vectorFeature['zcrMean']= self.zcrMean

        vectorFeature['specCenMean']= self.specCentMean

        vectorFeature['specRolloffMean']= self.specRolloffMean

        # mfcc[0] -> mfcc[12]
        # https://www.geeksforgeeks.org/enumerate-in-python/
        for i, mfccMean in enumerate(self.listMfccMean):
            tenMfcc = f"mfcc_{i}_Mean"
            vectorFeature[tenMfcc] = mfccMean
        #

        # chroma[0] -> chroma[11]
        for i, chromaMean in enumerate(self.listChromaMean):
            tenChroma = f"chroma_{i}_Mean"
            vectorFeature[tenChroma] = chromaMean
        #

        df1 = pd.DataFrame([vectorFeature])

        return df1;
    #

    #🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥
#