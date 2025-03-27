# Install deps
(yes, this also runs on linux//bash)
```bash
./deps.bat
```

# Build package
```
python -m build
```

# Uploading to pypi
```
python -m twine upload dist/*
```