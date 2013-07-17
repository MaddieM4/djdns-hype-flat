djdns-hype-flat
===============

The resources to host DNS for the .hype domain using DJDNS and its file backend. Includes a scraper facility to import data from the HypeDNS API. Anything hosted on HypeDNS can be hosted with this instead, and it will be forward-compatible with DJDNS when the DEJE backend is worth using.

## Try out the public alpha now!

See DJDNS for instructions on how to use the public server for your DNS resolution:

http://github.com/campadrenalin/python-djdns#try-out-the-public-alpha-now

## How do I get my domain added to the .hype domain?

Ask nicely in an issue! Provide your information, or make a pull request with
the appropriate changes.

## I want to defer from my own instance of an alternative DNS.

Say you want to run your own Namecoin server and recursively request off of that, instead of a public server. First of all, you're awesome, that helps keep load down on public servers and likely strengthens whatever alternative network you're doing it for. Second, thanks to recent changes to DHF, you can do this without changing any of the existing page files (except a symlink).

### 1. Set up your alternative DNS server

Make sure it hosts on a different machine or port than your DJDNS instance, so that you're not both trying to bind to port 53 on the same IP address. This is pretty simple with virtualization (even using Linux Containers/Docker) because the virtual machine will have a different IP than your "real" host. If you're trying to host on the same machine, you need to configure the alt DNS port so that it doesn't collide.

### 2. Create a defer/local/mumble.json page file

You can basically copy it from an existing page and tweak things to point to your preferred host and port.

### 3. Create or change the relevant defer/mumble.json symlink

If you are hosting an alt DNS service that isn't part of mainstream DHF, this is easy. Just symlink from defer to defer/local:

```bash
$ cd defer
$ ln -s local/mumble.json mumble.json
```

If you are replacing an existing symlink, you'll have to delete the old one before creating the new one.

### 4. Add branch to root.json if necessary

This part is only necessary if DHF doesn't already support your alt DNS of choice. Basically, follow the existing examples to create another branch that points to your alt DNS with an appropriate regex and comment.

It's much preferred to add support to mainline DHF instead of maintaining it in custom configurations - everyone else would love to be able to resolve your obscure TLDs too! I'm happy to accept pull requests and recommendations. Long live alt DNS!
