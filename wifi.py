#!/usr/bin/env python3


import argparse
import numpy as np
import matplotlib.pyplot as plt
import json

parser = argparse.ArgumentParser()
parser.add_argument('input',  metavar='FILENAME', type=str)

if __name__ == "__main__":
    args = parser.parse_args()
    print(args.input)
signal = np.genfromtxt(open(args.input), delimiter=' ')
code = np.array([+1, +1, +1, -1, -1, -1, +1, -1, -1, +1, -1])
code = np.repeat(code,5)
dc = np.convolve(signal,code[::-1], mode = 'full')
time = np.arrange(dc.shape[0])
plt.figure(figsize = (11,5))
plt.plot(time,dc,color = 'green')
std = np.std(dc)
mean = np.mean(dc)
peaksup = dc > (mean + 3*std)
peaksdown = dc < (mean - 3*std)
tup = time[peaksup]
tdown = time[peaksdown]
plt.plot(tup, dc[peaksup], '*', color = 'red')
plt.plot(tdown, dc[peaksdown], '*', color = 'red')
plt.show()
Ndown = len(tdown)
for k in range(1, Ndown):
    if abs(tdown[k] - tdown[k-1]) < 5:
        tup[k-1] = 0
Nup = len(tup)
for i in range(1, Nup):
    if abs(tup[i] - tup[i-1]) < 5:
        tup[i-1] = 0    
tdown = -tdown # для отдлеления по модулю верхних от нижних пиков
sopt = np.concatenate((tup, tdown))
piks = sorted(sopt, key = abs)
bitpiks = []
for x in range(len(piks)):
    if piks[x] < 0:
        bitpiks.append(0)
    elif piks[x] > 0:
         bitpiks.append(1)       
resul = bytes(np.packbits(bitpiks)).decode(encoding = 'ascii')
slovar_resul = {'message':resul}
with open('wifi.json', 'w') as file:
    json.dump(slovar_resul, file)
