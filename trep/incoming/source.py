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

from importlib import import_module

from trep.settings import get_conf, get_logger


class TrepSource(object):

    def __init__(self):
        self.source_name = get_conf()['test_results']['source']
        self.conf = {}
        try:
            self.source_mod = import_module(
                "trep.incoming.%s" % self.source_name)
        except ImportError:
            get_logger().error('Invalid source value: "%s"' % self.source_name)
            raise

        self.conf = get_conf()['test_results'].get(self.source_name, {})

    def get_itrr(self):
            return self.source_mod.prepare_source(self.conf).get_itrr()
