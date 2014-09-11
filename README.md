# pysag
The Python Static API Generator

## Overview
This package provides a `Reader` that will parse a directory for yaml files and
generate python data structures. There is also a `Writer` that will dump this
data as JSON into a web servable location.

The basic intended use case is to generate a static site running a JavaScript
front end to consume a generated API.

## Example
Given a directory called `_data` that looks like this

    _data/
    ├── porfolio
    │   ├── 1.yml
    │   └── 2.yml
    └── posts
        ├── 2008-08-14.yml
        └── 2010-05-15.yml

Running the following script

~~~python
import pysag

reader = pysag.Reader()
writer = pysag.Writer()
writer.write(reader.read('_data'), '_site/api')
~~~

Will generate the following directories / files at `_site/api`

    _site/
    └── api
        ├── porfolio
        │   ├── 1.json
        │   └── 2.json
        ├── porfolio.json
        ├── posts
        │   ├── 2008-08-14.json
        │   └── 2010-05-15.json
        └── posts.json


## Tests
Run the tests with `nosetests`.

## TODO
* Can I use versioning in requirements.txt like `~1.0.1`?
* Allow specifying the DataNode class in yml files
* Allow defining properties from converted markdown files
* Better doc for expected yml file contents
* Make everything more "Pythonic"
