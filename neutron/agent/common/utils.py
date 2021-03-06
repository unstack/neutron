# Copyright 2015 Cloudbase Solutions.
# All Rights Reserved.
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

from oslo_config import cfg
from oslo_log import log as logging
from oslo_utils import timeutils

from neutron.common import utils as neutron_utils
from neutron.conf.agent import common as config
from neutron.conf.agent.database import agents_db


if os.name == 'nt':
    from neutron.agent.windows import utils
else:
    from neutron.agent.linux import utils


LOG = logging.getLogger(__name__)
config.register_root_helper(cfg.CONF)
agents_db.register_agent_opts()

INTERFACE_NAMESPACE = 'neutron.interface_drivers'


execute = utils.execute


def load_interface_driver(conf):
    """Load interface driver for agents like DHCP or L3 agent.

    :param conf: driver configuration object
    :raises SystemExit of 1 if driver cannot be loaded
    """

    try:
        loaded_class = neutron_utils.load_class_by_alias_or_classname(
                INTERFACE_NAMESPACE, conf.interface_driver)
        return loaded_class(conf)
    except ImportError:
        LOG.error("Error loading interface driver '%s'",
                  conf.interface_driver)
        raise SystemExit(1)


def is_agent_down(heart_beat_time):
    return timeutils.is_older_than(heart_beat_time,
                                   cfg.CONF.agent_down_time)
