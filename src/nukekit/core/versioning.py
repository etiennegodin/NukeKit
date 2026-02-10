from __future__ import annotations
import semver
import logging
from dataclasses import dataclass
from typing import Self, Literal

logger = logging.getLogger(__name__)

VERSION_CLASSES = Literal["major", "minor","patch"]

@dataclass(frozen=True, order=True)
class Version():
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
    def from_tuple(cls, version_tuple:tuple[int,int,int]) -> Self:
        return cls(".".join(str(val) for val in version_tuple))
    
    def version_up(self, type_name:VERSION_CLASSES):
        """
        Docstring for version_up
        
        :param self: Description
        :param type_name: Description
        :type type_name: VERSION_ITEM
        """
        current_val = getattr(self,type_name)
        setattr(self,type_name, current_val+1)

        if type_name == "major":
            self.minor = 0 
            self.patch = 0
        elif type_name == "minor":
            self.patch = 0 

    @classmethod
    def highest_version(cls, version_list: list[str|tuple|Version]) -> Version:
        """
        Returns highest version for a versions list 

        :param version_list: List of versions to compare
        :type version_list: list[str | tuple | Version]
        :return: Highest version from list
        :rtype: Version
        """
        # Temp version as lowest possible
        latest = Version.from_string("0.0.0")
        for v in version_list:
            #Handle multiple cases
            if isinstance(v, str):
                v = Version(v)
            if isinstance(v, tuple):
                v = Version.from_tuple(v)
                
            # Compare
            if v > latest:
                latest = v
        return latest
    
    def __repr__(self) -> str:
        return f"Version('{self}')"
    
    def __str__(self):
        return (f"{self.major}.{self.minor}.{self.patch}")

    def __format__(self, format_spec):
        return str(self)
            
