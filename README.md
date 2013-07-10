djdns-hype-flat
===============

A script and resources to host DNS for the .hype domain using DJDNS and its
file backend. Includes a scraper facility to import data from the HypeDNS API.
Anything hosted on HypeDNS can be hosted with this instead, and it will be
forward-compatible with DJDNS when the DEJE backend is worth using.

## Try out the public alpha now!

I'm running a server on roaming-initiative.com for people to use on and off the meshnet. To use it:

### Back up your existing conf

If something goes terribly wrong, whether on your end or mine, you'll want to have your old config back. So in your shell, do this:

    $ cp /etc/resolv.conf /etc/resolv.conf.bak

Or more succinctly (although I think it's specific to bash):

    $ cp /etc/resolv.conf{,.bak}

That way, you can copy the original back over later if you have to.

### Put in the new conf

Replace the contents of /etc/resolv.conf with the following:

    nameserver [fcd5:7d07:2146:f18f:f937:d46e:77c9:80e7]
    nameserver 173.255.210.202
    nameserver 8.8.8.8

These are, respectively:

 * Roaming Initiative on Hyperboria.
 * Roaming Initiative via IPv4 Clearnet.
 * Google Public DNS.

This should be a pretty sane chain of fallbacks for most alpha testers, but don't be afraid to mix things up and experiment if you feel like it. That's what config backups are for!

### Report any issues here on Github

This project uses the Github issue tracker. If you don't use GH and don't intend to, you can email me at philip@roaming-initiative.com, or find me on HypeIRC.

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
