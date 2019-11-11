import json
import uuid
import os
from rdflib import RDFS, RDF, OWL, Namespace, Graph, URIRef
from .queries import *
from itertools import permutations

# Bulk load queries as lists to limit disc calls
ALL_ENTITIES = ph_load_all_entities()
ALL_ENTITIES.remove('entity')
ALL_EQUIPS = ph_load_all_equips()
ALL_EQUIPS.remove('equip')
EACH_EQUIP_AS_SET = []
for e in ALL_EQUIPS:
    EACH_EQUIP_AS_SET.append(set(e.split('-')))

ALL_VALS = ph_load_all_vals()
ALL_VALS.remove('val')
ALL_MARKERS = ph_load_all_markers()
ALL_MARKERS.remove('marker')
ALL_PHENOMENON = ph_load_all_phenomenon()
ALL_PHENOMENON.remove('phenomenon')
ALL_QUANTITIES = ph_load_all_quantities()
ALL_QUANTITIES.remove('quantity')

FC_ENTITIES = ph_load_fc_entities()
FC_EQUIPS = ph_load_fc_equips()
FC_MARKERS = ph_load_fc_markers()
FC_PHENOMENON = ph_load_fc_phenomenon()
FC_QUANTITIES = ph_load_fc_quantities()

POINT_FUNCTION_TYPES = ph_load_pointFunctionTypes()


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


# Mimic the `find_tagset` funciton, however,
# excluding entities containing ALL of the tags in the exclude_tags list
def find_tagset_exclusive(entities, tags, exclude_tags):
    exclude_tags = set(exclude_tags)
    matches, non_matches = find_tagset(entities, tags)
    matches_exclude = [e for e in matches if not exclude_tags.issubset(e.keys())]
    return matches_exclude


# Find a given string in the navName parameter and return it as a match
def find_str_in_navName(entities, find):
    matches = [e for e in entities if ('navName' in e.keys() and find.lower() in e['navName'].lower())]
    non_matches = [e for e in entities if ('navName' in e.keys() and not find.lower() in e['navName'].lower())]
    return (matches, non_matches)


# Iterate through all entites, adding the tag_to_add
# as a marker to all entities
def add_marker(entities, tag_to_add):
    for e in entities:
        e[tag_to_add] = "m:"
    return entities


# Iterate through all entities, adding the tag_to_add
# as a marker to all entities that are a subset of the
# tags_to_find
def add_marker_given_tagset(entities, tag_to_add, tags_to_find):
    tags_to_find = set(tags_to_find)
    for e in entities:
        e[tag_to_add] = "m:" if tags_to_find.issubset(e) else e
    return entities


# Per Project Haystack specification, marker tags should be serialized
# to a JSON type using "m:" as the value.  It was noticed that many of
# the marker tags in the examples were serialized as "M".  This function
# will replace the m_bad with "m:"
def cleanup_marker_tags(entities, m_bad="M"):
    for e in entities:
        for k, v in e.items():
            if v == m_bad:
                e[k] = "m:"
            else:
                e[k] = v
    return entities


# Remove the tag from all entities passed in.
# If the tag is not present, the entity is not affected
def remove_tag(entities, tag):
    output = []
    for e in entities:
        e.pop(tag)
        output.append(e)
    return output


# Identify all of the 'typing' (i.e. marker tags) used.
# Regardless of if a dict or a list of dicts is passed,
# all unique marker types are passed back in a single list
def only_markers(entities):
    types = []
    if isinstance(entities, list):
        for e in entities:
            for k, v in e.items():
                types.append(k) if (v == "m:" and not k in types) else None
    elif isinstance(entities, dict):
        for k, v in entities.items():
            types.append(k) if (v == "m:" and not k in types) else None
    return types


# Identify all of the 'non-typing' (i.e. val tags) used.
# Regardless of if a dict or a list of dicts is passed,
# all unique val types are passed back in a single list
def only_vals(entities):
    types = []
    if isinstance(entities, list):
        for e in entities:
            for k, v in e.items():
                types.append(k) if (v != "m:" and k not in types) else None
    elif isinstance(entities, dict):
        for k, v in entities.items():
            types.append(k) if (v != "m:" and k not in types) else None
    return types


