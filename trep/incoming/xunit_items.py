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

from trep.vendor import xunitparser
from trep import itrr as test_result
from trep.incoming.xunit import SourceXUnit


def prepare_source(conf):
    return SourceXUnitItems(conf)


class SourceXUnitItems(SourceXUnit):

    def __init__(self, conf):
        self.filename = conf['filename']
        self.case_name = conf['case_name']

    def get_itrr_by_filename(self, filename):
        itrr = test_result.ITRR()
        ts = itrr.add_test_suite(name='')
        with open(filename) as f:
            for test_suite, tr in xunitparser.parse(f):
                ts.name = test_suite.name
                # Here test_suite means test_case
                tc = ts.add_test_case(name=self.case_name)
                for xunit_case in test_suite:
                    ti = tc.add_test_item(xunit_case.methodname)
                    result = SourceXUnitItems.get_case_result(xunit_case)
                    aux = {
                        'stdout': xunit_case.stdout,
                        'stderr': xunit_case.stderr,
                        'time': xunit_case.time,
                    }
                    ti.add_result(result, info=aux)
        return itrr
