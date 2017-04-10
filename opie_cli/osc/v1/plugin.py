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

from openstackclient.compute.v2 import server
from openstackclient.i18n import _


class CreatePlugin(server.CreateServer):
    _description = _("Create a new preemptible instance.""")

    def take_action(self, parsed_args):
        if hasattr(parsed_args, "hint"):
            parsed_args.hint.append("preemptible=True")
        else:
            parsed_args.hint = ["preemptible=True"]
        return super(CreatePlugin, self).take_action(parsed_args)
