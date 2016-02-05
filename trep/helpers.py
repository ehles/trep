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

import os
from functools32 import lru_cache


@lru_cache()
def root_directory(application_path=None):
    root_path = application_path or os.path.dirname(__file__)
    while root_path and "bin" not in os.listdir(root_path):
        root_path = os.path.dirname(root_path)
    return root_path


@lru_cache()
def config_stage_directory():
    root_path = root_directory()
    return os.path.join(root_path, "configs")
