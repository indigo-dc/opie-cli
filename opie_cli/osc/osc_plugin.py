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

from osc_lib import utils

API_NAME = 'opie'
API_VERSION_OPTION = 'opie_api_version'
DEFAULT_API_VERSION = '1'
API_VERSIONS = {
    '1': 'opie_cli.v1.client.Client',
}


def make_client(instance):
    """Returns a client to the ClientManager."""
    pass


def build_option_parser(parser):
    """Hook to add global options.

    Called from openstackclient.shell.OpenStackShell.__init__()
    after the builtin parser has been initialized.  This is
    where a plugin can add global options such as an API version setting.

    :param argparse.ArgumentParser parser: The parser object that has been
        initialized by OpenStackShell.
    """

    parser.add_argument(
        '--os-opie-api-version',
        metavar='<opie-api-version>',
        default=utils.env('OS_OPIE_API_VERSION',
                          default=DEFAULT_API_VERSION),
        help='OPIE API version, default=' +
             DEFAULT_API_VERSION +
             ' (Env: OS_OPIE_API_VERSION)')

    return parser
