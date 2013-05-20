djdns-hype-flat
===============

A script and resources to host DNS for the .hype domain using DJDNS and its file backend.

## Guide to operation

To set up an instance of DHF, make sure you have python-virtualenv installed,
and then follow these steps. Python versions 2.6-3.3 are supported.

```bash
$ cd ~ # Or wherever you want to store the project
$ virtualenv dhf
$ cd dhf
$ source ./bin/activate
$ pip install docopt
$ git clone https://github.com/campadrenalin/pymads
$ git clone https://github.com/campadrenalin/python-djdns
$ git clone https://github.com/campadrenalin/djdns-hype-flat
$ cd pymads
$ python setup.py install
$ cd ../python-djdns
$ python setup.py install
$ cd ../djdns-hype-flat
```

Then, to run:
```bash
$ sudo ~/dhf/bin/python run.py -u $USER -g $USER
```

This starts the script as root so that it can bind to port 53, then immediately
drops back down to your natural god-given user credentials.

To test this out:

```bash
$ dig @localhost ri.hype
```

## How do I get my domain added to the .hype domain?

Ask nicely in an issue! Provide your information, or make a pull request with
the appropriate changes.
