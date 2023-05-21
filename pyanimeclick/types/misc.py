from dataclasses import dataclass

from .obj import Object

@dataclass
class Cover(Object):
    resolved: str
    original: str