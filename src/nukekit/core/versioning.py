import semver
from typing import Self

class Version():
    def __init__(self, version_string:str):
        ver = semver.Version.parse(version_string)
        self.major = ver.major
        self.minor = ver.minor
        self.patch = ver.patch

    @classmethod
    def from_tuple(cls, version_tuple:tuple[int,int,int]):
        return cls('.'.join(str(val) for val in version_tuple))

    def __gt__(self, other:Self):
        return (self.major, self.minor, self.patch) > \
               (other.major, other.minor, other.patch)
    
    def __repr__(self):
        return str(f"{self.major}.{self.minor}.{self.patch}")
    
    def __str__(self):
        return str(f"{self.major}.{self.minor}.{self.patch}")
