import numpy as np
from scipy import signal
from matplotlib import pyplot as plt
import soundfile as sf


def ov(data, samplerate, Fs, overlap):
    """オーバーラップ処理をする関数"""

    # フレーム数計算（全データ長Ts, フレーム周期Fc, フレームずらし幅x_ol）
    Ts = len(data) / samplerate
    Fc = Fs / samplerate
    x_ol = Fs * (1 - (overlap / 100))
    N = int((Ts - (Fc * (overlap / 100))) / (Fc * (1 - (overlap / 100))))

    array = []

    # データを抽出
    for i in range(N):
        ps = int(x_ol * i)
        array.append(data[ps:ps + Fs:1])
        final_time = (ps + Fs)/samplerate
        
    return array, N, final_time


def hanning(data_array, Fs, N_ave):
    """ハニング窓をかける関数（振幅補正係数計算付き）"""
    
    han = signal.windows.hann(Fs)
    acf = 1 / (sum(han) / Fs)

    # オーバーラップされた複数時間波形全てに窓関数をかける
    for i in range(N_ave):
        data_array[i] = data_array[i] * han

    return data_array, acf


def calc_fft(data_array, samplerate, Fs, N_ave, acf):
    """FFTする関数"""
    
    fft_array = []
    fft_axis = np.linspace(0, samplerate, Fs)

    # FFTをして配列に追加、窓関数補正値をかけ正規化を実施
    for i in range(N_ave):
        fft_array.append(acf * np.abs(np.fft.fft(data_array[i]) / (Fs / 2)))
    fft_array = np.array(fft_array)

    return fft_array, fft_axis


def plot(fft_array, samplerate, final_time):
    """グラフを描画する関数"""

    # グラフをオブジェクト指向で作成する
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    # データをプロットする
    im = ax1.imshow(fft_array,
                    vmin=0, vmax=80,
                    extent=[0, final_time, 0, samplerate],
                    aspect='auto',
                    cmap='jet')

    # カラーバーを設定する
    cbar = fig.colorbar(im)
    cbar.set_label('Amplitude[dB]')

    # 軸設定する
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Frequency [Hz]')

    # スケールの設定をする
    ax1.set_xlim(0, 3)
    ax1.set_ylim(0, 3000)

    # グラフを表示する
    plt.show()
    plt.close()


if __name__ == '__main__':
    """メイン"""
    
    # フレームサイズとオーバーラップ率でスペクトログラムの分解能を調整
    Fs = 4096
    overlap = 90

    # wavファイルを読み込み
    path = 'wav/kuchibue.wav'
    data, samplerate = sf.read(path)
    
    # ステレオのwavファイルだったらモノラルに変換
    if data.ndim == 2:
        data = data.mean(axis=1)

    # オーバーラップ抽出された時間波形配列
    time_array, N_ave, final_time = ov(data, samplerate, Fs, overlap)

    # ハニング窓関数
    time_array, acf = hanning(time_array, Fs, N_ave)

    # FFT
    fft_array, fft_axis = calc_fft(time_array, samplerate, Fs, N_ave, acf)

    # スペクトログラムで縦軸周波数、横軸時間にするためにデータを転置
    fft_array = fft_array.T

    # dB変換(dB基準値 0dB=20μPa)
    fft_array = 20 * np.log10(fft_array / 2e-5)

    # プロット
    plot(fft_array, samplerate, final_time)
