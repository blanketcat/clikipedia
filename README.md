# CLIkipedia

### Read Wikipedia Articles From The Command Line 

### Installation For Development

Dependencies:

* Postgresql
* MongoDB
* PyQt4 (Which implies a few other things namely QT4, and sip)
* Helmet (No dude, like a *real* helmet. As you are reading this I have yet to run this once.)


```~$ git clone https://github.com/knotech/clikipedia.git
~$ cd clikipedia/
~$ virtualenv -p python3 env
~$ source env/bin/activate
~$ pip install -r requirements.txt```


### Usage

```
~$ know command line interface
```

```
~$ know_gui command lin interface
```

### Web

If you want to test it before downloading wikipedia, just run ```~$ ./clickipedia/sources/wikipedia.py "your search query phrase" -g```


### How it works

* You Download The English Wikipedia XML Dumps
* The Program Parses Wikipedia
* The Program Populates Databases
* ```~$ know "Thing you want to know about" ```
* Magic.


### How to help

Wikimedia currently experiences an insanely high volume of requests to themselves and the mirrors of these XML dumps. You can help by seeding a torrent if you download the dump.


### Pull requests

I have way too much on my plate to maintain this. Bug fixes seriously appreciated.

Like seriously, I've never run it. I just wrote it just to write it.