# Given a single entity, attempt to determine the 'type'.  The following logic
# is used:
# 1. limit entity tags to only valid haystack markers
# 2. Determine the entity type
#     - Raise error if multiple or none of first class entity markers defined
def ph_typer(entity, valid_entities=FC_ENTITIES, all_entities=ALL_ENTITIES):
    to_return = {}
    if not 'id' in entity.keys():
        to_return['status'] = {
            'valid': False,
            'description': 'Entity does not have an id'
        }
        return to_return
    to_return['id'] = entity['id']

    # refine all tags on entity to only marker tags
    entity_markers = only_markers(entity)
    entity_markers = set(entity_markers)
    entity_valid_markers = entity_markers.intersection(ALL_MARKERS)
    entity_invalid_markers = entity_markers.difference(ALL_MARKERS)

    entity_vals = only_vals(entity)
    entity_vals = set(entity_vals)
    if len(entity_vals) > 1:
        entity_valid_vals = entity_vals.intersection(ALL_VALS)
        entity_invalid_vals = entity_vals.difference(ALL_VALS)
    else:
        entity_valid_vals = []
        entity_invalid_vals = []

    # determine the entity type.  Should be exactly one entity type,
    # raise Exception if else.
    entity_valid_entity = entity_markers.intersection(FC_ENTITIES)

    if len(entity_valid_entity) == 0:
        to_return['valid'] = False
        to_return['description'] = "No first class entity type provided"
    elif len(entity_valid_entity) > 1:
        to_return['valid'] = False
        to_return['description'] = "Mutliple first class entity types provided: {}".format(entity_valid_entity)
    else:
        to_return['valid'] = True
        to_return['fc_entity_type'] = list(entity_valid_entity)[0]

    if to_return['valid']:
        non_entity_markers = entity_valid_markers.difference(ALL_ENTITIES)
        # Given only valid fc entities
        to_return = ph_subtyper(to_return, entity_markers, non_entity_markers)
    to_return['valid_markers'] = list(entity_valid_markers)
    to_return['invalid_markers'] = list(entity_invalid_markers)
    to_return['valid_vals'] = list(entity_valid_vals)
    to_return['invalid_vals'] = list(entity_invalid_vals)
    return to_return


# Given an entity with a valid first class entity type, attempt to determine the subtype
# TODO: Deal with other first class entity types
def ph_subtyper(a_dict, entity_markers, non_entity_markers):
    entity_type = a_dict['fc_entity_type']
    # if entity_type == 'device':

    if entity_type == 'equip':
        all_valid_markers = list(entity_markers) + list(non_entity_markers)
        subclasses_in_entity = []
        for e in EACH_EQUIP_AS_SET:
            if e.issubset(all_valid_markers):
                if len(e) > 1:
                    e_list = list(e)
                    e_perms = permutations(e_list, len(e_list))
                    for c in e_perms:
                        c2 = '-'.join(c)
                        subclasses_in_entity.append(c2) if c2 in ALL_EQUIPS else None

                else:
                    subclasses_in_entity.append(list(e)[0])
        non_entity_markers = list(non_entity_markers)
        a_dict['subclasses_in_entity'] = subclasses_in_entity
        a_dict['non_entity_markers'] = non_entity_markers
    elif entity_type == 'point':
        point_type = set(non_entity_markers).intersection(POINT_FUNCTION_TYPES)
        point_phenom = set(non_entity_markers).intersection(ALL_PHENOMENON)
        point_quantity = set(non_entity_markers).intersection(ALL_QUANTITIES)
        a_dict['point_function'] = list(point_type)
        a_dict['phenomenon'] = list(point_phenom)
        a_dict['quantity'] = list(point_quantity)
    # elif entity_type == 'protocol':
    elif entity_type == 'site':
        a = 1
    # elif entity_type == 'space':
    # elif entity_type == 'weatherStation':
    return a_dict


