#
#  --------------------------------------------------------------------------
#   Gurux Ltd
#
#
#
#  Filename: $HeadURL$
#
#  Version: $Revision$,
#                   $Date$
#                   $Author$
#
#  Copyright (c) Gurux Ltd
#
# ---------------------------------------------------------------------------
#
#   DESCRIPTION
#
#  This file is a part of Gurux Device Framework.
#
#  Gurux Device Framework is Open Source software; you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 2 of the License.
#  Gurux Device Framework is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  More information of Gurux products: http://www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http://www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
import gurux_common.io.BaudRate
import gurux_common.io.Parity
import gurux_common.io.StopBits

###Python 2 requires this
# pylint: disable=bad-option-value,old-style-class,too-few-public-methods
class GXSettings:

    def __init__(self,
                 baudRate=gurux_common.io.BaudRate.BAUD_RATE_9600,
                 dataBits=8,
                 parity=gurux_common.io.Parity.NONE,
                 stopBits=gurux_common.io.StopBits.ONE):
        self.baudrate = baudRate
        self.dataBits = dataBits
        self.parity = parity
        self.stopBits = stopBits
