import numpy as np
from matplotlib import pyplot as plt
import soundfile as sf


def fourier_transform(t, x):
    """フーリエ変換をする関数"""
    
    N  = len(x)
    dt = t[1] - t[0]

    # FFT（実数）と周波数軸
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(N, d=dt)

    # 振幅スペクトル
    amp = np.abs(X) / N
    if len(amp) > 2:
        amp[1:-1] *= 2
        
    return f, amp


def plot(t, x, freq, amp):
    """波形を確認する関数"""
    
    plt.rcParams['font.size'] = 14
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'

    fig = plt.figure(figsize=(6, 8))
    ax1 = fig.add_subplot(211); ax2 = fig.add_subplot(212)
    for ax in (ax1, ax2):
        ax.yaxis.set_ticks_position('both')
        ax.xaxis.set_ticks_position('both')

    ax1.set_xlabel('Time[s]')
    ax1.set_ylabel('Amplitude')
    ax2.set_xlabel('Frequency[Hz]')
    ax2.set_ylabel('Amplitude')
    ax2.set_xlim(0.0, 5000.0)
    ax2.set_ylim(-20, 80)
    #ax2.set_yscale('log')

    ax1.plot(t, x, label='time', lw=1, color='red')
    ax2.plot(freq, amp, label='freq', lw=1, color='red')

    fig.tight_layout()
    plt.show()
    plt.close()
    
    return

if __name__ == '__main__':
    """メイン"""
    
    # wav波形の読み込み
    path = 'wav/recorded.wav'
    data, samplerate = sf.read(path)
    
    # 時間軸の作成
    dt = 1 / samplerate
    t = np.arange(0, len(data)*dt, dt)
    
    # フーリエ変換とグラフ表示
    freq, amp = fourier_transform(t, data)
    
    # デシベル変換
    amp_db = 20 * np.log10(amp / 2e-5)
    
    # プロット
    plot(t, data, freq, amp_db)
