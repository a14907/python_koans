#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: Create a Proxy Class
#
# In this assignment, create a proxy class (one is started for you
# below).  You should be able to initialize the proxy object with any
# object.  Any attributes called on the proxy object should be forwarded
# to the target object.  As each attribute call is sent, the proxy should
# record the name of the attribute sent.
#
# The proxy class is started for you.  You will need to add a method
# missing handler and any other supporting methods.  The specification
# of the Proxy class is given in the AboutProxyObjectProject koan.

# Note: This is a bit trickier than its Ruby Koans counterpart, but you
# can do it!

from typing import Any
from runner.koan import *


class Proxy:
    def __init__(self, target_object):
        # WRITE CODE HERE

        # initialize '_obj' attribute last. Trust me on this!
        self._obj = target_object 
        self._messages = dict() 
        
    def __getattribute__(self, __name: str) -> Any:
        if __name == '_obj':
            return super().__getattribute__(__name)   
        if __name == '_messages':
            return super().__getattribute__(__name)  
        if __name == 'was_called':
            return lambda name: name in self._messages
        if __name == 'number_of_times_called':
            return lambda name: self._messages[name] if name in self._messages else 0
        
        if __name == 'messages':
            return lambda: [k for (k,v) in self._messages.items()]
        
        dic = self._messages
        Proxy.countCall(dic, __name)
        
        return self._obj.__getattribute__(__name)
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == '_obj' or __name == '_messages' :
            return super().__setattr__(__name, __value)
        
        dic = self._messages
        Proxy.countCall(dic, __name)
        
        return self._obj.__setattr__(__name, __value)
    
    @staticmethod
    def countCall(dic,name):
        if name in dic:
            dic[name]+=1
        else:
            dic[name]=1


# The proxy object should pass the following Koan:
#
class AboutProxyObjectProject(Koan):
    def test_proxy_method_returns_wrapped_object(self):
        # NOTE: The Television class is defined below
        tv = Proxy(Television())

        self.assertTrue(isinstance(tv, Proxy))

    def test_tv_methods_still_perform_their_function(self):
        tv = Proxy(Television())

        tv.channel = 10
        tv.power()

        self.assertEqual(10, tv.channel)
        self.assertTrue(tv.is_on())

    def test_proxy_records_messages_sent_to_tv(self):
        tv = Proxy(Television())

        tv.power()
        tv.channel = 10

        self.assertEqual(["power", "channel"], tv.messages())

    def test_proxy_handles_invalid_messages(self):
        tv = Proxy(Television())

        with self.assertRaises(AttributeError):
            tv.no_such_method()

    def test_proxy_reports_methods_have_been_called(self):
        tv = Proxy(Television())

        tv.power()
        tv.power()

        self.assertTrue(tv.was_called("power"))
        self.assertFalse(tv.was_called("channel"))

    def test_proxy_counts_method_calls(self):
        tv = Proxy(Television())

        tv.power()
        tv.channel = 48
        tv.power()

        self.assertEqual(2, tv.number_of_times_called("power"))
        self.assertEqual(1, tv.number_of_times_called("channel"))
        self.assertEqual(0, tv.number_of_times_called("is_on"))

    def test_proxy_can_record_more_than_just_tv_objects(self):
        proxy = Proxy("Py Ohio 2010")

        result = proxy.upper()

        self.assertEqual("PY OHIO 2010", result)

        result = proxy.split()

        self.assertEqual(["Py", "Ohio", "2010"], result)
        self.assertEqual(["upper", "split"], proxy.messages())


# ====================================================================
# The following code is to support the testing of the Proxy class.  No
# changes should be necessary to anything below this comment.

# Example class using in the proxy testing above.
class Television:
    def __init__(self):
        self._channel = None
        self._power = None

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        self._channel = value

    def power(self):
        if self._power == "on":
            self._power = "off"
        else:
            self._power = "on"

    def is_on(self):
        return self._power == "on"


# Tests for the Television class.  All of theses tests should pass.
class TelevisionTest(Koan):
    def test_it_turns_on(self):
        tv = Television()

        tv.power()
        self.assertTrue(tv.is_on())

    def test_it_also_turns_off(self):
        tv = Television()

        tv.power()
        tv.power()

        self.assertFalse(tv.is_on())

    def test_edge_case_on_off(self):
        tv = Television()

        tv.power()
        tv.power()
        tv.power()

        self.assertTrue(tv.is_on())

        tv.power()

        self.assertFalse(tv.is_on())

    def test_can_set_the_channel(self):
        tv = Television()

        tv.channel = 11
        self.assertEqual(11, tv.channel)
