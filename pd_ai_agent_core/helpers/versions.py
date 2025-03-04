import semver
import re
from dataclasses import dataclass
import logging
from typing import List

logger = logging.getLogger(__name__)


@dataclass
class VersionConstraint:
    operator: str  # >=, >, <, <=, =, ^, ~
    version: str


class VersionUtils:
    @staticmethod
    def parse_constraint(constraint: str) -> List[VersionConstraint]:
        """Parse version constraint string into structured format
        Examples:
        - Exact: 1.0.0
        - Greater than: >1.0.0
        - Greater than or equal: >=1.0.0
        - Less than: <2.0.0
        - Less than or equal: <=2.0.0
        - Range: >=1.0.0 <2.0.0
        - Caret (minor updates): ^1.0.0
        - Tilde (patch updates): ~1.0.0
        - Wildcard: 1.x or 1.x.x
        """
        if not constraint:
            return []

        # Handle wildcard patterns first
        if "x" in constraint.lower():
            # Convert 1.x or 1.x.x to ^1.0.0
            base = constraint.lower().replace("x", "0")
            return [VersionConstraint("^", base)]

        constraints = []
        # Split on spaces or commas
        parts = re.split(r"[\s,]+", constraint.strip())

        for part in parts:
            match = re.match(r"^([><=~^]|>=|<=)?(.+)$", part)
            if match:
                op, ver = match.groups()
                op = op or "="  # Default to exact match
                ver = ver.lstrip("v")

                # Validate version format
                try:
                    semver.VersionInfo.parse(ver)
                    constraints.append(VersionConstraint(op, ver))
                except ValueError:
                    logger.warning(f"Invalid version in constraint: {ver}")
                    continue

        return constraints

    @staticmethod
    def matches_constraint(version: str, constraint: str) -> bool:
        """Check if version matches constraint"""
        try:
            version = version.lstrip("v")
            # ver = semver.VersionInfo.parse(version)
            constraints = VersionUtils.parse_constraint(constraint)

            for c in constraints:
                if c.operator == "=":
                    if not semver.match(version, f"={c.version}"):
                        return False
                elif c.operator == "^":
                    if not semver.match(version, f"^{c.version}"):
                        return False
                elif c.operator == "~":
                    if not semver.match(version, f"~{c.version}"):
                        return False
                else:
                    if not semver.match(version, f"{c.operator}{c.version}"):
                        return False
            return True
        except ValueError:
            return False

    @staticmethod
    def compare_versions(v1: str, v2: str) -> int:
        """Compare two versions, handling v prefix"""
        v1 = v1.lstrip("v")
        v2 = v2.lstrip("v")
        return semver.compare(v1, v2)
