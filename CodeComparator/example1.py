from __future__ import annotations

from typing import Optional


class petrinet_Petrinet:
    """Class petrinet::Petrinet."""

    def __init__(self, name: str) -> None:
        self.name: str = name


class petrinet_Arc:
    """Class petrinet::Arc."""

    def __init__(self, weight: int) -> None:
        self.weight: int = weight


class petrinet_Token:
    """Class petrinet::Token."""

    def __init__(self) -> None:
        pass


class petrinet_PTArc(Arc):
    """Class petrinet::PTArc."""

    def __init__(self) -> None:
        super().__init__()


class petrinet_Place:
    """Class petrinet::Place."""

    def __init__(self, name: str) -> None:
        self.name: str = name

    def isAPart(self) -> bool:
        pass

    def getTokenNumber(self) -> int:
        pass


class petrinet_Transition:
    """Class petrinet::Transition."""

    def __init__(self, name: str) -> None:
        self.name: str = name

    def isEnabled(self) -> bool:
        pass


class Arc:
    """Class Arc."""

    def __init__(self) -> None:
        pass


class petrinet_TPArc(Arc):
    """Class petrinet::TPArc."""

    def __init__(self) -> None:
        super().__init__()