Sample-prep
===========

Remove silence from percussive samples, normalize and write norm/high/low
versions.

Install
-------

Pip:

```bash
pip install .
```

Poetry:

```bash
poetry shell
poetry install
```

Apple M1:

```bash
poetry shell
export LLVM_CONFIG=/opt/homebrew/Cellar/llvm@11/*/bin/llvm-config
pip install llvmlite
poetry install
```

Run
---

```bash
sample-prep ~/path/to/samples
```

Usage
-----

* Record samples as 96kHz/24bit
* Record for 2 seconds before making the sound, keep recording for another two
seconds
  * I use this to cut noises when pressing buttons on the recorder
* Place the samples in a folder in a subfolder called `in`
* Run sample-prep
* Check your samples, if there is unwanted noise in the result, silence it in
there original
* There are some heuristics to prepare most samples correct, if some don't work
process them manually

In my test out of 40 samples I had to silence parts in 2 samples.
