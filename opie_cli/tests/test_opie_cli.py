# Copyright 2016 Spanish National Research Council (CSIC)
# Copyright 2016 INDIGO-DataCloud
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

from opie_cli.osc.v1 import plugin

from openstackclient.compute.v2 import server
from openstackclient.tests.unit.compute.v2 import fakes as compute_fakes
from openstackclient.tests.unit.compute.v2 import test_server
from openstackclient.tests.unit.image.v2 import fakes as image_fakes


class TestServerCreate(test_server.TestServer):

    columns = (
        'OS-EXT-STS:power_state',
        'addresses',
        'flavor',
        'id',
        'image',
        'name',
        'networks',
        'properties',
    )

    def datalist(self):
        datalist = (
            server._format_servers_list_power_state(
                getattr(self.new_server, 'OS-EXT-STS:power_state')),
            '',
            self.flavor.name + ' (' + self.new_server.flavor.get('id') + ')',
            self.new_server.id,
            self.image.name + ' (' + self.new_server.image.get('id') + ')',
            self.new_server.name,
            self.new_server.networks,
            '',
        )
        return datalist

    def setUp(self):
        super(TestServerCreate, self).setUp()

        attrs = {
            'networks': {},
        }
        self.new_server = compute_fakes.FakeServer.create_one_server(
            attrs=attrs)

        # This is the return value for utils.find_resource().
        # This is for testing --wait option.
        self.servers_mock.get.return_value = self.new_server

        self.servers_mock.create.return_value = self.new_server

        self.image = image_fakes.FakeImage.create_one_image()
        self.images_mock.get.return_value = self.image

        self.flavor = compute_fakes.FakeFlavor.create_one_flavor()
        self.flavors_mock.get.return_value = self.flavor

        # Get the command object to test
        self.cmd = server.CreateServer(self.app, None)

    def test_create_preemptible(self):
        self.cmd = plugin.CreatePlugin(self.app, None)
        arglist = [
            '--image', 'image1',
            '--flavor', 'flavor1',
            self.new_server.name,
        ]
        verifylist = [
            ('image', 'image1'),
            ('flavor', 'flavor1'),
            ('config_drive', False),
            ('server_name', self.new_server.name),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # In base command class ShowOne in cliff, abstract method take_action()
        # returns a two-part tuple with a tuple of column names and a tuple of
        # data to be shown.
        columns, data = self.cmd.take_action(parsed_args)

        # Set expected values
        kwargs = dict(
            meta=None,
            files={},
            reservation_id=None,
            min_count=1,
            max_count=1,
            security_groups=[],
            userdata=None,
            key_name=None,
            availability_zone=None,
            block_device_mapping_v2=[],
            nics=[],
            scheduler_hints={"preemptible": 'True'},
            config_drive=None,
        )
        # ServerManager.create(name, image, flavor, **kwargs)
        self.servers_mock.create.assert_called_with(
            self.new_server.name,
            self.image,
            self.flavor,
            **kwargs
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.datalist(), data)
