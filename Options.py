from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions, Range, OptionCounter

class Difficulty(Choice):
    """Difficulty. Default Easy.
    Easy: Easy Settings
    Normal: Normal Settings
    Hard: Hard Settings
    """
    display_name = "Difficulty"
    option_easy = 0
    option_normal = 1
    option_hard = 2

class AdjacencyOdds(Range):
    """The chances that the map will need to warp to the next location. Default 3.
    """
    range_start = 1
    range_end = 10
    default = 3

class BranchingOdds(Range):
    """The chances that the map will branch out. Default 5.
    """
    range_start = 1
    range_end = 10
    default = 5

class CardsPerRegion(Range):
    """The number of cards that each region has. Default 20.
    """
    range_start = 5
    range_end = 100
    default = 20

class MapRadius(Range):
    """The radius of the map generated. Default 25.
    """
    range_start = 20
    range_end = 100
    default = 25

class TrapReleasePercent(Range):
    """The odds that a trap will release itself at the end of a battle. Default 13.
    """
    range_start = 0
    range_end = 100
    default = 13

class TilesPerPip(Range):
    """How many map tiles need to spawn for 1 map pip to spawn. Default 25.
    9 = 1 Tile Radius of buffer space
    25 = 2 Tile Radius of buffer space
    49 = 3 Tile Radius of buffer space
    81 = 4 Tile Radius of buffer space
    """
    range_start = 9
    range_end = 100

    one_radius = 9
    two_radius = 25
    three_radius = 49
    four_radius = 81
    
    default = 25

class NodePercentages(OptionCounter):
    """The percentage of various map nodes. Must add up to 100.
    Home will add an extra node to the location you spawn at.
    There will always be 1 boss.
    Warps only acount for non-vital warp points.
    Obstacles are not implimented yet.

    Auto:           A point you travel along instantly. Add path texture.   Default 05%
    Intersection:   A free point. Usually used for intersections.           Default 15%
    Shop:           A location to turn money into cards and items.          Default 05%
    Treasure:       An instant reward is at this location.                  Default 05%
    Release Altar:  Release cards to pass this locaiton.                    Default 05%
    Warp:           Internal/shortcut warp. 2 nodes for the price of 1.     Default 05%
    Event:          A choice or minigame that can boost or hinder you.      Default 10%
    Enemy:          Enemy cards which must be defeated to pass.             Default 40%
    """
    min = 0
    max = 100
    default = {
        "Auto" : 5,
        "Intersection" : 15,
        "Shop" : 5,
        "Treasure" : 5,
        "Releaser" : 5,
        "Warp" : 5,
        "Event" : 10,
        "Enemy" : 40
    }

class ItemPercentages(OptionCounter):
    """The percentage of non-core items.
    Filler:
    Default Card:       A statless 1/1 unreleasable card.                                               Default 00%
	Money:              10 dollars.                                                                     Default 00%
    Booster Pack:       A pack of 3 cards, giving you 1 choice from it.                                 Default 00%
    Perk:               A random perk.                                                                  Default 00%
    Random Card         A random card from your cardpool.
    Scout		        Scouts 1 location in your game. Picks unaccessable cards first.
    Shield	            Protects you from the next incoming trap.
    Treasure	        Starts a treasure event.
    Burger              Burger.
    Extra Life          Lets you lose a battle without losing your deck.

    Useful:
    Ghost Stamp:        A stamp that makes a released card able to show up again.                       Default 00%
    Harmony Stamp:      A stamp that befriends an enemy card.                                           Default 00%
    Square Stamp:       A stamp that makes a card boost up 1 square step.                               Default 00%
    Steel Stamp:        A stamp that prevents a card from self-releasing.                               Default 00%
    Gold Stamp:         A stamp that lets you release a card at any time for a treasure encounter.      Default 00%
    House Upgrade:      Start with more items upon death.                                               Default 00%

    Trap:
    Unstable Trap:      Every trap card you own has a 50% chance of releasing.                          Default 00%
    Fog Trap:           You can't see the enemies in your next battle.                                  Default 00%
    Release Trap:       A random card you own will be released.                                         Default 00%
    Trade Down Trap:    Your highest quality card will be exchanged for one of a lower quality.         Default 00%
    Stackless Trap:     You can't stack cards in your next battle.                                      Default 00%
    Blind Trap:         You can't see what cards are available in your next shop, event or treasure.    Default 00%
    """
    min = 0
    max = 100
    default = {
        #52%
        "Default Card"      :   13,
        "Money"             :   13,
        "Booster Pack"      :   13,
        "Perk"              :   13,
        "Random Card"		:   0,
        "Scout"				:   0,
        "Shield"			:   0,
        "Treasure"			:   0,
        "Burger"			:   0,
        "Extra Life"		:   0,
        
        #30%
        "Ghost Stamp"       :   5,
        "Harmony Stamp"     :   5,
        "Square Stamp"      :   5,
        "Steel Stamp"       :   5,
        "Gold Stamp"        :   5,
        "House Upgrade"     :   5,
        
        #18%
        "Unstable Trap"     :   3,
        "Fog Trap"          :   3,
        "Release Trap"      :   3,
        "Trade Down Trap"   :   3,
        "Stackless Trap"    :   3,
        "Blind Trap"        :   3
    }

@dataclass
class CardelagoOptions(PerGameCommonOptions):
    difficulty : Difficulty
    adjacency_odds : AdjacencyOdds
    branching_odds : BranchingOdds
    cards_per_region : CardsPerRegion
    map_radius : MapRadius
    tiles_per_pip : TilesPerPip
    node_percentages : NodePercentages
    item_percentages : ItemPercentages
    trap_release_chance : TrapReleasePercent
