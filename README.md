# ptcx
A format for modularized AST-based patching of arbitary code.

> [!WARNING]
> This is only conceptual and not implemented yet.

# Usage
Setup a directory stucture:
1. `./src` the source code you'd like to patch
2. `./patch` the patches to apply [docs](docs/README.md)

Patch
```
python -m ptcx patch
```
Reset previous state of src
```
python -m ptcx reset
```
