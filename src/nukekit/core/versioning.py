from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Literal, Self

import semver

logger = logging.getLogger(__name__)

VERSION_CLASSES = Literal["major", "minor", "patch"]


@dataclass(order=True)
class Version:
    """_Semantic version implementation._

    Raises:
        ValueError: _description_
    """

    major: int
    minor: int
    patch: int

    @classmethod
    def from_string(cls, version_string):
        try:
            ver = semver.Version.parse(version_string)
        except ValueError as e:
            raise e
        return cls(ver.major, ver.minor, ver.patch)

    @classmethod
    def from_tuple(cls, version_tuple: tuple[int, int, int]) -> Self:
        return cls.from_string(".".join(str(val) for val in version_tuple))

    def version_up(self, type_name: VERSION_CLASSES):
        """
        Increment version number.

        Args:
            type_name: Type of version increment ('major', 'minor', or 'patch')
        """
        current_val = getattr(self, type_name)
        setattr(self, type_name, current_val + 1)

        if type_name == "major":
            self.minor = 0
            self.patch = 0
        elif type_name == "minor":
            self.patch = 0

    @classmethod
    def highest_version(cls, version_list: list[str | tuple | Version]) -> Version:
        """
        Returns highest version for a versions list

        :param version_list: List of versions to compare
        :type version_list: list[str | tuple | Version]
        :return: Highest version from list
        :rtype: Version
        """
        # Temp version as lowest possible
        version_list_obj = []
        for v in version_list:
            # Handle multiple cases
            if isinstance(v, str):
                version_list_obj.append(Version.from_string(v))
            elif isinstance(v, tuple):
                version_list_obj.append(Version.from_tuple(v))
            else:
                version_list_obj.append(v)

        latest = sorted(version_list_obj)[0]
        for v in version_list_obj:
            # Compare
            if v > latest:
                latest = v
        return latest

    def __repr__(self) -> str:
        return f"Version('{self}')"

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def __format__(self, format_spec):
        return str(self)

    def __hash__(self):
        return hash(str(self))
