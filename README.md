# notebook-httpdbg

`notebook-httpdbg` is a notebook extension to trace the HTTP requests.

## installation 

```
pip install notebook-httpdbg
```

## usage

### load the extension in the notebook

```
%load_ext notebook_httpdbg
```

### trace the HTTP requests for a cell
```
%%httpdbg
```

## example

```
%load_ext notebook_httpdbg
import requests
%%httpdbg
_ = requests.get("https://www.example.com")
```