from __future__ import annotations
import semver
from typing import Self, Literal


"""
Major: Breaking changes (different inputs/outputs)
Minor: New features, backward compatible
Patch: Bug fixes
"""

class Version():
    
    classes = Literal['major', 'minor','patch']

    def __init__(self, version_string:str):
        try:
            ver = semver.Version.parse(version_string)
        except ValueError as e:
            raise e
            
        self.major = ver.major
        self.minor = ver.minor
        self.patch = ver.patch

    @classmethod
    def from_tuple(cls, version_tuple:tuple[int,int,int])->Self:
        return cls('.'.join(str(val) for val in version_tuple))
    
    def version_up(self, type_name:classes)->Self:
        """
        Docstring for version_up
        
        :param self: Description
        :param type_name: Description
        :type type_name: VERSION_ITEM
        """
        current_val = getattr(self,type_name)
        setattr(self,type_name, current_val+1)
        if type_name == 'major':
            self.minor = 1 
            self.patch = 0
        elif type_name == 'minor':
            self.patch = 0 
        return self

    def __gt__(self, other:Self):
        return (self.major, self.minor, self.patch) > \
               (other.major, other.minor, other.patch)
    
    def __eq__(self, other:Self):
        return (self.major == other.major and self.minor == other.minor and self.patch == other.patch)
    
    def __repr__(self):
        return str(f"{self.major}.{self.minor}.{self.patch}")
    
    def __str__(self):
        return str(f"{self.major}.{self.minor}.{self.patch}")
