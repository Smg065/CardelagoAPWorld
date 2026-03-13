from typing import NamedTuple

#Cardelago
BASE_ID			= 6500000
#Color IDs
RED_ID			=   10000
GREEN_ID		=   20000
VIOLET_ID		=   30000
ORANGE_ID		=   40000
BLUE_ID			=   50000
YELLOW_ID		=   60000
#Item Flags IDs
FILLER_ID		=    0000
USEFUL_ID		=    1000
PROGRESS_ID		=    2000
PROGUSEFUL_ID	=    3000
TRAP_ID			=    4000


class ItemData(NamedTuple):
	acid: int|None = None
	qty: int = 0
	type: str = ""
	default_location: str = ""

# 65X0XXX
filler_table = {
	"Default Card"			:	ItemData(BASE_ID + FILLER_ID, -1, "Filler", ""),
	"Money"					:	ItemData(BASE_ID + FILLER_ID + 1, -1, "Filler", ""),
	"Booster Pack"			:	ItemData(BASE_ID + FILLER_ID + 2, -1, "Filler", ""),
	"Perk"					:	ItemData(BASE_ID + FILLER_ID + 3, -1, "Filler", ""),
	"Random Card"			:	ItemData(BASE_ID + FILLER_ID + 4, -1, "Filler", ""),
	"Scout"					:	ItemData(BASE_ID + FILLER_ID + 5, -1, "Filler", ""),
	"Shield"				:	ItemData(BASE_ID + FILLER_ID + 6, -1, "Filler", ""),
	"Treasure"				:	ItemData(BASE_ID + FILLER_ID + 7, -1, "Filler", ""),
	"Burger"				:	ItemData(BASE_ID + FILLER_ID + 8, -1, "Filler", ""),
	"Extra Life"			:	ItemData(BASE_ID + FILLER_ID + 9, -1, "Filler", "")
}
# 65X1XXX
useful_table = {
	#Stamps
	"Steel Stamp"			:	ItemData(BASE_ID + USEFUL_ID + RED_ID, -1, "Useful", ""),
	#"Hint Stamp"           :   Use the Hint Point system for this
	"Harmony Stamp"			:	ItemData(BASE_ID + USEFUL_ID + GREEN_ID, -1, "Useful", ""),
	"Ghost Stamp"			:	ItemData(BASE_ID + USEFUL_ID + ORANGE_ID, -1, "Useful", ""),
	"Square Stamp"			:	ItemData(BASE_ID + USEFUL_ID + BLUE_ID, -1, "Useful", ""),
	"Gold Stamp"			:	ItemData(BASE_ID + USEFUL_ID + YELLOW_ID, -1, "Useful", ""),
	#Non-Stamps
	"House Upgrade"			:	ItemData(BASE_ID + USEFUL_ID + VIOLET_ID + 1, -1, "Useful", "")
}
# 65X2XXX
progression_table = {
	"Bottle"				:	ItemData(BASE_ID + PROGRESS_ID + RED_ID, 1, "Progression", ""),
	"Axe"					:	ItemData(BASE_ID + PROGRESS_ID + GREEN_ID, 1, "Progression", ""),
	"Castle Key"			:	ItemData(BASE_ID + PROGRESS_ID + VIOLET_ID, 1, "Progression", ""),
	"Pickaxe"				:	ItemData(BASE_ID + PROGRESS_ID + ORANGE_ID, 1, "Progression", ""),
	"Boat"					:	ItemData(BASE_ID + PROGRESS_ID + BLUE_ID, 1, "Progression", ""),
	"Shovel"				:	ItemData(BASE_ID + PROGRESS_ID + YELLOW_ID, 1, "Progression", ""),
}
# 65X3XXX
spheres_table = {
	"Red Sphere"			:	ItemData(BASE_ID + PROGUSEFUL_ID + RED_ID, 1, "Sphere", ""),
	"Green Sphere"			:	ItemData(BASE_ID + PROGUSEFUL_ID + GREEN_ID, 1, "Sphere", ""),
	"Violet Sphere"			:	ItemData(BASE_ID + PROGUSEFUL_ID + VIOLET_ID, 1, "Sphere", ""),
	"Orange Sphere"			:	ItemData(BASE_ID + PROGUSEFUL_ID + ORANGE_ID, 1, "Sphere", ""),
	"Blue Sphere"			:	ItemData(BASE_ID + PROGUSEFUL_ID + BLUE_ID, 1, "Sphere", ""),
	"Yellow Sphere"			:	ItemData(BASE_ID + PROGUSEFUL_ID + YELLOW_ID, 1, "Sphere", "")
}
# 65X4XXX
trap_table = {
	#Every trap card in your deck has a 50% chance of releasing
	"Unstable Trap"			:	ItemData(BASE_ID + TRAP_ID + RED_ID, -1, "Trap", ""),
	#You cannot see the enemies in your next battle
	"Fog Trap"				:	ItemData(BASE_ID + TRAP_ID + GREEN_ID, -1, "Trap", ""),
	#A random card you own will be released
	"Release Trap"			:	ItemData(BASE_ID + TRAP_ID + VIOLET_ID, -1, "Trap", ""),
	#Your highest quality card will be exchanged for one of a lower quality
	"Trade Down Trap"		:	ItemData(BASE_ID + TRAP_ID + ORANGE_ID, -1, "Trap", ""),
	#You cannot stack cards in your next battle
	"Stackless Trap"		:	ItemData(BASE_ID + TRAP_ID + BLUE_ID, -1, "Trap", ""),
	#You cannot see what cards are available in your next shop, event or treasure
	"Blind Trap"			:	ItemData(BASE_ID + TRAP_ID + YELLOW_ID, -1, "Trap", "")
}

all_items_table = {
	**spheres_table,
	**trap_table,
	**progression_table,
	**useful_table,
	**filler_table
}