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

import re

from trep.vendor import xunitparser
from trep import itrr as test_result


def prepare_source(conf):
    return SourceXUnit(conf)


class SourceXUnit(object):

    def __init__(self, conf):
        self.filename = conf['filename']

    def get_itrr(self):
        filename = self.filename
        return self.get_itrr_by_filename(filename)

    @staticmethod
    def get_case_result(xunit_case):
        if xunit_case.success:
            return test_result.TEST_RESULT_PASS
        elif xunit_case.failed:
            return test_result.TEST_RESULT_FAIL
        elif xunit_case.skipped:
            return test_result.TEST_RESULT_SKIP
        elif xunit_case.errored:
            return test_result.TEST_RESULT_BLOCKED
            # return test_result.TEST_RESULT_ERROR
        else:
            return None

    def methodname2case(self, methodname):
        """Returns case name from test methodname
        For example if test name is
            "test_update_router_admin_state[id-a8902683-c788-4246-95c7-ad9c6d63a4d9]"
        it returns test_update_router_admin_state
        """
        rex = r'(?P<name>[a-zA-Z0-9_]*)\[?'
        result = re.search(rex, methodname)
        if result is not None:
            try:
                case_name = result.group('name')
                return str(case_name)
            except AttributeError:
                pass
        else:
            return None

    def get_itrr_by_filename(self, filename):
        itrr = test_result.ITRR()
        with open(filename) as f:
            for test_suite, tr in xunitparser.parse(f):
                ts = itrr.add_test_suite(test_suite.name)
                for xunit_case in test_suite:
                    tc = ts.add_test_case(self.methodname2case(xunit_case.methodname))
                    ti = tc.add_test_item(None)
                    result = SourceXUnit.get_case_result(xunit_case)
                    aux = {
                        'stdout': xunit_case.stdout,
                        'stderr': xunit_case.stderr,
                        'time': xunit_case.time,
                    }
                    ti.add_result(result, info=aux)
        return itrr
