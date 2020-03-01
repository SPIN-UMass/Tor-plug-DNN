#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The obfs3 module implements the obfs3 protocol.
"""

import random

from twisted.internet import threads

import obfsproxy.transports.base as base

from  collections import deque
import obfsproxy.common.log as logging


log = logging.get_obfslogger()

HISTORY_LEN = 10
import time

class NNTransport(base.BaseTransport):
    

    def __init__(self):
        """Initialize the obfs3 pluggable transport."""
        super(NNTransport, self).__init__()
        self.sent_packets = deque(maxlen = HISTORY_LEN)
        self.rcvd_packets = deque(maxlen = HISTORY_LEN)

    def circuitConnected(self):
        

        log.debug("SOMEONE connected")



    def receivedUpstream(self, data):
        """
        Got data from upstream. We need to obfuscated and proxy them downstream.
        """
        message = data.read()
        log.debug("nn receivedUpstream: Transmitting %d bytes.", len(message))
        
        self.sent_packets.append((time.time(),len(message)))
        # Proxy encrypted message.
        self.circuit.downstream.write(message)

    def receivedDownstream(self, data):
        """
        Got data from downstream. We need to de-obfuscate them and
        proxy them upstream.
        """
        log.debug("nn receivedDownstream: Processing %d bytes of application data." %
                    len(data))

        self.rcvd_packets.append((time.time(),len(data)))
        
        log.debug(self.rcvd_packets)
        
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



