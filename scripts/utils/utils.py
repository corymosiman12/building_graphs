import json
import uuid

# Import one of the Haystack JSON files as a list
# of dictionaries. Files to be serialized using the JSON
# Haystack API specification.  Only 'rows' are returned.
def import_haystack_json(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data['rows']


# Find all of the equipment given a Haystack 'rows' dict
def find_equips(entities):
    equips, non_equips = find_tagset(entities, tags=['equip'])
    return (equips, non_equips)


# Find all sensor points
# TODO: add 'point' to tags list for find_sensors, find_cmds, find_sps
# TODO: add exclsivity check, i.e. sensor cannot also be cmd, etc.
def find_sensors(entities):
    sensors, non_sensors = find_tagset(entities, tags=['sensor'])
    return (sensors, non_sensors)

# Find all cmd points
def find_cmds(entities):
    cmds, non_cmds = find_tagset(entities, tags=['cmd'])
    return (cmds, non_cmds)


# Find all setpoint points
def find_sps(entities):
    sps, non_sps = find_tagset(entities, tags=['sp'])
    return (sps, non_sps)


# Given a list of separate tags (strings), find the entities with the
# full set of tags.  Return a two-termed tuple, where the first term
# are all matches, and the second term is all non-matches
def find_tagset(entities, tags):
    tags = set(tags)
    matches = [e for e in entities if tags.issubset(e.keys())]
    non_matches = [e for e in entities if not tags.issubset(e.keys())]
    return (matches, non_matches)


# Find a given string in the navName parameter and return it as a match
def find_str_in_navName(entities, find):
    matches = [e for e in entities if ('navName' in e.keys() and find.lower() in e['navName'].lower())]
    non_matches = [e for e in entities if ('navName' in e.keys() and not find.lower() in e['navName'].lower())]
    return (matches, non_matches)

# Iterate through all entites, adding the marker indicator to
# the marker_str key defined
def add_marker(entities, marker_str):
    for e in entities:
        e[marker_str] = "M"
    return entities

def remove_tag(entities, tag):
    output = []
    for e in entities:
        e.pop(tag)
        output.append(e)
    return output

# TODO: Add how BRICK points 'found' given equip.
# Given an equip dict, and a dict of entities, find the points
# belonging to the respective equipment
def find_equip_points(equip, entities, ontology_lang='haystack'):
    if ontology_lang == 'haystack':
        equip_id = equip['id']
        points = [p for p in entities if p['equipRef'] == equip_id]
        return points
    elif ontology_lang == 'brick':
        # do stuff
        a = 1
    else:
        return False

# TODO: Entity class definition...how to?
class Entity(object):
    def __init__(self, entity_dict):
        self.as_dict = entity_dict
        self.id = entity_dict['id'] if 'id' in entity_dict else str(uuid.uuid4())
        self.dis = entity_dict['dis'] if 'dis' in entity_dict else 'No dis available'
        # self.root_entity = self.generate_root_entity()

    def __str__(self):
        return self.dis

    # def generate_root_entity(self):
    # Method to find 'largest' entity type definition, i.e. one of:
    #     - device
    #     - equip
    #     - network
    #     - point
    #     - protocol
    #     - site
    #     - space
    #     - weatherStation
