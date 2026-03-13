from typing import Any, Dict
import logging

from BaseClasses import Item, Location, Region, Tutorial, ItemClassification
from worlds.generic.Rules import set_rule
from .ItemPool import spheres_table, all_items_table, progression_table, filler_table, useful_table, trap_table
from .Options import CardelagoOptions

from ..AutoWorld import World, WebWorld
from NetUtils import SlotType

class CardelagoItem(Item):
    game: str = "Cardelago"

class CardelagoLocation(Location):
    Cardelago : str = "Cardelago"

class CardelagoWeb(WebWorld):
    englishTut = Tutorial("",
                     """A guide for setting up Cardelago on your computer.""",
                     "English",
                     "setup_en.md",
                     "setup/en",
                     ["Smg065"])
    tutorials = [englishTut]

class CardelagoWorld(World):
    """
    Cardelago is a game that uses items at it's locations as in-game items.
    """
    game : str = "Cardelago"
    version : str = "V0.5"
    web = CardelagoWeb()
    topology_present = True
    options_dataclass = CardelagoOptions
    options : CardelagoOptions
    card_colors : list[str] = ["Red", "Green", "Violet", "Orange", "Blue", "Yellow"]
    #Items
    item_name_to_id = {}
    for each_key, each_item in all_items_table.items():
        item_name_to_id[each_key] = each_item.acid
    #Locations (Cards)
    location_name_to_id = {}
    for color_index, each_color in enumerate(card_colors):
        for each_card in range(0, 100):
            id : int = (color_index * 100) + each_card
            location_name_to_id[each_color + " Card " + str(each_card + 1)] = id + 65000

    def generate_early(self):
        player = self.player
        multiworld = self.multiworld

        #Basic setup
        menu_region : Region = Region("Menu", player, multiworld)
        multiworld.regions.append(menu_region)
        self.spawning_sphere = self.random.choice(list(spheres_table.keys()))
        spawning_sphere = self.create_item(self.spawning_sphere)
        multiworld.push_precollected(spawning_sphere)
        self.final_boss_origin = self.random.choice(list(multiworld.player_name.values()))
        #Victory Condition
        all_bosses : CardelagoLocation = CardelagoLocation(player, "All Bosses", None, menu_region)
        all_bosses.place_locked_item(self.create_event("Victory"))
        menu_region.locations.append(all_bosses)
        multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
        set_rule(all_bosses, lambda state: state.has_all(list(spheres_table.keys()), player))

        #Create the 6 regions
        color_to_region : Dict[str, Region] = {}
        for color_name in self.card_colors:
            each_region : Region = Region(color_name + " Region", player, multiworld)
            color_to_region[color_name] = each_region
            multiworld.regions.append(each_region)
            #Spawning sphere is
            if self.spawning_sphere.startswith(color_name):
                menu_region.connect(each_region, color_name + "Spawn")
        
        #Get the sphere order
        self.generate_world_map_order(menu_region)

        #Get the breakers priority
        self.get_obstacles_priorities()

        #Gate regions based on that order
        for region_color, region_connections in self.world_order.items():
            #The key of the graph node is the origin you're starting at
            from_region = color_to_region[region_color]
            for each_connection in region_connections:
                #Create the requirements
                generated_requirements = [each_connection + " Sphere"]
                #Each value at the key is the destination it leads to
                to_region = color_to_region[each_connection]
                #The region this is in potentially prevents you from getting there via obstacles
                if each_connection in self.breaker_priority[region_color]:
                    generated_requirements.append(self.color_to_breaker(each_connection))
                #Go from one to the other, requiring the sphere as the key
                from_region.connect(to_region, "Unlock " + each_connection + " Gate", lambda state, requires = generated_requirements: state.has_all(requires, self.player))
        
        #Create all the cards
        for region_index, region_color in enumerate(color_to_region):
            origin_region : Region = color_to_region[region_color]
            #For the total number there are per region
            for card_number in range(self.options.cards_per_region):
                card_id = (region_index * 100) + card_number
                each_card : CardelagoLocation = CardelagoLocation(player, region_color + " Card " + str(card_number + 1), card_id + 65000, origin_region)
                origin_region.locations.append(each_card)
            
        return super().generate_early()

    def generate_world_map_order(self, menu_region : Region):
        #Sphere order starts with your spawning sphere
        self.world_order : dict[str, list[str]] = {}
        
        #Make sure all the logic keys exist
        for each_color in self.card_colors:
            self.world_order[each_color] = []

        #From the spheres not yet in sphere order
        colors_remaining : list[str] = self.card_colors.copy()
        #Account for the color you spawn in
        spawn_color = self.spawning_sphere.split(" ")[0]
        colors_remaining.remove(spawn_color)

        #Branching
        branching_node = spawn_color
        adjacency_orgins = [spawn_color, spawn_color]

        #How many logical branches can exist from here?
        while len(colors_remaining) > 0:
            #You need to select a node
            color_selected : str
            
            #Find adjacencies
            adjacencies : list[str] = []
            for each_orgin in adjacency_orgins:
                index = self.card_colors.index(each_orgin)
                adjacencies.extend(
                    [self.card_colors[(index + 5) % len(self.card_colors)],
                    self.card_colors[(index + 1) % len(self.card_colors)]]
                )

            #Trim to only valid adjacencies
            valid_adjacencies : list[str] = []
            valid_warpables : list[str] = []
            for each_color in colors_remaining:
                if each_color in adjacencies:
                    valid_adjacencies.append(each_color)
                else:
                    valid_warpables.append(each_color)

            #Only worry about adjacenies if there are ones, and if there's non-adjacent options
            if len(valid_adjacencies) > 0 and len(valid_warpables) > 0:
                #Pick
                if self.random.randint(1, self.options.adjacency_odds) != 1:
                    #Adjacent weighted
                    color_selected = self.random.choice(valid_adjacencies)
                else:
                    #Warps are less common
                    color_selected = self.random.choice(valid_warpables)
            else:
                #Pick a color at random from the remaining if valid's aren't a concern
                color_selected = self.random.choice(colors_remaining)
                

            #Assign into dictionary, creating a new list when needed
            self.world_order[branching_node].append(color_selected)
            #This is no longer a sphere in the selectable pool
            colors_remaining.remove(color_selected)
            
            #Use the last line as refrence for what we're doing
            adjacency_orgins[0] = branching_node
            adjacency_orgins[1] = color_selected
            #Reuse the last branching node a fifth of the time
            if self.random.randint(1, self.options.branching_odds) != 1:
                branching_node = color_selected
        
        #Inform the spoiler log of the logic construction here
        for base_color, color_connections in self.world_order.items():
            for each_index, each_connection in enumerate(color_connections):
                menu_region.add_event(base_color + " Sphere Requirement " + str(1 + each_index), each_connection + " Gate")

    def color_to_breaker(self, in_color : str):
        #Color to breaker types
        return list(progression_table.keys())[self.card_colors.index(in_color)]

    def get_obstacles_priorities(self):
        self.breaker_priority : dict[str, list[str]] = {}
        for each_region, region_gates in self.world_order.items():
            blocking_gates : list[str] = []
            for each_gate in region_gates:
                if self.random.randint(0, 1) == 1:
                    blocking_gates.append(each_gate)
            self.breaker_priority[each_region] = blocking_gates

    def create_item(self, name: str) -> Item:
        item_data = all_items_table[name]
        item_classification = None
        item_id = item_data.acid
        match item_data.type:
            #Spheres are Proguseful
            case "Sphere":
                item_classification = ItemClassification.progression | ItemClassification.useful
            case "Filler":
                item_classification = ItemClassification.filler
            case "Progression":
                item_classification = ItemClassification.progression
            case "Trap":
                item_classification = ItemClassification.trap
            case "Useful":
                item_classification = ItemClassification.useful
        item_output = CardelagoItem(name, item_classification, item_id, self.player)
        return item_output

    def create_event(self, name: str):
        return CardelagoItem(name, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:
        core_items : list = []
        core_items.extend(list(spheres_table.keys()))
        core_items.extend(list(progression_table.keys()))
        core_items.remove(self.spawning_sphere)
        core_item_count : int = 0
        
        #Core Items
        for each_item in core_items:
            for _ in range(all_items_table[each_item].qty):
                self.multiworld.itempool.append(self.create_item(each_item))
                core_item_count += 1
        
        #The filler, useful and trap items that scale
        noncore_count = (self.options.cards_per_region * 6) - core_item_count
        #Noncore Spawning Garunteed
        noncore_items : list[CardelagoItem] = []
        for item_name, item_percent in self.options.item_percentages.value.items():
            to_spawn = (item_percent * noncore_count) // 100
            for _ in range(to_spawn):
                noncore_items.append(self.create_item(item_name))
        #Noncore Spawning Variation
        while len(noncore_items) < noncore_count:
            chosen_weight = self.random.randint(0, 100)
            random_item : str
            for item_name, item_percent in self.options.item_percentages.value.items():
                chosen_weight -= item_percent
                random_item = item_name
                if chosen_weight < 0:
                    break
            noncore_items.append(self.create_item(random_item))
        self.multiworld.itempool.extend(noncore_items)

    def locations_of_slots_items(self) -> list[list[int]]:
        myItems : list[Item] = self.get_items_from(self.player)
        output : list[list[int | str]] = []
        for each_item in myItems:
            output.append([each_item.location.player, each_item.location.name, each_item.flags, each_item.code, each_item.location.address])
        return output

    def get_items_from(self, target_player) -> list[Item]:
        return list(filter(lambda a: a.player == target_player, self.multiworld.itempool))

    def fill_slot_data(self) -> Dict[str, Any]:
        options = {}
        options["difficulty"] = self.options.difficulty.value
        options["cards_per_region"] = self.options.cards_per_region.value
        options["map_radius"] = self.options.map_radius.value
        options["node_percentages"] = self.options.node_percentages.value
        options["tiles_per_pip"] = self.options.tiles_per_pip.value
        enemies = self.locations_of_slots_items()
        options["enemies"] = enemies
        options["final_boss_origin"] = self.final_boss_origin
        options["trap_release_chance"] = self.options.trap_release_chance.value
        options["breaker_priority"] = self.breaker_priority
        options["spawning_sphere"] = self.spawning_sphere
        options["world_order"] = self.world_order
        options["player_name"] = self.multiworld.player_name[self.player]
        options["seed"] = self.random.randint(-6500000, 6500000)
        options["version"] = self.version
        return options