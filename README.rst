============
vmod_ipcast
============

----------------------
Varnish ipcast Module
----------------------

:Author: Lasse Karstensen
:Date: 2016-04-29
:Version: 1.3
:Manual section: 3

SYNOPSIS
========

import ipcast;

DESCRIPTION
===========

This is a Varnish 3.0 VMOD for converting a string into an IP type
in VCL.

Note that previously this VMOD overwrote the ``client.ip`` internal
variable. This was an inherently flawed method and has since been abandoned.

For Varnish 4 use the built-in ``std.ip()`` function.

This VMOD is tested on Varnish 3.0.7.

FUNCTIONS
=========

ip
--

Prototype
        ::

                ip(STRING S, STRING fallback)
Return value
	IP

Description
	Parse the IPv4/IPv6 address in S and return that. If not successful, parse
	the string in fallback and return that.

	When parsing fails the getaddrinfo() error output will be logged to
	varnishlog.

	Caveat: If the fallback address is unparseable Varnish will crash.


        ::

                set req.http.xff = regsub(req.http.X-Forwarded-For, "^(^[^,]+),?.*$", "\1");
                if (ipcast.ip(req.http.xff, "198.51.100.255") == "198.51.100.255") { error 400 "Bad request"; }

                set resp.http.x-parsed-ip = ipcast.ip("2001:db8::1", "198.51.100.255");



INSTALLATION
============

The source tree is based on autotools to configure the building, and
does also have the necessary bits in place to do functional unit tests
using the varnishtest tool.

Usage::

 # only if you are building from a git clone.
 ./autogen.sh
 ./configure VARNISHSRC=DIR [VMODDIR=DIR]

`VARNISHSRC` is the directory of the Varnish source tree for which to
compile your vmod. Both the `VARNISHSRC` and `VARNISHSRC/include`
will be added to the include search paths for your module.

Optionally you can also set the vmod install directory by adding
`VMODDIR=DIR` (defaults to the pkg-config discovered directory from your
Varnish installation).

Make targets:

* make - builds the vmod
* make install - installs your vmod in `VMODDIR`
* make check - runs the unit tests in ``src/tests/*.vtc``

In your VCL you could then use this vmod along the following lines::

        import ipcast;
        acl friendly_network {
            "192.0.2.0"/24;
        }
        sub vcl_recv {
            set req.http.xff = regsub(req.http.X-Forwarded-For, "^(^[^,]+),?.*$", "\1");
            if (ipcast.ip(req.http.xff, "198.51.100.255") == "198.51.100.255") {
                error 400 "Bad request";
            }

            if (ipcast.ip(req.http.xff, "198.51.100.255") !~ friendly_network) {
                    error 403 "Forbidden";
            }
        }
COPYRIGHT
=========

This document is licensed under the same license as the
libvmod-ipcast project. See LICENSE for details.

* Copyright (c) 2011-2016 Varnish Software
