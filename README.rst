============
vmod_ipcast
============

----------------------
Varnish ipcast Module
----------------------

:Author: Lasse Karstensen
:Date: 2013-07-17
:Version: 1.0
:Manual section: 3

SYNOPSIS
========

import ipcast;

DESCRIPTION
===========

This is a Varnish 3.0 VMOD for inserting a VCL string into
the client.ip internal variable.

FUNCTIONS
=========

clientip
--------

Prototype
        ::

                clientip(STRING S)
Return value
	VOID
Description
	Parse the IPv4/IPv6 address in S, and set that to client.ip.

        ::

                ipcast.clientip("192.168.0.10");

INSTALLATION
============

This is an ipcast skeleton for developing out-of-tree Varnish
vmods available from the 3.0 release. It implements the "Hello, World!" 
as a vmod callback. Not particularly useful in good hello world 
tradition,but demonstrates how to get the glue around a vmod working.

The source tree is based on autotools to configure the building, and
does also have the necessary bits in place to do functional unit tests
using the varnishtest tool.

Usage::

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
                if (req.http.X-Forwarded-For ~ ",") {
                        # NB: regex might need some improvement.
                        set req.http.xff = regsub(req.http.X-Forwarded-For,
                                "^[^,]+.?.?(.*)$", "\1"); }
                else { set req.http.xff = req.http.X-Forwarded-For; }
                ipcast.clientip(req.http.xff);

                if (client.ip !~ friendly_network) {
                        error 403 "Forbidden";
                }
        }

HISTORY
=======

This manual page was released as part of the libvmod-ipcast package,
demonstrating how to create an out-of-tree Varnish vmod.

COPYRIGHT
=========

This document is licensed under the same license as the
libvmod-ipcast project. See LICENSE for details.

* Copyright (c) 2011-2013 Varnish Software
