# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from platformio.managers.platform import PlatformBase


class Ststm32Platform(PlatformBase):

    def configure_default_packages(self, variables, targets):
        board = variables.get("board")
        if "mbed" in variables.get("pioframework",
                                   []) or board == "mxchip_az3166":
            self.packages['toolchain-gccarmnoneeabi'][
                'version'] = ">=1.60301.0"

        if board == "mxchip_az3166":
            self.frameworks['arduino'][
                'package'] = "framework-arduinostm32mxchip"
            self.frameworks['arduino'][
                'script'] = "builder/frameworks/arduino/mxchip.py"

            self.packages['tool-openocd']['type'] = "uploader"

        return PlatformBase.configure_default_packages(self, variables,
                                                       targets)

    def board_config(self, id_):
        config = PlatformBase.board_config(self, id_)
        debug = config.manifest.get("debug", {})
        if "tools" not in debug:
            debug['tools'] = {}
        debug['tools']['blackmagic'] = {
            "hwids": [["0x1d50", "0x6018"]],
            "require_debug_port": True
        }
        config.manifest['debug'] = debug
        return config
