from __future__ import print_function

usage = """Usage:
python3 example-service.py &
python3 example-client.py
python3 example-async-client.py
python3 example-client.py --exit-service
"""

# Copyright (C) 2004-2006 Red Hat Inc. <http://www.redhat.com/>
# Copyright (C) 2005-2007 Collabora Ltd. <http://www.collabora.co.uk/>
#
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from gi.repository import GLib

import dbus
import dbus.service
import dbus.mainloop.glib

class DemoException(dbus.DBusException):
    _dbus_error_name = 'com.example.DemoException'

class SomeObject(dbus.service.Object):

    @dbus.service.method("org.freedesktop.fwupd.mockup",
                         in_signature='s', out_signature='as')
    def HelloWorld(self, hello_message):
        print("service:", str(hello_message))
        return ["Hello", " from example-service.py", "with unique name",
                session_bus.get_unique_name()]

    @dbus.service.method("org.freedesktop.fwupd.mockup",
                         in_signature='', out_signature='')
    def RaiseException(self):
        raise DemoException('The RaiseException method does what you might '
                            'expect')

    @dbus.service.method("org.freedesktop.fwupd.mockup",
                         in_signature='', out_signature='(ss)')
    def GetTuple(self):
        return ("Hello Tuple", " from example-service.py")

    @dbus.service.method("org.freedesktop.fwupd.mockup",
                         in_signature='', out_signature='a{ss}')
    def GetDict(self):
        return {"first": "Hello Dict", "second": " from example-service.py"}

    @dbus.service.method("org.freedesktop.fwupd.mockup",
                         in_signature='', out_signature='')
    def Exit(self):
        mainloop.quit()

    @dbus.service.method("org.freedesktop.fwupd.mockup",
                          in_signature='', out_signature='aa{sv}')
    def GetHostSecurityAttrs(self):
        print("Get fake attr!!")
        return [{"AppstreamId": "org.fwupd.hsi.Uefi.SecureBoot", "Name": "UEFI secure boot", "Flags": 1025},
                {"AppstreamId": "org.fwupd.hsi.Uefi.Pk", "Name": "UEFI platform key", "Flags": 1}]
        #return {}


# [Argument: a{sv} {"AppstreamId" = [Variant(QString): "org.fwupd.hsi.Uefi.SecureBoot"], 
# "Created" = [Variant(qulonglong): 1648435005], 
# "Name" = [Variant(QString): "UEFI secure boot"], 
# "Uri" = [Variant(QString): "https://fwupd.github.io/libfwupdplugin/hsi.html#org.fwupd.hsi.Uefi.SecureBoot"], 
# "Flags" = [Variant(qulonglong): 1024], 
# "HsiResult" = [Variant(uint): 2]}]

#[Argument: a{sv} {"AppstreamId" = [Variant(QString): "org.fwupd.hsi.Uefi.Pk"],
#  "Created" = [Variant(qulonglong): 1648435005],
#  "Name" = [Variant(QString): "UEFI platform key"],
#  "Uri" = [Variant(QString): "https://fwupd.github.io/libfwupdplugin/hsi.html#org.fwupd.hsi.Uefi.Pk"],
#  "Flags" = [Variant(qulonglong): 1],
#  "HsiLevel" = [Variant(uint): 1], 
# "HsiResult" = [Variant(uint): 3]}]

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    session_bus = dbus.SystemBus()
    name = dbus.service.BusName("org.freedesktop.fwupd.mockup", session_bus)
    object = SomeObject(session_bus, '/mockup')

    mainloop = GLib.MainLoop()
    print("Running example service.")
    print(usage)
    mainloop.run()