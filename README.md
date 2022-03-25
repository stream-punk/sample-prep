Install
-------

```bash
poetry shell
poetry update
```

Apple M1:

```bash
poetry shell
export LLVM_CONFIG=/opt/homebrew/Cellar/llvm@11/*/bin/llvm-config
pip install llvmlite
poetry update
```
