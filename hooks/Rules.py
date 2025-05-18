from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value
from BaseClasses import MultiWorld, CollectionState
from .. import Rules
    
import re

# Skills
def dodge(state: CollectionState, player: int):
    """Has the player dodge ability?"""
    return state.has("Dodge", player)

def dodge_upgrade(state: CollectionState, player: int):
    """Has the player dodge upgrade ability?"""
    return state.has_all("Dodge", player)

def dash(multiworld: MultiWorld, state: CollectionState, player: int):
    """Has player dash ability?"""
    if state.has("Dash", player):
        return True
    
    if logic_hard(multiworld, player) and (double_jump(state, player) and armor(state, player)):
        return True

    return False

def chain_dash(multiworld: MultiWorld, state: CollectionState, player: int):
    """Has the player chain dash ability?"""
    if dash_state(state, player, 2):
        return True
    
    if logic_hard(multiworld, player) and \
        dash_state(state, player, 1) and \
        (
            armor(state, player) or
            double_jump(state, player) or
            spin(state, player) or
            dodge(state, player)
        ):
        return True
    
    return False

def chain_dash_upgrade(multiworld: MultiWorld, state: CollectionState, player: int):
    """Has the player the upgraded chain dash ability?"""
    if dash_state(state, player, 3):
        return True
    
    if logic_hard(multiworld, player) and \
        dash_state(state, player, 2) and \
        (
            armor(state, player) or
            double_jump(state, player) or
            spin(state, player) or
            dodge(state, player)
        ):
        return True
    
    return False

def dash_state(state: CollectionState, player: int, amount: str):
    """Which dash does the player have?"""
    return int(amount) <= state.count("Dash", player)

def double_jump(multiworld: MultiWorld, state: CollectionState, player: int):
    """Has the player double jump ability?"""
    if state.has("Double Jump", player):
        return True

    if logic_hard(multiworld, player) and (not state.has("Double Jump", player) and armor(state, player)):
        return True
    
    return False

def armor(state: CollectionState, player: int):
    """Has the player armor ability?"""
    return state.has("Armor", player)

def spin(state: CollectionState, player: int):
    """Has the player spin ability?"""
    return state.has("Spin", player)

def vision(multiworld: MultiWorld, state: CollectionState, player: int):
    if state.has("vision", player):
        return True

    if logic_hard(multiworld, player):
        return True
    
    return False
# Skills Done

# Shards
def all_shards(state: CollectionState, player: int):
    """All all shards collected?"""
    return state.has_all(["Blue Shard", "Red Shard", "Yellow Shard"], player)
# Shards Done

# Logic
def logic_normal(multiworld: MultiWorld, player: int):
    """Is normal logic active?"""
    return not logic_hard(multiworld, player)

def logic_hard(multiworld: MultiWorld, player: int):
    """Is hard logic active?"""
    return Rules.YamlEnabled(multiworld, player, "logic_hard")
# Logic Done

# Events
def prologue_done(state: CollectionState, player: int):
    """Post prologue environment"""
    return state.has("Prologue Done", player)

def is_prologue(state: CollectionState, player: int):
    """Prologue environment"""
    return not prologue_done(state, player)
# Events Done

# Examples - No Use
# Sometimes you have a requirement that is just too messy or repetitive to write out with boolean logic.
# Define a function here, and you can use it in a requires string with {function_name()}.
def overfishedAnywhere(world: World, state: CollectionState, player: int):
    """Has the player collected all fish from any fishing log?"""
    for cat, items in world.item_name_groups:
        if cat.endswith("Fishing Log") and state.has_all(items, player):
            return True
    return False

# You can also pass an argument to your function, like {function_name(15)}
# Note that all arguments are strings, so you'll need to convert them to ints if you want to do math.
def anyClassLevel(state: CollectionState, player: int, level: str):
    """Has the player reached the given level in any class?"""
    for item in ["Figher Level", "Black Belt Level", "Thief Level", "Red Mage Level", "White Mage Level", "Black Mage Level"]:
        if state.count(item, player) >= int(level):
            return True
    return False

# You can also return a string from your function, and it will be evaluated as a requires string.
def requiresMelee():
    """Returns a requires string that checks if the player has unlocked the tank."""
    return "|Figher Level:15| or |Black Belt Level:15| or |Thief Level:15|"
# Examples - No Use Done