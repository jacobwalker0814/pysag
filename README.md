# pysag
The Python Static API Generator

## Overview
This package provides a `Reader` that will parse a directory for yaml files and
generate python data structures. There is also a `Writer` that will dump this
data as JSON into a web servable location.

The basic intended use case is to generate a static site running a JavaScript
front end to consume a generated API.

## Tests
At the moment the only test present is for the `Reader` class. To test it run
`python -m pysag.test.reader`

## TODO
* Write `Writer`
* Make/find better test runner
* Use PIP for requirements (PyYAML)
