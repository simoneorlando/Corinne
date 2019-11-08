# Corinne
Corinne is a tool to manage Choreography Automata (CA).

## Table of Contents

* [Dependencies](#dependencies)
* [Running](#running)
* [Usage](#usage)
* [File List](#file-list)
* [License](#license)

### Dependencies

- [Python3] (3.7)
- [Graphviz] (https://www.graphviz.org/download/) (0.10.1)
- [graphviz-python3-package] (https://pypi.org/project/graphviz/) (0.13.2)
- [antlr4-python3-runtime] (https://pypi.org/project/antlr4-python3-runtime/) (4.7.2)

### Running

Open a terminal in the main folder of Corinne and type:
```sh
python3 main.py
```

### Usage

- OPEN: takes in input DOT files (.gv) in CA syntax, but also it can get:
        - Chorgram file (.txt) , a grammar used for Global Graph (See [Chorgram] (https://bitbucket.org/emlio_tuosto/chorgram/wiki/Home))
        - DOT files (.gv) generated by Domitilla (See [Domitilla] (https://github.com/dedo94/Domitilla))
        and convert them into DOT files with CA syntax.
    For more details about the CA syntax see "/dot_parser/DOT.g4" file.

- RENDER: render a given DOT (.gv) file in PNG or PDF format.

Once taken one or more files as input, Corinne can apply some functions on it:

- PRODUCT: a cartesian product of two CA ;
- SYNCHRONIZATION: given a CA, it can synchronize two participants of its ;
- PROJECTION: given a CA, you can select one participant from it and get the relative CFSA (Communicating-FSA) ;


### File List
* main.py : launch the program.
* guy.py : define the guy and its methods to create every view of the program.
* controller.py : define methods used by the guy to process files (open, render, ...).
* fsa.py : an abstract class to define a simple Finite State Machine and its methods.
* chor_auto.py : a class to define the Choreography Automata (CA), inherits from fsa class.
* cfsa.py : a class to define the Communicating FSA (CFSA), inherits from fsa class.
* dot_parser/* : contains the dot parser and every files it need to parse and convert.
* global_graph_parser/* : contains the Global Graph parser and every files it need to parse and convert.
* example/* : some examples.

### Author
**Simone Orlando** - [simoneorlando](https://github.com/simoneorlando) - simoneorlando.cs@gmail.com

### License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details