from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol


class Tier(str, Enum):
    HBM = "hbm"
    CPU = "cpu"
    NVME = "nvme"
    DROPPED = "dropped"


@dataclass
class KVStats:
    total_blocks: int
    free_blocks: int
    block_size: int


class KVBlockManagerAPI(Protocol):          # A builds, B calls
    def can_allocate(self, seq_id: str, n: int) -> bool: ...
    def allocate(self, seq_id: str, n: int) -> list[tuple[int, int]]: ...  # returns CoW copies
    def free(self, seq_id: str) -> None: ...
    def fork(self, parent: str, child: str) -> None: ...
    def slots(self, seq_id: str, start: int, end: int) -> list[int]: ...
    def num_tokens(self, seq_id: str) -> int: ...
    def move(self, seq_id: str, tier: Tier) -> None: ...        # week 5
    def prefetch(self, seq_id: str, deadline_s: float) -> None: ...  # week 6
    def stats(self) -> KVStats: ...


@dataclass
class StepOutput:                           # B builds, C reads
    ran: list[str]
    new_tokens: dict[str, int]
    finished: list[str]
    preempted: list[str] = field(default_factory=list)


@dataclass
class ToolCallStarted:                      # C emits, B reads
    session_id: str
    tool: str
    args: dict
    t: float


@dataclass
class ToolCallFinished:
    session_id: str
    tool: str
    latency_s: float
    t: float