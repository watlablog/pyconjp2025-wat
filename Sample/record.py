import pyaudio
import soundfile as sf
import numpy as np
from matplotlib import pyplot as plt


def record(index, samplerate, fs, duration):
    """録音する関数"""
    
    pa = pyaudio.PyAudio()

    # ストリームの開始
    data = []
    stream = pa.open(format=pyaudio.paInt16,
                     channels=1,
                     rate=samplerate,
                     input=True,
                     input_device_index=index,
                     frames_per_buffer=fs)

    # フレームサイズ毎に音声を録音していくループ
    for i in range(int(((duration * samplerate) / fs))):
        frame = stream.read(fs)
        data.append(frame)

    # ストリームの終了
    stream.stop_stream()
    stream.close()
    pa.terminate()

    # データをまとめる処理
    data = b"".join(data)

    # データをNumpy配列に変換/時間軸を作成
    data = np.frombuffer(data, dtype="int16") / float((np.power(2, 16) / 2) - 1)
    t = np.arange(0, fs * (i + 1) * (1 / samplerate), 1 / samplerate)

    return data, t


def plot(t, data):
    """波形を確認する関数"""
    
    # フォントの種類とサイズを設定する。
    plt.rcParams['font.size'] = 14
    plt.rcParams['font.family'] = 'Times New Roman'

    # 目盛を内側にする。
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'

    # グラフの上下左右に目盛線を付ける。
    fig = plt.figure()
    ax= fig.add_subplot(111)
    ax.yaxis.set_ticks_position('both')
    ax.xaxis.set_ticks_position('both')

    # 軸のラベルを設定する。
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Amplitude')

    # データプロット。
    ax.plot(t, data, label='Time waveform', lw=1, color='red')

    # レイアウト設定
    fig.tight_layout()

    # グラフを表示する。
    plt.show()
    plt.close()
    
    return


if __name__ == '__main__':
    """メイン"""
    
    # 計測条件を設定
    time = 5
    samplerate = 44100
    fs = 1024
    index = 2

    # 録音する関数を実行
    data, t = record(index, samplerate, fs, time)
    
    # 波形を確認する
    plot(t, data)

    # wavファイルに保存する
    filename = 'wav/recorded.wav'
    sf.write(filename, data, samplerate)
