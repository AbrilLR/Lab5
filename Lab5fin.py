import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, filtfilt, find_peaks
from scipy import signal
import pywt


file_path = "senal_ecgfinal ultimo.csv"
df = pd.read_csv(file_path)
t = df.iloc[:, 0].values
ecg_signal = df.iloc[:, 1].values

fs = 250.0  
nyquist = 0.5 * fs


duracion_total = t[-1] - t[0]  
num_muestras = len(t)
fs = 1 / np.mean(np.diff(t))

print(f"Duración total: {duracion_total:.2f} segundos")
print(f"Número de muestras: {num_muestras}")
print(f"Frecuencia de muestreo: {fs:.2f} Hz")





print("\nEstadísticas de la señal:")
print(f"Voltaje máximo: {np.max(ecg_signal):.4f} V")
print(f"Voltaje mínimo: {np.min(ecg_signal):.4f} V")
print(f"Voltaje promedio: {np.mean(ecg_signal):.4f} V")
print(f"Desviación estándar: {np.std(ecg_signal):.4f} V")


# Diseño de filtros

def butter_highpass(data, cutoff=0.5, fs=250.0, order=3):
    normal_cutoff = cutoff / (0.5 * fs)
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return lfilter(b, a, data)


def butter_lowpass(data, cutoff=40.0, fs=250.0, order=4):
    normal_cutoff = cutoff / (0.5 * fs)
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)


def notch_filter(data, notch_freq=60.0, fs=250.0, bandwidth=4.0):
    low = (notch_freq - bandwidth/2) / nyquist
    high = (notch_freq + bandwidth/2) / nyquist
    b, a = butter(2, [low, high], btype='bandstop')
    return filtfilt(b, a, data)


ecg_filtered = butter_highpass(ecg_signal)
ecg_filtered = butter_lowpass(ecg_filtered)
ecg_filtered = notch_filter(ecg_filtered)



duracion_total = t[-1] - t[0]
tiempo_inicio = t[0] + duracion_total / 2 - 10
tiempo_final = tiempo_inicio + 20

idx_inicio = np.searchsorted(t, tiempo_inicio)
idx_final = np.searchsorted(t, tiempo_final)


plt.figure(figsize=(12, 4))
plt.plot(t[idx_inicio:idx_final], ecg_signal[idx_inicio:idx_final])
plt.title("Señal ECG Original - 20s")
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.grid(True)
plt.tight_layout()
plt.show()


plt.figure(figsize=(12, 4))
plt.plot(t[idx_inicio:idx_final], ecg_filtered[idx_inicio:idx_final], color='orange')
plt.title("Señal ECG Filtrada - 20s")
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (V)")
plt.grid(True)
plt.tight_layout()
plt.show()


print("\nEstadísticas de la señal ECG filtrada:")
print(f"Voltaje máximo: {np.max(ecg_filtered):.4f} V")
print(f"Voltaje mínimo: {np.min(ecg_filtered):.4f} V")
print(f"Voltaje promedio: {np.mean(ecg_filtered):.4f} V")
print(f"Desviación estándar: {np.std(ecg_filtered):.4f} V\n")

b, a = butter(4, 40.0/nyquist, btype='low')
print("Coeficientes de filtro IIR (b):", b)
print("Coeficientes de filtro IIR (a):", a)
print("Ecuación en diferencias: y[n] = " +
      " + ".join([f"{b[i]:.3e}*x[n-{i}]" for i in range(len(b))]) + " - " +
      " - ".join([f"{a[i]:.3e}*y[n-{i}]" for i in range(1, len(a))]))


altura_umbral = np.mean(ecg_filtered) + 0.5 * np.std(ecg_filtered)
picos_r, _ = find_peaks(ecg_filtered, height=altura_umbral, distance=int(0.6 * fs))

print(f"\nNúmero de picos R detectados: {len(picos_r)}")


rr_intervals = np.diff(t[picos_r])
rr_times = np.cumsum(rr_intervals)
rr_times = np.insert(rr_times, 0, t[picos_r[0]])
rr_intervals_full = np.insert(rr_intervals, 0, rr_intervals[0])



fs_rr = 1 / np.mean(np.diff(rr_times))
print(f"\nFrecuencia promedio de muestreo para señal R-R: {fs_rr:.2f} Hz")

#HRV

hrv_rmssd = np.sqrt(np.mean(np.square(np.diff(rr_intervals))))
hrv_sdnn = np.std(rr_intervals)

print(f"HRV (RMSSD): {hrv_rmssd * 1000:.2f} ms")
print(f"HRV (SDNN): {hrv_sdnn * 1000:.2f} ms")


plt.figure(figsize=(12, 6))
plt.plot(rr_times, rr_intervals_full, marker='')
plt.title("Variabilidad de la frecuencia cardíaca - Intervalos R-R")
plt.xlabel("Tiempo (s)")
plt.ylabel("Intervalo R-R (s)")
plt.grid(True)
plt.tight_layout()
plt.show()


#  Transformada 


fs = 1 / np.mean(np.diff(rr_times))
coef, freqs = pywt.cwt(rr_intervals_full, np.arange(1, 128), 'morl', sampling_period=1/fs)
power = np.abs(coef)**2

freqs, power = freqs[freqs <= 0.5], power[freqs <= 0.5]
lf = (freqs >= 0.04) & (freqs < 0.15)
hf = (freqs >= 0.15) & (freqs <= 0.4)
lf_hf = np.sum(power[lf], axis=0) / np.sum(power[hf], axis=0)

fig, axs = plt.subplots(2, 1, figsize=(12, 6), sharex=True)
axs[0].imshow(power, extent=[rr_times[0], rr_times[-1], freqs[0], freqs[-1]], cmap='jet', aspect='auto', origin='lower')
axs[0].set_ylabel("Frecuencia (Hz)")
axs[1].plot(rr_times, lf_hf, color='darkred')
axs[1].set_xlabel("Tiempo (s)")
axs[1].set_ylabel("LF/HF")
plt.tight_layout(); plt.show()



