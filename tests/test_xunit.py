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

from trep.incoming import xunit
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestIncomingXUnit(unittest.TestCase):

    def test_item_one_test_suite(self):
        filename = 'tests/data/xunitresult_one_suite.xml'
        itrr = xunit.SourceXUnit.get_itrr(filename)

    def test_item_multi_test_suites(self):
        filename = 'tests/data/xunitresult_multi_suites.xml'
        itrr = xunit.SourceXUnit.get_itrr(filename)
