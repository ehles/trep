#    Copyright 2016 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import xunitparser



def get_itrr_from_xunit(filename):
    import os
    print os.getcwd()
    with open(filename) as f:
        ts, tr = xunitparser.parse(f)
        return ts, tr


def get_xunit_test_suite(filename):
    with open(filename) as f:
        ts, tr = xunitparser.parse(f)
        return ts, tr
