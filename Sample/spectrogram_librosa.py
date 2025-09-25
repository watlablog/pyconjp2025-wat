import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt


def plot_spectrogram_librosa(
    wav_path, Fs, overlap, window, vmin, vmax, xlim, ylim):
    """Librosaでスペクトログラムをプロットする関数"""
    
    # 音声読み込み
    y, sr = librosa.load(wav_path, sr=None, mono=True)

    # ずらし幅（ここではオーバーラップの考え方を使っている）
    hop_length = max(1, int(Fs * (1.0 - overlap / 100.0)))

    # STFT
    D = librosa.stft(
        y,
        n_fft=Fs,
        hop_length=hop_length,
        window=window,
        center=False)

    # 振幅スペクトル
    S = np.abs(D)

    # スケーリングとハニング窓の振幅補正係数（ACF = 1 / (sum(hann)/N)）
    han = np.hanning(Fs)
    acf = 1.0 / (han.sum() / Fs)
    S *= acf / (Fs / 2.0)

    # dB変換（20μPaを基準）
    S_db = librosa.amplitude_to_db(S, ref=2e-5)

    # プロット
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # librosa.display.specshowで周波数軸をHz表示
    img = librosa.display.specshow(
        S_db,
        x_axis="time",
        y_axis="hz",
        sr=sr,
        hop_length=hop_length,
        cmap="jet",
        ax=ax,
        )

    # カラーバー
    cbar = fig.colorbar(img)
    cbar.set_label("Amplitude[dB]")

    # 軸ラベル
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Frequency [Hz]")

    # カラースケール
    img.set_clim(vmin=vmin, vmax=vmax)

    # 表示範囲
    if xlim is not None:
        ax.set_xlim(*xlim)
    if ylim is not None:
        ax.set_ylim(*ylim)

    plt.show()
    plt.close()


if __name__ == "__main__":
    """メイン"""
    
    plot_spectrogram_librosa(
        wav_path="wav/recorded.wav",
        Fs=2048,
        overlap=90,
        window="hann",
        vmin=0,
        vmax=80,
        xlim=(0.0, 3.0),
        ylim=(0, 3000)
        )
