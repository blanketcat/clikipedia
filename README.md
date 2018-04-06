# CLIkipedia

##### Read Wikipedia Articles From The Command Line 

### Installation

```
~$ git clone https://github.com/knotech/clikipedia.git
~$ cd clikipedia/
~$ virtualenv -p python3 env
~$ source env/bin/activate
~$ pip install -r requirements.txt
```

Dependencies:
* Postgresql
* MongoDB
* PyQt4 (Which implies a few other things namely QT4, and sip)

### Usage

##### Web

If you want to skip downloading and wiring the wikipedia SQL dumps you can pull the articles from the web.

```
~$ ./clickipedia/sources/wikipedia.py "your search query phrase" -g
```
##### CLI

```
~$ know command line interface
```

##### GUI

```
~$ know_gui command line interface
```

### Setting up standalone system

Presently, a lot of the process for setting up a stand alone system requires manual configuration. Soon this should not be an issue.  
* Download The English Wikipedia XML Dumps
* The Program Parses Wikipedia
* The Program Populates Databases
* ```~$ know "Thing you want to know about" ```

##### Notes

* Donate to wikimedia https://wikimediafoundation.org/wiki/Ways_to_Give
* If you download a SQL dump, create a torrent and seed it.
