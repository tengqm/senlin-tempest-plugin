# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from tempest.lib import decorators

from senlin.tests.tempest.api import base
from senlin.tests.tempest.api import utils


class TestClusterPolicy(base.BaseSenlinTest):

    def setUp(self):
        super(TestClusterPolicy, self).setUp()
        profile_id = utils.create_a_profile(self)
        self.addCleanup(utils.delete_a_profile, self, profile_id)

        self.cluster_id = utils.create_a_cluster(self, profile_id)
        self.addCleanup(utils.delete_a_cluster, self, self.cluster_id)

        self.policy_id = self.create_test_policy()['id']
        self.addCleanup(self.client.delete_obj, 'policies', self.policy_id)

        self.attach_policy(self.cluster_id, self.policy_id)
        self.addCleanup(self.detach_policy, self.cluster_id, self.policy_id)

    @decorators.idempotent_id('ebaeedcb-7198-4997-9b9c-a8f1eccfc2a6')
    def test_cluster_policy_list(self):
        res = self.client.list_cluster_policies(self.cluster_id)

        # Verify resp of cluster policy list API
        self.assertEqual(200, res['status'])
        self.assertIsNone(res['location'])
        self.assertIsNotNone(res['body'])
        policies = res['body']
        self.assertEqual(1, len(policies))
        for key in ['cluster_id', 'cluster_name', 'enabled', 'id',
                    'policy_id', 'policy_name', 'policy_type']:
            self.assertIn(key, policies[0])
        self.assertEqual(self.policy_id, policies[0]['policy_id'])

    @decorators.idempotent_id('fdf4dbf9-fcc6-4eb0-96c1-d8e8caa90f6d')
    def test_cluster_policy_show(self):
        res = self.client.get_cluster_policy(self.cluster_id, self.policy_id)

        # Verify resp of cluster policy show API
        self.assertEqual(200, res['status'])
        self.assertIsNone(res['location'])
        self.assertIsNotNone(res['body'])
        policy = res['body']
        for key in ['cluster_id', 'cluster_name', 'id', 'policy_id',
                    'policy_name', 'policy_type', 'enabled']:
            self.assertIn(key, policy)
        self.assertEqual(self.policy_id, policy['policy_id'])
