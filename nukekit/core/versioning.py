
from dataclasses import dataclass, field, asdict
import semver
from typing import Self


class Version():

    def __init__(self, version_string:str):
        ver = semver.Version.parse(version_string)
        self.major = ver.major
        self.minor = ver.minor
        self.patch = ver.patch

    def compare(self, other:Self):
        return (self.major, self.minor, self.patch) > \
               (other.major, other.minor, other.patch)




x = Version('1.1.0')
y = Version('1.1.1')

test = x.compare(y)
print(test)