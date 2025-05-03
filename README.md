
# Variabilidad de la Frecuencia Cardiaca usando la Transformada Wavelet

## Aviso 
Los datos utilizados en este proyecto son de mi autoría y han sido obtenidos a partir de mediciones personales. Se autoriza su uso y distribución exclusivamente para fines de investigación, educación y desarrollo de proyectos relacionados con el procesamiento de señales electromiográficas, siempre que se cite adecuadamente la fuente y se respete la integridad de la información. El uso con fines comerciales queda sujeto a mi autorización previa.
## Descripción 

En esta práctica de laboratorio, se busca estudiar la Variabilidad de la Frecuencia Cardíaca (HRV), la HRV es un marcador clave para evaluar la como se regula el sistema nervioso autónomo SNA actuando en el corazón. La HRV refleja las fluctuaciones temporales entre los intervalos R-R del electrocardiograma, permitiendo evaluar el equilibrio entre la parte simpática la cuál es responsable de acelerar las respuestas fisiológicas (como el aumento de la frecuencia cardíaca), y la rama parasimpática, encargada de promover estados de relajación. 

Mientras mayor se el nivel de variabilidad de la frecuencia cardica se puede decir que la persona cuenta con un sistema cardiovascular saludable y con una mayor capacidad de adaptarse a factores estresantes lo que permiten reducir la tasa de enfermedad 

 Por el contrario, una HRV reducida se ha relacionado con estrés, fatiga y diversas patologías, como la hipertensión y la insuficiencia cardíaca. 

La HRV cuenta con ciertos parámetros que permiten su estudio 

* SDNN: Es la desviación estándar de todos los intervalos R-R. Representa la variabilidad de la frecuencia cardíaca (HRV) considerando tanto fluctuaciones a corto como a largo plazo. Se da en milisegundos
* rMSSD Corresponde a la raíz cuadrada de la media de las diferencias cuadráticas entre intervalos R-R consecutivos. Es un indicador sensible de la actividad parasimpática y del control vagal sobre el corazón. Se da en milisegundos.


La Transformada Wavelet, es una herramienta que permite identificar cambios en frecuencias características y analiza la dinámica temporal de la señal cardíaca, es eficiente para el análisis local de señales no estacionarias y de rápida transitoriedad. 

Esta transformada cuenta con dos parámetros indispensables en el análisis, el desplazamiento y el escalamiento. El desplazamiento se refiere a que se recorre la señal de adelante hacia atrás en el tiempo. Mientras que en el escalamiento se alarga y comprime la Wavelet. La señal resultante depende de la Wavelet madre y de los parámetros anteriormente mencionados. 

Los dos parámetros indispensables en el análisis por Transformada Wavelets son el desplazamiento y el escalamiento. En el desplazamiento se recorre la señal de adelante hacia atrás en el tiempo. Mientras que el escalamiento se refiere al alargamiento y la compresión de la Wavelet. La señal obtenida dependerá tanto de la Wavelet madre como de estos parámetros. Existen varios tipos de Transformada Wavelet, algunos de estos son: 

* Wavelet de Morlet = transformada continua   

