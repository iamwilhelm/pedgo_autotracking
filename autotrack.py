from functools import wraps
from typing import Callable, Any, Set, Optional

# Global Revision State
CURRENT_REVISION: int = 0

# Tag Class for Tracking Revisions
class Tag:
    def __init__(self, name):
        global CURRENT_REVISION
        self.revision = CURRENT_REVISION
        self.name = name

def create_tag(name):
    return Tag(name)

# Callback when a tag is dirtied
on_tag_dirtied: Callable[[], None] = lambda: None

def set_on_tag_dirtied(callback: Callable[[], None]):
    global on_tag_dirtied
    on_tag_dirtied = callback

def dirty_tag(tag: Tag):
    global CURRENT_REVISION, current_computation
    if current_computation is not None and tag in current_computation:
        raise RuntimeError("Cannot dirty tag that has been used during a computation")

    CURRENT_REVISION += 1
    tag.revision = CURRENT_REVISION
    on_tag_dirtied()

# Tracking Dependencies
current_computation: Optional[Set[Tag]] = None

def consume_tag(tag: Tag):
    if current_computation is not None:
        current_computation.add(tag)

def get_max_revision(tags: Set[Tag]):
    return max((tag.revision for tag in tags), default=0)

# Memoization with Dependency Tracking
def memoize_function(fn: Callable[[], Any]) -> Callable[[], Any]:
    last_value: Optional[Any] = None
    last_revision: Optional[int] = None
    last_tags: Optional[Set[Tag]] = None

    @wraps(fn)
    def wrapper():
        nonlocal last_value, last_revision, last_tags
        global current_computation

        print("fn:", fn.__name__)
        if last_tags:
            print(", ".join(f"[{tag.name}]: {tag.revision}" for tag in last_tags))
        else:
            print("[]")

        if last_tags and get_max_revision(last_tags) == last_revision:
            if current_computation and last_tags:
                current_computation.update(last_tags)
            return last_value

        previous_computation = current_computation
        current_computation = set()

        try:
            last_value = fn()
            print("end ", fn.__name__)
        finally:
            last_tags = current_computation.copy()
            last_revision = get_max_revision(last_tags)

            if previous_computation and last_tags:
                previous_computation.update(last_tags)

            current_computation = previous_computation

        return last_value

    return wrapper

# Tracked Property Decorator
def tracked(initial_value=None):
    def decorator(fn):
        tags = {}
        values = {}

        @property
        def prop(self):
            if self not in values:
                values[self] = initial_value() if callable(initial_value) else initial_value
                tags[self] = create_tag(fn.__name__)

            consume_tag(tags[self])
            return values[self]

        @prop.setter
        def prop(self, value):
            values[self] = value
            if self not in tags:
                tags[self] = create_tag(fn.__name__)
            dirty_tag(tags[self])

        return prop

    return decorator
