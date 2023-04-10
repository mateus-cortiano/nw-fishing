from typing import Protocol, Self, Generic, TypeVar

T = TypeVar("T")


class State(Generic[T], Protocol):
    def enter(self, context: T, _from: Self | None = None):
        ...

    def next(self, context: T) -> Self:
        return State()

    def exit(self, context: T, to: Self):
        ...

    def __repr__(self):
        return f"State<{self.__class__.__name__}>"


class CacheState:
    _sentinel = object()

    def __init__(self, state: State[T]):
        self.state = state
        self.cache = {}

    def __call__(self, *args, **kwargs):
        key = args + (self._sentinel,) + tuple(sorted(kwargs.items()))

        if (instance := self.cache.get(key)) is None:
            instance = self.state(*args, **kwargs)
            self.cache.update({key: instance})

        return instance


class StateMachine(Generic[T]):
    def __init__(self, initial_state: State[T], context: T):
        self.state = initial_state
        self.context = context
        self.state.enter(context)

    def next(self):
        current_state = self.state
        next_state = current_state.next(self.context)

        if next_state is not current_state:
            current_state.exit(self.context, next_state)
            next_state.enter(self.context, current_state)

        self.state = next_state
