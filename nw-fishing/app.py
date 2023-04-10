import random
import window
import controller
from state import State, StateMachine, CacheState
from models import Context, Images

AppState = State[Context]


class StartingUp(AppState):
    def next(self, context: Context) -> AppState:
        controller.activate_window(context.window)
        controller.center_mouse(context.window)
        controller.time.sleep(2.5)

        return CheckingConditions()


@CacheState
class CheckingConditions(AppState):
    def next(self, context: Context) -> AppState:
        if window.locate(Images.HOLD_CAST) is None:
            return RepairingTool()

        if context.equip_bait and window.locate(Images.NO_BAIT, confidence=0.8):
            return TryEquipingBait()

        return CastingLine()


class TryEquipingBait(AppState):
    def __init__(self):
        self.tries = 0

    def next(self, context: Context) -> AppState:
        controller.equip_bait(context.window)

        if window.locate(Images.NO_BAIT, confidence=0.8) is None:
            return CheckingConditions()

        self.tries += 1

        if self.tries >= context.equip_bait_max_tries:
            context.equip_bait = False
            return CheckingConditions()

        return self


@CacheState
class CastingLine(AppState):
    def next(self, context: Context) -> AppState:
        controller.key_down(context.free_cam_key)
        controller.cast_line(context.cast_time)

        return WaitingForFishBait()


@CacheState
class WaitingForFishBait(AppState):
    def next(self, _: Context) -> AppState:
        if window.locate(Images.FISH_BAIT, confidence=0.75):
            controller.click()
            return ReelingFish()

        return self


@CacheState
class ReelingFish(AppState):
    def enter(self, *_):
        controller.mouse_down()

    def next(self, _: Context) -> AppState:
        if window.locate(Images.HOLD_CAST):
            return FinishingReeling()

        if window.locate(Images.FISH_REELING_WARN, confidence=0.65):
            return SlackingLine()

        return self

    def exit(self, *_):
        controller.mouse_up()


@CacheState
class SlackingLine(AppState):
    def next(self, _: Context) -> AppState:
        if window.locate(Images.HOLD_CAST):
            return FinishingReeling()

        if window.locate(Images.FISH_REELING, confidence=0.8):
            return ReelingFish()

        return self


@CacheState
class FinishingReeling(AppState):
    def next(self, context: Context):
        context.runs += 1

        controller.key_up(context.free_cam_key)

        if random.randint(1, 5) == 5:
            key = random.choice(context.move_directions)
            controller.key_down(key)
            controller.key_up(key)

        if context.repair_tool and not context.runs % context.repair_tool_every:
            return RepairingTool()

        return CheckingConditions()


@CacheState
class RepairingTool(AppState):
    def next(self, context: Context) -> AppState:
        controller.repair_tool(context.window)
        return CheckingConditions()


class Application(StateMachine[Context]):
    def __init__(self, context: Context):
        super().__init__(StartingUp(), context)

    def clean_up(self):
        controller.key_up(self.context.free_cam_key)

    def reset(self):
        self.state = StartingUp()
