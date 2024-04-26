from abc import ABC, abstractmethod

from duplicate_oid import DuplicateOid
from duplicate_email import DuplicateEmail

class IdentifiedObject(ABC):
    def __init__(self, oid):
        self._oid = oid

    @property
    def oid(self):
        return self._oid

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.oid == other.oid

    def __hash__(self):
        return hash(self.oid)



