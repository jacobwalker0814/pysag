# pysag
The Python Static site and API Generator

[![Build Status][travis-image]][travis-link]
[travis-image]: https://travis-ci.org/jacobwalker0814/pysag.svg?branch=master
[travis-link]: https://travis-ci.org/jacobwalker0814/pysag

## Overview
This package provides a `Reader` that will parse a directory for yaml files and
generate python data structures. There is also a `Writer` that will dump this
data as JSON into a web servable location.

The basic intended use case is to generate a static site running a JavaScript
front end to consume a generated API.

## Example
Given a directory called `_data` that looks like this

    _data/
    ├── portfolio
    │   ├── 1.yml
    │   └── 2.yml
    └── posts
        ├── 2008-08-14.yml
        └── 2010-05-15.yml

Running the following script

```python
import pysag

reader = pysag.Reader()
writer = pysag.Writer()
writer.write(reader.read('_data'), '_site/api')
```

Will generate the following directories / files at `_site/api`

    _site/
    └── api
        ├── portfolio
        │   ├── 1.json
        │   └── 2.json
        ├── portfolio.json
        ├── posts
        │   ├── 2008-08-14.json
        │   └── 2010-05-15.json
        └── posts.json

### Writing Content
Pysag primarily only parses yaml files to generate api data. However properties
of the generated data can be parsed from markdown files. Take for example the
following set of files:

`_data/posts/2008-08-14.yml`

```yaml
title: Wedding Day
author: Jacob
coauthor: Anna
_markdown:
    abstract: 2008-08-14-abstract.md
    body: 2008-08-14-body.md
```

`_data/posts/2008-08-14-abstract.md`

    It was a day **long** in the making... but we got there!

`_data/posts/2008-08-14-body.md`

    All (*most*) of our friends and family came out to celebrate with us.

The key `_markdown` in the yaml file tells pysag to look for additional
files to parse as markdown. The names of these files do not matter but
they will be parsed relative to the directory of the yaml file.

These three files would generate the following object in the API

```json
{
    "_id": "2008-08-14",
    "abstract": "<p>It was a day <strong>long</strong> in the making... but we got there!</p>",
    "author": "Jacob",
    "body": "<p>All (<em>most</em>) of our friends and family came out to celebrate with us.</p>",
    "coauthor": "Anna",
    "title": "Wedding Day"
}
```

## Tests
Run the tests with `nosetests`.

## TODO
* Better dependency management
    * Can I use versioning in requirements.txt like `~1.0.1`?
    * Separate file for dev requirements
* Allow specifying the DataNode class in yml files
* Make everything more "Pythonic"
* Some mechanism to fetch just certain fields
* Complete / document the executable
* Ability to generate RSS feed and sitemap.xml?
