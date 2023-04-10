from dataclasses import dataclass, field, asdict


@dataclass
class Window:
    top: int
    left: int
    width: int
    height: int
    pywindow: any

    @property
    def center(self) -> tuple[int, int]:
        return (self.left + (self.width / 2), self.top + self.height / 2)

    def asdict(self) -> dict:
        return asdict(self)


@dataclass
class Context:
    window: Window

    cast_time: float = 1.0

    equip_bait: bool = True
    equip_bait_max_tries: int = 3

    repair_tool: bool = True
    repair_tool_every: int = 30

    free_cam_key: str = "alt"
    move_directions: list[str] = field(default_factory=lambda: ["a", "d"])

    update_rate: int = 60

    runs: int = 0


class Images:
    FISH_BAIT = "imgs/fish_bait.png"
    FISH_REELING = "imgs/fish_reeling.png"
    FISH_REELING_WARN = "imgs/fish_reeling_warn.png"
    HOLD_CAST = "imgs/hold_cast.png"
    NO_BAIT = "imgs/no_bait.png"
