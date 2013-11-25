#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import queue

class MsgQueue(queue.Queue):
    """global message queue

    messages should always be a tuple
    where the first element should be the identifier
    """
    
    def __init__(self, maxsize):
        queue.Queue.__init__(self, maxsize)
        self.running = False
        self.callbacks = {}

    def add_callback(identifier, callback):
        self.callbacks[identifier] = callback

