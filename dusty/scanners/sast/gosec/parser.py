#!/usr/bin/python3
# coding=utf-8
# pylint: disable=I0011,W1401,E0401,R0914,R0915,R0912

#   Copyright 2019 getcarrier.io
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
    Bandit JSON parser
"""

from collections import namedtuple

from dusty.tools import log, markdown
from dusty.models.finding import SastFinding

from .legacy import GosecOutputParser
from . import constants


def parse_findings(data, scanner):
    """ Parse findings """
    # Parse JSON using legacy parser
    findings = GosecOutputParser(data).items
    # Make finding instances
    for item in findings:
        finding = SastFinding(
            title=item["title"],
            description=[
                "\n\n".join([
                    item['description'],
                    f"**File to review:** {markdown.markdown_escape(item['file_path'])}"
                ])
            ] + item["steps_to_reproduce"]
        )
        finding.set_meta("tool", scanner.get_name())
        finding.set_meta("severity", constants.GOSEC_SEVERITY_MAPPING[item["severity"]])
        finding.set_meta("legacy.file", item["file_path"])
        finding.set_meta("endpoints", [namedtuple("Endpoint", ["raw"])(raw=item["file_path"])])
        log.debug(f"Endpoints: {finding.get_meta('endpoints')}")
        scanner.findings.append(finding)
