NicoLive2Feed (NL2F)
====

NicoLive2Feed is a scraping library to provide feed of searching result.

## Description

While RSS feeds for the non-live videos in nicovideo.jp are provided officially,
feeds for searching results of nico-live are not given officially.
I want to pick up automatically the new releases from searching result,
then feed them into feed aggregators (like Plagger).


## Demo

```
nicolive2feed -t 'WIXOSS' -f rss -s close
```
`nicolive2feed` is a demo-command.
In the above case, a feed for backward searching of the title 'WIXOSS' are dumped to standard error in the format of rss.


## Requirement

* Python2.7.6 or beyond (It don't works with Python3.x).
* added modules described in `requirements.txt`

You can install added modules using `pip` as follows:
```
pip install -r requirements.txt
```
