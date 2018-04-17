#
# Copyright 2013 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from functools import partial
import tarfile

import matplotlib
from nose_parameterized import parameterized
import pandas as pd

from gateway import examples
from gateway.data.bundles import register, unregister
from gateway.testing import test_resource_path
from gateway.testing.fixtures import WithTmpDir, GatewayTestCase
from gateway.testing.predicates import assert_equal
from gateway.utils.cache import dataframe_cache
from gateway.utils.paths import update_modified_time


# Otherwise the next line sometimes complains about being run too late.
_multiprocess_can_split_ = False

matplotlib.use('Agg')


class ExamplesTests(WithTmpDir, GatewayTestCase):
    # some columns contain values with unique ids that will not be the same

    @classmethod
    def init_class_fixtures(cls):
        super(ExamplesTests, cls).init_class_fixtures()

        register('test', lambda *args: None)
        cls.add_class_callback(partial(unregister, 'test'))

        with tarfile.open(test_resource_path('example_data.tar.gz')) as tar:
            tar.extractall(cls.tmpdir.path)

        cls.expected_perf = dataframe_cache(
            cls.tmpdir.getpath(
                'example_data/expected_perf/%s' %
                pd.__version__.replace('.', '-'),
            ),
            serialization='pickle',
        )

        market_data = ('SPY_benchmark.csv', 'treasury_curves.csv')
        for data in market_data:
            update_modified_time(
                cls.tmpdir.getpath(
                    'example_data/root/data/' + data
                )
            )

    @parameterized.expand(sorted(examples.EXAMPLE_MODULES))
    def test_example(self, example_name):
        actual_perf = examples.run_example(
            example_name,
            # This should match the invocation in
            # gateway/tests/resources/rebuild_example_data
            environ={
                'GATEWAY_ROOT': self.tmpdir.getpath('example_data/root'),
            },
        )
        assert_equal(
            actual_perf[examples._cols_to_check],
            self.expected_perf[example_name][examples._cols_to_check],
            # There is a difference in the datetime columns in pandas
            # 0.16 and 0.17 because in 16 they are object and in 17 they are
            # datetime[ns, UTC]. We will just ignore the dtypes for now.
            check_dtype=False,
        )
