## Network optimization algorithm

### Instalation:
Python 3.6 and pip are needed

```
pip install numpy
```

### Usage:

```
python main.py -e <entry_dir> -d <demands_file> -c <number_of_cores> [-s]

-e, --entry <entry_dir>          Absolute path to directory with files (must end with /)
-d, --dfile <demands_file>       Full name of file with demands
-c, --cores <number_of_cores>    Number of cores in a single link (must be > 0)
-s, --summary                    Generates a brief summary in a format: <demands_file>_summary.csv

```

#### Entry directory must contain following files:
- f30.spec
- ff.net
- ff30.pat

#### Demands file name must be in format <net_load>_<set_nr>.dem, where:
- <net_load> is a average network load in Erlangs
- <set_nr>  is number of the demands set
