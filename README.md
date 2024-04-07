# CSP With Preference Reasoning

### goal:

CSP instances can be generated using the RB model with random dependencies and a number
of different conditional preferences. The CSP instance is then solved by a back tracking
algorithm and two other optimizations(Full look ahead, Forward Checking). However, the generated
assignment sequences are evaluated by the given preferences, so we get the most optimal solutions.
These are called pareto solutions and the implemented model supports finding the k-pareto solutions.


### Compiling and Execution:

In order to run the program, simply execute the main.py in the folder that it is with
other files.

Windows
``` cmd
python main.py
```

Linux:
```
python3 main.py
```

You can also install the provided package CSPInst on PIP
with the provided setup.py.

Windows
``` cmd
python setup.py install
```

Linux:
```
python3 setup.py install
```