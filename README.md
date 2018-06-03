**main.py**

This code performs a GET request in chunks and save the results to a file. The number of chunks, size of the chunks, and how to download are modulated with arguments.

**Arguments**

  - **source** {type: str} Source URL to perform a GET request
  - **target** {type: str} Target location to save to (default is ./data/default.jar)
  - **async** {type: bool} Defines if we should perform the GET request serially or asynchronously (default is false)
  - **chunks** {type: int} Number of chunks to download (default is 4)
  - **chunksize** {type: int} Size of each chunk to download (default is 1 MiB)

**Python 3.x Required**

How to Install Dependencies
```
pip install -r requirements.txt
```

How to Run
```
python main.py <source> <target> <async> <chunks> <chunksize>
```

**Notes**

1. The arguments must be passed to main.py in the order listed above (and no not skip one)
2. The only required argument is "source"
3. When passing in arguments, do not provide quotation marks for things you expect to be a string (the code will explicitly handle this)
4. All testing was performed on a Windows machine (7 & 10) with Python 3.6.4