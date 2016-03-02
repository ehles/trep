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

from trep.test_result import renderer
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestResultRenderer(unittest.TestCase):
    template = 'tests/data/result_renderer_template.tmpl'

    def test_item_one_test_suite(self):
        expected_result = "TestResult\n"\
            "==========\n"\
            "test name 'TestCaseName'\n"\
            "test results:\n"\
            "* test1\n"\
            "* test2\n"\
            "* test3"
        data = {
            'test_name': 'TestCaseName',
            'tests': ['test1', 'test2', 'test3']
        }
        r = renderer.ResultRenderer(self.template)
        result = r.render(**data)
        self.assertEqual(result, expected_result, 'Unexpected template value')

