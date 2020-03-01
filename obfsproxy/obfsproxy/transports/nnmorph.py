#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The obfs3 module implements the obfs3 protocol.
"""

import random

import obfsproxy.common.aes as aes
import obfsproxy.transports.base as base
import obfsproxy.transports.obfs3_dh as obfs3_dh
import obfsproxy.common.log as logging
import obfsproxy.common.hmac_sha256 as hmac_sha256
import obfsproxy.common.rand as rand

from twisted.internet import threads

log = logging.get_obfslogger()

MAX_PADDING = 8194

PUBKEY_LEN = 192
KEYLEN = 16  # is the length of the key used by E(K,s) -- that is, 16.
HASHLEN = 32 # length of output of sha256

ST_WAIT_FOR_KEY = 0 # Waiting for public key from the other party
ST_WAIT_FOR_HANDSHAKE = 1 # Waiting for the DH handshake
ST_SEARCHING_MAGIC = 2 # Waiting for magic strings from the other party
ST_OPEN = 3 # obfs3 handshake is complete. Sending application data.

class NNTransport(base.BaseTransport):
    

    def __init__(self):
        """Initialize the obfs3 pluggable transport."""
        super(NNTransport, self).__init__()

    def circuitConnected(self):
        

        log.debug("SOMEONE connected")



    def receivedUpstream(self, data):
        """
        Got data from upstream. We need to obfuscated and proxy them downstream.
        """
        message = data.read()
        log.debug("nn receivedUpstream: Transmitting %d bytes.", len(message))

        # Proxy encrypted message.
        self.circuit.downstream.write(message)

    def receivedDownstream(self, data):
        """
        Got data from downstream. We need to de-obfuscate them and
        proxy them upstream.
        """
        log.debug("nn receivedDownstream: Processing %d bytes of application data." %
                    len(data))
        self.circuit.upstream.write(data.read())

    
class NNClient(NNTransport):

    """
    Obfs3Client is a client for the obfs3 protocol.
    The client and server differ in terms of their padding strings.
    """

    def __init__(self):
        NNTransport.__init__(self)

        
        self.we_are_initiator = True

class NNServer(NNTransport):

    """
    Obfs3Server is a server for the obfs3 protocol.
    The client and server differ in terms of their padding strings.
    """

    def __init__(self):
        NNTransport.__init__(self)

        
        self.we_are_initiator = False



