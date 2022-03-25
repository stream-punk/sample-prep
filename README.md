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