![image](https://github.com/user-attachments/assets/f04aa85a-9e85-446f-95a7-e1ab9d6c5219)


* Wavelets Daubechies = transformadas discretas

![image](https://github.com/user-attachments/assets/0e7e8ad0-22d7-496f-b8de-3d069b88e75c)



Para la realización de la práctica se adoptó la siguiente metodología  



![diagramita](https://github.com/user-attachments/assets/54f9a77d-ebb4-4e2c-a0fe-d3cfca96017c)





# Captura de la señal 
Para la captura de la señal utilizamos el módulo de electromiografia AD8232 el cual actúa como un sistema de amplifiacación y filtrado de la señal., posicionamos los electrodos activos en las derivaciones precordiales V1 y V2  enfocadas en la región septal, está es la región donde se encuentra la esctructura que separa los dos ventriculos. El electrodo tierra fue posicionado en la zona lateral del abdomen. 

Posteriormente conectamos el módulo de electromiografía al sistema de adquisición de datos NI-DAQ y Con el siguiente código se estableció una frecuencia de muestreo de 250 Hz, ya que el rango de frecuencias de una señal de electrocardigorama va de 0 a 100 Hz, utilizando una frecuencia de muestreo de 250 Hz aseguramos que se cumpla teorema de Nyquist. El código también permite graficar y guardar los datos de la señal en un archivo CSV para su posterior análisis.

```python
def iniciar_adquisicion(self):
device_name = self.puertos_combo.currentText()
if not device_name:
QMessageBox.warning(self, "Error", "Selecciona un dispositivo DAQ antes de iniciar la adquisición.")
return

self.archivo_tdms = "TestData.tdms"
self.duracion = 300
self.frecuencia_muestreo = 250
total_muestras = self.duracion * self.frecuencia_muestreo

try:
with nidaqmx.Task() as task:
task.ai_channels.add_ai_voltage_chan(f"{device_name}/ai0")
task.timing.cfg_samp_clk_timing(
self.frecuencia_muestreo,
sample_mode=AcquisitionType.FINITE,
samps_per_chan=total_muestras
)

task.start()
datos = task.read(number_of_samples_per_channel=total_muestras, timeout=nidaqmx.constants.WAIT_INFINITELY)
task.stop()

self.procesar_datos(datos)
except Exception as e:
QMessageBox.critical(self, "Error", f"Error durante la adquisición de datos:\n{e}")

```
La captura durante 5 minutos con el módulo dió como resultado la siguente señal

![sinfilro](https://github.com/user-attachments/assets/f0de424b-3005-4ebc-9ce4-9bc5b9c930c5)

La cual cuenta con los siguientes parámetros

![image](https://github.com/user-attachments/assets/edd46541-ab0c-416c-84ac-9bbee05a97a8)


durante la captura buscamos estresar y relajar al voluntario en varios momentos de la prueba con el fin de analizar la variabilidad de la Frecuencia Cardíaca

## Filtro digital IIR:

Antes de graficar los datos de la señal en Python, se aplica un filtro pasa banda digital tipo IIR (infinite impulse response) para ayudar a atenuar más las frecuencias no deseadas para el ECG, este filtro se define con los siguientes parámetros:
*Atenuación de -3,01dB para 0,5Hz y 100Hz
*Atenuación de -10dB para 0,1Hz y 120Hz
Estos parámetros se eligen teniendo en cuenta los rangos de frecuencia util para un ECG. Luego de elegir los parámetros se aplica un prewarping a cada dato, obteniendo los siguientes valores:
Ω1=0,628 rad/muestra
ΩL=3,142 rad/muestra
Ωu=1538,84 rad/muestra
Ω2=2621,09 rad/muestra
luego de esto se calcula el orden del filtro, obtniendo el valor absoluto de A y B a partir de la transformación de filtro paso bajo a pasa banda, y utilizando la frecuencia menor para despejar el orden del filtro (n)
![image](https://github.com/user-attachments/assets/db75a9af-9ec6-41d3-9eaf-d66c41330875)

se obtiene como resultado un filtro de orden 3. El tipo de filtro es Butterworth debido a que su atenuación de -3dB se encuentra en la frecuencia de corte para el filtro pasa alto y pasa bajo, lo que garantiza una transición suave entre la banda pasante y la banda de atenuación (sin ondulaciones) , además que es un filtro muy común disponible en prácticamente cualquier herramienta de procesamiento. 

luego de esto se toma la función de transferencia para un filtro de tercer orden y se reemplaza s con la expresión correspondiente a transformación correspondiente de filtro paso bajo a pasa banda, obteniendo la siguiente expresión para la función de transferencia:
![image](https://github.com/user-attachments/assets/33ffc665-2886-40de-bbda-5816e044ff1f)
y reemplazando ΩL y Ωu obtenemos:
![image](https://github.com/user-attachments/assets/a902c330-2d51-4527-8c65-ce380097df8d)

Luego de obtener la función de transferencia se aplica una transformación bilineal para pasar del dominio s al dominio z(dominio digital), aplicando la siguiente formula con w=s

![image](https://github.com/user-attachments/assets/651c8d42-7123-494b-bf73-fd0e8a98cf09)

se obtiene la siguiente función de transferencia en terminos de z, y aplicando la trasnformada z inversa con condiciones iniciales iguales a 0, se obtiene la respectiva ecuación en diferencias para el filtro:

![image](https://github.com/user-attachments/assets/cc13727d-5615-4433-969f-ab094fe1c426)
![image](https://github.com/user-attachments/assets/6959dc9e-a8f8-48b8-ac38-84d42fdd9eb4)

Una vez diseñado el filtro, se implementó en python, teniendo en cuenta el orden calculado, las frecuencias de corte establecidas, y la frecuencia de muestreo, además de esto se usó un comando de python para imprimir los coeficientes de la función de transferencia del filtro (los cuales están en terminos de z debido a que es un filtro digital), a continuación se muestra el código:

```python
import numpy as np
import pandas as pd
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt


def butter_lowpass_filter(data, cutoff, fs, order=3):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = lfilter(b, a, data)
    return y


def butter_highpass_filter(data, cutoff, fs, order=3):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    y = lfilter(b, a, data)
    return y


file_path = "senal_ecgfinal ultimo.csv"
df = pd.read_csv(file_path)


t = df.iloc[:, 0].values
emg_signal = df.iloc[:, 1].values


fs = 250.0               
low_cutoff = 0.5          
high_cutoff = 100.0       
order = 3                 


filtered = butter_lowpass_filter(emg_signal, high_cutoff, fs, order)
filtered = butter_highpass_filter(filtered, low_cutoff, fs, order)


plt.figure(figsize=(10, 5))
plt.plot(t, emg_signal, label='Original', alpha=0.5)
plt.plot(t, filtered, label='Filtrada (0.5–100 Hz)', linewidth=2)
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.legend()
plt.title("Filtrado Pasa Banda ECG - Orden 3")
plt.grid(True)
plt.tight_layout()
plt.show()

nyq = 0.5 * fs
low = low_cutoff / nyq
high = high_cutoff / nyq

# Coeficientes del filtro pasa banda
b, a = butter(order, [low, high], btype='bandpass', analog=False)

# Imprimir coeficientes (forma directa)
print("Coeficientes del numerador (b):", b)
print("Coeficientes del denominador (a):", a)
```
![image](https://github.com/user-attachments/assets/f0332b36-f56a-4056-9c7a-ac11a643b99a)
como podemos observar los coeficientes impresos corresponden a los coeficientes calculados luego de la transformación bilineal en el filtro, por lo que el dieseño del filtro se puede considerar exitoso y concordante con lo planteado. Una vez verificado el filtro, se gráfica tanto la señal ecg original como la filtrada, obteniendo las siguientes gráficas:
![image](https://github.com/user-attachments/assets/c91660bc-0a57-4d7c-ad47-5a95a2140471)

# HRV en el dominio del tiempo:
Luego de filtrada la señal de ECG, calculamos los intervalos R-R para obtener una nueva señal que contiene el HRV, que es la variabilidad de la frecuencia cardiaca, es decir la variación de tiempo entre cada R-R.
Posteriormente se analiza en el dominio del tiempo, obteniendo valores como la media, desviacion estandar, entre otros.

```python

```
# Transformada Wavelet
Se obtubo un espectrograma de la HRV usando la transformada wavelet continua, utilizando la función wavelet Morlet que es usada en señales fisiológicas.
También se obtuvo LF/HF, que es la relación entre las bandas de baja y alta frecuencia, la banda de baja frecuencia (0,04-0,15 Hz) está relacionada con el sistema nervioso simpático, activo en situaciones de estrés; mientras que la banda de alta frecuencia (0,15-0,4 Hz) se relaciona con el sistema nervioso parasímpatico, activo en estados de relajación.
Podemos observar en la relación LF/HF valores altos iniciales, que luego disminuyen y vuelven a aumentar luego de los 200s, indicando inicialmente predominancia de la activad simpática, luego de la actividad parasimpática y por ultimo de la simpática otra vez, esto tambien lo podemos observar en el espectrograma donde vemos una mayor potencia al inicio y al final en la banda de baja frecuencia.



### Requisitos 
* Pyton 3.9.0 ó superior
* Módulo de electrocardiograma AD8232
* NI DAQ USB
* Electrodos 
### Librerias
* Pandas
* numpy
* matplotlib
* scipy.stats
* nidaqmx
* PyQt5
* PyWavelets



