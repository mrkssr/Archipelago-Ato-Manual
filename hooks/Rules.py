from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value
from BaseClasses import MultiWorld, CollectionState
from .. import Rules
    
import re

# Coin Rogue, Talisman Bandit, Talisman Black Piles Room, Talisman Yari, Checkpoint Yari, Coin Yari, Red Shard, Talisman Hidden, Talisman Fans, Mind Rune, Coin Phantom Jin, Fatal Draw Upgrade, Checkpoint Phantom Shin, Electric Wind Lethal Strike, Talisman Hidden Breakables, Talisman Owl, Talisman Lore Room, Coin Switch Puzzle, Talisman Warp Obstacles

# Skills
def dodge(multiworld: MultiWorld, state: CollectionState, player: int):
    """Has the player dodge ability?"""
    if not Rules.YamlEnabled(multiworld, player, "skills_shuffle"):
        return True

    return state.has("Dodge", player)

def dodge_upgrade(multiworld: MultiWorld, state: CollectionState, player: int):
    """Has the player dodge upgrade ability?"""
    if not Rules.YamlEnabled(multiworld, player, "skills_shuffle"):
        return True

    return state.has_all("Dodge", player)

def dash(multiworld: MultiWorld, state: CollectionState, player: int):
    """Has player dash ability?"""
    if not Rules.YamlEnabled(multiworld, player, "skills_shuffle"):
        return True

    if state.has("Dash", player):
        return True
    
    if logic_hard(multiworld, player) and (double_jump(state, player) and armor(state, player)):
        return True

    return False

def chain_dash(multiworld: MultiWorld, state: CollectionState, player: int):
    """Has the player chain dash ability?"""
    if not Rules.YamlEnabled(multiworld, player, "skills_shuffle"):
        return True

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
    if not Rules.YamlEnabled(multiworld, player, "skills_shuffle"):
        return True

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
    if not Rules.YamlEnabled(multiworld, player, "skills_shuffle"):
        return True

    if state.has("Double Jump", player):
        return True

    if logic_hard(multiworld, player) and (not state.has("Double Jump", player) and armor(state, player)):
        return True
    
    return False

def armor(multiworld: MultiWorld, state: CollectionState, player: int):
    """Has the player armor ability?"""
    if not Rules.YamlEnabled(multiworld, player, "skills_shuffle"):
        return True

    return state.has("Armor", player)

def spin(multiworld: MultiWorld, state: CollectionState, player: int):
    """Has the player spin ability?"""
    if not Rules.YamlEnabled(multiworld, player, "skills_shuffle"):
        return True

    return state.has("Spin", player)

def vision(multiworld: MultiWorld, state: CollectionState, player: int):
    if not Rules.YamlEnabled(multiworld, player, "skills_shuffle"):
        return True

    if state.has("vision", player):
        return True

    if logic_hard(multiworld, player):
        return True
    
    return False
# Skills Done

# Shards
def all_shards(multiworld: MultiWorld, state: CollectionState, player: int):
    """All all shards collected?"""
    if not Rules.YamlEnabled(multiworld, player, "shard_shuffle"):
        return True

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