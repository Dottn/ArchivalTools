# ArchivalTools

## DownloadNataliePictures.py

This script crawls through the artist page of a specified artist on natalie.mu, and downloads every single picture from the linked article galleries.

### Prerequisites

The script uses the python modules lxml, yurl, and requests.
They can be installed by running:

`python -m pip install lxml requests YURL`

Alternatively:

`python -m pip install -r requirements.txt`

### Usage

In the start of `DownloadNataliePictures.py`, the variables `artist_id` and `pages` are set.

Sakura Gakuin Artist page: <https://natalie.mu/eiga/news/list/page/1/artist_id/8935>

The artist ID is the last element on the artist page of the relevant artist, in this case `8935`.
At time of writing, the oldest natalie articles of SG were on page 14, so to get all pictures, set `pages` to 14.

Pictures will be downloaded to `./natalie/$artist_id/$article_id`
If the folder already exist, the script will skip that article.

Fair warning, if an article is about for example TIF, and your artist is mentioned, *ALL* pictures will be downloaded, independent of who's actually on it.

After setting `artist_id` and `pages`, run:

`python ./DownloadNataliePictures.py`

Sample output:

``` bash
$ python .\DownloadNataliePictures.py
Artist ID: 8935
Number of pages to check: 1
Page 1
Article 352258
Article 352136
352136/onefive_art201910.jpg
352136/onefive_jkt201910.jpg
352136/onefive_MOMO.jpg
352136/onefive_GUMI.jpg
352136/onefive_KANO.jpg
352136/onefive_SOYO.jpg
352136/onefive_01.jpg
352136/onefive_02.jpg
352136/onefive_03.jpg
352136/default.jpg
```

### Systems

Verified working on Windows (using vscode).