# Given the entities in the building, extend the report['general']
# to include a list of all markers / vals broken out by whether or
# not they are valid / invalid
def all_valid_invalid_markers_and_vals(entities, report):
    # First
    markers_used = only_markers(entities)
    vals_used = only_vals(entities)

    valid_markers = set(markers_used).intersection(ALL_MARKERS)
    invalid_markers = set(markers_used).difference(ALL_MARKERS)
    valid_vals = set(vals_used).intersection(ALL_VALS)
    invalid_vals = set(vals_used).difference(ALL_VALS)

    report['general']['valid_markers'] = list(valid_markers)
    report['general']['invalid_markers'] = list(invalid_markers)
    report['general']['valid_vals'] = list(valid_vals)
    report['general']['invalid_vals'] = list(invalid_vals)
    return report


# Given the entities in the building, extend the report['general']
# to include a counting of tags (vals or markers), broken out by
# valid / invalid, and counted by the first class entity type which implemented
# the tag
def count_tags_by_entity(entities, report):
    # These are the entity keys we will be iterating through
    to_iter = ['valid_markers', 'invalid_markers', 'valid_vals', 'invalid_vals']

    report['general']['count_tags_by_entity'] = {}

    # Break the report down by Haystack first class entities
    for ent in FC_ENTITIES:
        if not ent in report['general']['count_tags_by_entity'].keys():
            report['general']['count_tags_by_entity'][ent] = {}
        for i in to_iter:
            report['general']['count_tags_by_entity'][ent][i] = {}

    # Generic catch all for all non-first class entities
    report['general']['count_tags_by_entity']['other'] = {}

    for i in to_iter:
        report['general']['count_tags_by_entity']['other'][i] = {}

    # Iterate through each entity already analyzed by the report
    for entity in report['entities']:
        # Set the entity_type to be one of the FC_ENTITIES or 'other':
        #     'point', 'equip', 'weatherStation', 'site', 'device', 'space', 'protocol', 'other'
        if entity['valid']:
            entity_type = entity['fc_entity_type']
        else:
            entity_type = 'other'
        # Iterate through each of the:
        #     ['valid_markers', 'invalid_markers', 'valid_vals', 'invalid_vals']
        for marker_or_vals in to_iter:
            for tag in entity[marker_or_vals]:
                if tag not in report['general']['count_tags_by_entity'][entity_type][marker_or_vals].keys():
                    report['general']['count_tags_by_entity'][entity_type][marker_or_vals][tag] = 1
                else:
                    report['general']['count_tags_by_entity'][entity_type][marker_or_vals][tag] += 1
    return report


def ph_reporter_general(entities, report):
    # First step is to get general information on valid / invalid
    # marker and val tags used in the model
    report = all_valid_invalid_markers_and_vals(entities, report)

    # Second step is to get specific information on which tags
    # are used on each first class entity type, and how many times they are used
    report = count_tags_by_entity(entities, report)
    return report


# Iterate through list of entities, providing a typer for each
def ph_typer_many(entities, valid_entities=FC_ENTITIES, all_entities=ALL_ENTITIES):
    report = {
        'entities': [],
        'general': {}
    }
    for e in entities:
        report['entities'].append(ph_typer(e, valid_entities, all_entities))

    report = ph_reporter_general(entities, report)
    return report


# Expect a report from ph_typer_many, print out report
def reporter(report, name):
    valid = 0
    no_fc_entity = 0
    mult_fc_entities = 0

    # Count the number of valid entities
    for r in report['entities']:
        if r['valid']:
            valid += 1
        else:
            if r['description'] == 'No first class entity type provided':
                no_fc_entity += 1
            else:
                mult_fc_entities += 1

    print("Report for {}".format(name))
    print("Number of valid entities: {}".format(valid))
    print("Number of entities w/no first class entity defined: {}".format(no_fc_entity))
    print("Number of entities w/multiple first class entities defined: {}".format(mult_fc_entities))
    print(json.dumps(report['general'], sort_keys=True, indent=2))
    output_dir = os.path.join(os.getcwd(), 'output')
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, 'report_{}'.format(name))
    with open(output_file, 'w') as f:
        json.dump(report, f, sort_keys=True, indent=2)


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
