# Variabilidad de la Frecuencia Cardiaca usando la Transformada Wavelet
## Descripción 

En esta práctica de laboratorio, se busca estudiar la Variabilidad de la Frecuencia Cardíaca (HRV), la HRV es un marcador clave para evaluar la como se regula el sistema nervioso autónomo SNA actuando en el corazón. La HRV refleja las fluctuaciones temporales entre los intervalos R-R del electrocardiograma, permitiendo evaluar el equilibrio entre la parte simpática la cuál es responsable de acelerar las respuestas fisiológicas (como el aumento de la frecuencia cardíaca), y la rama parasimpática, encargada de promover estados de relajación. 

Mientras mayor se el nivel de variabilidad de la frecuencia cardica se puede decir que la persona cuenta con un sistema cardiovascular saludable y con una mayor capacidad de adaptarse a factores estresantes lo que permiten reducir la tasa de enfermedad 

 Por el contrario, una HRV reducida se ha relacionado con estrés, fatiga y diversas patologías, como la hipertensión y la insuficiencia cardíaca. 

La Transformada Wavelet, es una herramienta que permite identificar cambios en frecuencias características y analiza la dinámica temporal de la señal cardíaca, es eficiente para el análisis local de señales no estacionarias y de rápida transitoriedad. 

Esta transformada cuenta con dos parámetros indispensables en el análisis, el desplazamiento y el escalamiento. El desplazamiento se refiere a que se recorre la señal de adelante hacia atrás en el tiempo. Mientras que en el escalamiento se alarga y comprime la Wavelet. La señal resultante depende de la Wavelet madre y de los parámetros anteriormente mencionados. 

Los dos parámetros indispensables en el análisis por Transformada Wavelets son el desplazamiento y el escalamiento. En el desplazamiento se recorre la señal de adelante hacia atrás en el tiempo. Mientras que el escalamiento se refiere al alargamiento y la compresión de la Wavelet. La señal obtenida dependerá tanto de la Wavelet madre como de estos parámetros. Existen varios tipos de Transformada Wavelet, algunos de estos son: 

* Wavelet de Morlet = transformada continua   

![image](https://github.com/user-attachments/assets/f04aa85a-9e85-446f-95a7-e1ab9d6c5219)


* Wavelets Daubechies = transformadas discretas

![image](https://github.com/user-attachments/assets/0e7e8ad0-22d7-496f-b8de-3d069b88e75c)



Para la realización de la práctica se adoptó la siguiente metodología  



![diagramita](https://github.com/user-attachments/assets/54f9a77d-ebb4-4e2c-a0fe-d3cfca96017c)



















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



