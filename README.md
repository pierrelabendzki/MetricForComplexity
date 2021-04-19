# MetricForComplexity
Using lossless audio compression algorithmic to measure information content of musical messages. This approach base on Minimum Length Description offers a quantitative measurement for musical complexity that can analyses micro, meso and macro-scale redundancy in music. Visualisation of complexity over time of a given musical message can be use as a tool for musicology study. 

### requirement 

Python : 
numpy, scypi, matplotlib 

Flac codec at https://xiph.org/flac/index.htm

### use

For the sliding window and cumulative window : 

Set the pathway of the .wav file and the size of the increment of window in seconds. The ```fenetre_cumul``` and ```fentre_glissante``` functions return a one dimentional array of the complexity at every second of the track.        

```
filename = 'TheWellTemperedClavier.wav'
list_complexity_cumul = fenetre_cumul(filename,1)
list_complexity_slide = fenetre_glissante(filename,5)
```


![image](https://user-images.githubusercontent.com/45845954/115256170-45b5a880-a12f-11eb-8b85-9e249a2b4864.png)

