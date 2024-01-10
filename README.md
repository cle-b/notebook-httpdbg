# notebook-httpdbg

**notebook-httpdbg** is a notebook extension to trace the HTTP requests.

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

### configuration
```
%%httpdbg --header 500 --body 10000
```
You can choose the number of character to print for each request.


## example

```
In [1]: %load_ext notebook_httpdbg
```
```
In [2]: import requests
```

```
In [3]: %%httpdbg
        _ = requests.get("https://www.example.com")
```
```
Out [3]: - [httpdbg] 1 requests in 0.48 seconds
             - 200 GET https://www.example.com/
                 + request
                 - reponse
                    Content-Encoding: gzip
                    Accept-Ranges: bytes
                    Age: 428224
                    Cache-Control: max-age=604800
                    Content-Type: text/html; charset=UTF-8
                    Date: Sun, 05 Nov 2023 08:21:08 GMT
                    Etag: "3143526347+gzip"
                    Expires: Sun, 12 Nov 2023 08:21:08 GMT
                    Last-Modified: Thu, 17 Oct 2019 07:18:26 GMT
                    Server: ECS (bsb/27DC)
                    Vary: Accept-Encoding
                    X-Cache: HIT
                    Content-Length: 648

                    <!doctype html>
                    <html>
                    <head>
                        <title>Example Domain</title>

                        <meta charset="utf-8" />
                        <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
                        <meta name="viewport" content="width=device-width, initial-scale=1" />
                        <style type="text/css">
        
```

## documentation

https://httpdbg.readthedocs.io/en/latest/notebook/
