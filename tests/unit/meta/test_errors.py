# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2017-2019 Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from testtools.matchers import Equals

from snapcraft.internal.meta import errors
from tests import unit


class ErrorFormattingTestCase(unit.TestCase):

    scenarios = (
        (
            "MissingSnapcraftYamlKeysError",
            {
                "exception": errors.MissingSnapcraftYamlKeysError,
                "kwargs": {"keys": ["test-key1", "test-key2"]},
                "expected_message": (
                    "Failed to generate snap metadata: "
                    "Missing required key(s) in snapcraft.yaml: "
                    "'test-key1' and 'test-key2'. Either specify the missing "
                    "key(s), or use 'adopt-info' to get them from a part."
                ),
            },
        ),
        (
            "AdoptedPartMissingError",
            {
                "exception": errors.AdoptedPartMissingError,
                "kwargs": {"part": "test-part"},
                "expected_message": (
                    "Failed to generate snap metadata: "
                    "'adopt-info' refers to a part named 'test-part', but it is "
                    "not defined in the 'snapcraft.yaml' file."
                ),
            },
        ),
        (
            "AdoptedPartNotParsingInfo",
            {
                "exception": errors.AdoptedPartNotParsingInfo,
                "kwargs": {"part": "test-part"},
                "expected_message": (
                    "Failed to generate snap metadata: "
                    "'adopt-info' refers to part 'test-part', but that part is "
                    "lacking the 'parse-info' property."
                ),
            },
        ),
        (
            "AmbiguousPassthroughKeyError",
            {
                "exception": errors.AmbiguousPassthroughKeyError,
                "kwargs": {"keys": ["key1", "key2"]},
                "expected_message": (
                    "Failed to generate snap metadata: "
                    "The following keys are specified in their regular location "
                    "as well as in passthrough: 'key1' and 'key2'. "
                    "Remove duplicate keys."
                ),
            },
        ),
        (
            "InvalidAppCommandError",
            {
                "exception": errors.InvalidAppCommandError,
                "kwargs": {"command": "test-command", "app_name": "test-app"},
                "expected_message": (
                    "Failed to generate snap metadata: "
                    "The specified command 'test-command' defined in the app "
                    "'test-app' does not exist or is not executable.\n"
                    "Ensure that 'test-command' is installed with the correct path."
                ),
            },
        ),
        (
            "InvalidAppCommandNotFound",
            {
                "exception": errors.InvalidAppCommandNotFound,
                "kwargs": {"command": "test-command", "app_name": "test-app"},
                "expected_message": (
                    "Failed to generate snap metadata: "
                    "The specified command 'test-command' defined in the app "
                    "'test-app' does not exist.\n"
                    "Ensure that 'test-command' is installed with the correct path."
                ),
            },
        ),
        (
            "InvalidAppCommandNotExecutable",
            {
                "exception": errors.InvalidAppCommandNotExecutable,
                "kwargs": {"command": "test-command", "app_name": "test-app"},
                "expected_message": (
                    "Failed to generate snap metadata: "
                    "The specified command 'test-command' defined in the app "
                    "'test-app' is not executable."
                ),
            },
        ),
        (
            "InvalidAppCommandFormatError",
            {
                "exception": errors.InvalidAppCommandFormatError,
                "kwargs": {"command": "test-command", "app_name": "test-app"},
                "expected_message": (
                    "Failed to generate snap metadata: "
                    "The specified command 'test-command' defined in the app "
                    "'test-app' does not match the pattern expected by snapd.\n"
                    "The command must consist only of alphanumeric characters, spaces, "
                    "and the following special characters: / . _ # : $ -"
                ),
            },
        ),
        (
            "InvalidCommandChainError",
            {
                "exception": errors.InvalidCommandChainError,
                "kwargs": {"item": "test-chain", "app_name": "test-app"},
                "expected_message": (
                    "Failed to generate snap metadata: "
                    "The command-chain item 'test-chain' defined in the app 'test-app' "
                    "does not exist or is not executable.\n"
                    "Ensure that 'test-chain' is relative to the prime directory."
                ),
            },
        ),
        (
            "InvalidDesktopFileError",
            {
                "exception": errors.InvalidDesktopFileError,
                "kwargs": {"filename": "test-file", "message": "test-message"},
                "expected_message": (
                    "Failed to generate desktop file: "
                    "Invalid desktop file 'test-file': test-message."
                ),
            },
        ),
    )

    def test_error_formatting(self):
        self.assertThat(
            str(self.exception(**self.kwargs)), Equals(self.expected_message)
        )
