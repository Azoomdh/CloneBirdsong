
import numpy as np;
import librosa;
import librosa.display;
import matplotlib.pyplot as plt;
import IPython.display as ipd;
from scipy.io import wavfile;
import pandas as pd;

class ConfigAudio :
    def __init__(self, chieuRongPlot, chieuCaoPlot, hop_length, frame_length) :
        self.chieuRongPlot = chieuRongPlot
        self.chieuCaoPlot = chieuCaoPlot
        self.hop_length = hop_length
        self.frame_length = frame_length
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
            frame_length= 2048 
        );
        
        self.zcrMean= None; 
        self.setZcr();
        
        self.tamPhoMean = None; 
        self.setTamPho();
    
        self.specRolloffMean = None;
        self.setSpecRolloff();
    
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

    def getTamPhoAllTime(self):
        return librosa.feature.spectral_centroid(
            y= self.y,
            sr= self.sr,
            hop_length= self.config.hop_length
        );
    #

    def setTamPho(self):
        tamPhoAllTime= self.getTamPhoAllTime();
        self.tamPhoMean = np.mean(tamPhoAllTime);
    #

    def getTamPhoPlot(self):
        tamPhoAllTime= self.getTamPhoAllTime();

        fig, ax= self.createNullPlot();

        times = librosa.times_like(
            tamPhoAllTime, 
            sr= self.sr, 
            hop_length= self.config.hop_length
        )

        #semilogy = trục Oy là hàm log= semi-log-y
        ax.semilogy(
            times,
            tamPhoAllTime[0],
            label= 'tâm phổ',
        )

        ax.set_ylabel("Hz")
        ax.set_xlabel("Time")
        ax.legend(); #là cái ô chú thích "đường màu xanh là tâm phổ"
        ax.set_title("Tâm phổ")

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

    def getMfccAllTime(self):
        return 

    #🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥
#