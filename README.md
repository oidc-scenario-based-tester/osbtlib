# osbtlib

# test
```
// Run all tests
$ python -m pytest

// Run only test that do not use the server and proxy
$ python -m pytest -m "not server and not proxy"

// Run only tests that do not use the server
$ python -m pytest -m "not server"

// Run only tests that use the server
$ python -m pytest -m "server"
```