TextExpansion
=============

TextExpansion is a tool that can be used to expand short texts by using lexic and/or semantic dictionaries. This tool is part of an academic research an a published paper with the complete description of how it works can be found [here](http://www.dt.fee.unicamp.br/~tiago/papers/TPS_ENIAC14.pdf) (in portuguese).

Installation
------------

To install TextExpansion, execute the setup.sh script. Text Expansion also uses BabelNet as a semantic dictionary. BabelNet can be installed by using the install_babelnet.sh script.

Using TextExpansion
-------------------

TextExpansion can be used via a graphic UI or via command line. To use its UI just run the main.py program without any arguments. If you want to use it via command line, run the main.py program passing the arguments on the following format:

```
$ python main.py <default_dictionaries> [babelnet_config] <input_file> [custom_dictionaries]
```

where 

* **\<default_dictionaries\>** is a string of four letters (Y/N) indicating which default dictionaries should be used (original, lingo, concepts, disambiguation);
* **\[babelnet_config\]** is a parameter that indicates which databases BabelNet should use. -wn tells it to use only WordNet, -wiki tells it to use only Wikipedia, and leaving it empty will make it use both datasets;
* **\<input_file\>** is the dataset containing the texts you want to expand. This should be a simple text file with one sample each line. An example of this file can be found on res/samples.txt;
* **\[custom_dictionaries\]** is a list of files of custom dictionaries that you might want to use. Each of these dictionaries should be a text file where each line contains the word that should be translated and its desired translation, separated by a tab. An example of this file can be found on res/custom.txt.

