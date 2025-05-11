from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value
from BaseClasses import MultiWorld, CollectionState
from .. import Rules
    
import re

# Skills
def dodge(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Has the player dodge ability?"""
    return state.has("Dodge", player)

def dodge_upgrade(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Has the player dodge upgrade ability?"""
    return state.has_all("Dodge", player)

def dash(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Has player dash ability?"""
    if state.has("Dash", player):
        return True
    
    if logic_hard(world, multiworld, state, player) and (double_jump(world, multiworld, state, player) and armor(world, multiworld, state, player)):
        return True

    return False

def chain_dash(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Has the player chain dash ability?"""
    if dash_state(world, multiworld, state, player, 2):
        return True
    
    if logic_hard(world, multiworld, state, player) and \
        dash_state(world, multiworld, state, player, 1) and \
        (
            armor(world, multiworld, state, player) or
            double_jump(world, multiworld, state, player) or
            spin(world, multiworld, state, player) or
            dodge(world, multiworld, state, player)
        ):
        return True
    
    return False

def chain_dash_upgrade(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Has the player the upgraded chain dash ability?"""
    if dash_state(world, multiworld, state, player, 3):
        return True
    
    if logic_hard(world, multiworld, state, player) and \
        dash_state(world, multiworld, state, player, 2) and \
        (
            armor(world, multiworld, state, player) or
            double_jump(world, multiworld, state, player) or
            spin(world, multiworld, state, player) or
            dodge(world, multiworld, state, player)
        ):
        return True
    
    return False

def dash_state(world: World, multiworld: MultiWorld, state: CollectionState, player: int, amount: str):
    """Which dash does the player have?"""
    return int(amount) <= state.count("Dash", player)

def double_jump(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Has the player double jump ability?"""
    if state.has("Double Jump", player):
        return True

    if logic_hard(world, multiworld, state, player) and (not state.has("Double Jump", player) and armor(world, multiworld, state, player)):
        return True
    
    return False

def armor(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Has the player armor ability?"""
    return state.has("Armor", player)

def spin(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Has the player spin ability?"""
    return state.has("Spin", player)

def vision(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    if state.has("vision", player):
        return True

    if logic_hard(world, multiworld, state, player):
        return True
    
    return False
# Skills Done

# Shards
def all_shards(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """All all shards collected?"""
    return state.has_all(["Blue Shard", "Red Shard", "Yellow Shard"], player)
# Shards Done

# Logic
def logic_normal(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Is normal logic active?"""
    return not logic_hard(world, multiworld, state, player)

def logic_hard(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Is hard logic active?"""
    return Rules.YamlEnabled(world, multiworld, state, player, "logic_hard")
# Logic Done

# Events
def prologue_done(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Post prologue environment"""
    return False

def is_prologue(world: World, multiworld: MultiWorld, state: CollectionState, player: int):
    """Prologue environment"""
    return not prologue_done(world, multiworld, state, player)
# Events Done
