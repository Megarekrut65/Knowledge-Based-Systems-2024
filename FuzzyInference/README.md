# Fuzzy Inference
A fuzzy inference algorithm based on fuzzy rules was implemented.
The main.py file shows an example with the following rules:
```
R1: if the pressure is high, then the temperature is average
R2: if the pressure is low, then the temperature is low

Where,
Pressure surface - {800, 830, 860, 900}
Temperature surface - {300, 350, 400}

High pressure - {800/0.4; 830/0.6; 860/0.8; 900/1}
Low pressure - {800/1; 830/0.9; 860/0.6; 900/0.4}

Average temperature {300/0.5; 350/1; 400/0.5}
Low temperature {300/1; 350/0.4; 400/0.1}
```