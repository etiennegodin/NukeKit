from __future__ import annotations
import semver
from typing import Self, Literal

types = Literal['major', 'minor','patch']


class Version():
    def __init__(self, version_string:str):
        ver = semver.Version.parse(version_string)
        self.major = ver.major
        self.minor = ver.minor
        self.patch = ver.patch

    @classmethod
    def from_tuple(cls, version_tuple:tuple[int,int,int]):
        return cls('.'.join(str(val) for val in version_tuple))
    
    def version_up(self, type_name:types):
        """
        Docstring for version_up
        
        :param self: Description
        :param type_name: Description
        :type type_name: types
        """
        current_val = getattr(self,type_name)
        setattr(self,type_name, current_val+1)
        if type_name == 'major':
            self.minor = 0 
            self.patch = 0
        elif type_name == 'minor':
            self.patch = 0 

    def __gt__(self, other:Self):
        return (self.major, self.minor, self.patch) > \
               (other.major, other.minor, other.patch)
    
    def __repr__(self):
        return str(f"{self.major}.{self.minor}.{self.patch}")
    
    def __str__(self):
        return str(f"{self.major}.{self.minor}.{self.patch}")
