import json
import uuid
import os
from rdflib import RDFS, RDF, OWL, Namespace, Graph, URIRef

# Define namespaces for Project Haystack
PH = Namespace("https://project-haystack.org/def/ph/3.9.7#")
PHICT = Namespace("https://project-haystack.org/def/phIct/3.9.7#")
PHSCIENCE = Namespace("https://project-haystack.org/def/phScience/3.9.7#")
PHIOT = Namespace("https://project-haystack.org/def/phIoT/3.9.7#")

# Location to Haystack RDFs
HAYSTACK_DEFS = os.path.join(os.getcwd(), "resources/defs.ttl")


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
def which_markers(entities):
    types = []
    if isinstance(entities, list):
        for e in entities:
            for k, v in e.items():
                types.append(k) if (v == "m:" and not k in types) else None
    elif isinstance(entities, dict):
        for k, v in entities.items():
            types.append(k) if (v == "m:" and not k in types) else None
    return types


# Initialize and return a Haystack graph with the correct namespaces
# and the parsed ttl file already loaded
def init_haystack_graph(path=HAYSTACK_DEFS):
    g = Graph()
    g.bind("ph", PH)
    g.bind("phict", PHICT)
    g.bind("phscience", PHSCIENCE)
    g.bind("phiot", PHIOT)
    g.parse(path, format="ttl")
    return g


# Run the given query on the graph (given the path to the graph),
# returning as a list
def query_return_list(path, q):
    g = init_haystack_graph(path)
    match = g.query(q)
    m2 = []
    for m in match:
        m2.append(str(m[0]).split("#")[1])
    return m2


# Query the ttl file to find all ph:marker objects
# and all subClassOf ph:marker objects
# Return as a list of strings, removing the URI's
def ph_load_all_markers(path=HAYSTACK_DEFS):
    q = """SELECT ?m WHERE {
        ?m rdfs:subClassOf* ph:marker
    }"""
    return query_return_list(path, q)


# Load defs which are direct subclasses of marker
def ph_load_fc_markers(path=HAYSTACK_DEFS):
    q = """SELECT ?m WHERE {
        ?m rdfs:subClassOf ph:marker
    }"""
    return query_return_list(path, q)


# Query the ttl file to find all ph:entity objects
# and all subClassOf ph:entity objects
# Return as a list of strings, removing the URI's
# This set should fully overlap with the
# load_valid_hastack_markers set, as all entities are
# subClassOf markers
def ph_load_all_entities(path=HAYSTACK_DEFS):
    q = """SELECT ?e WHERE {
        ?e rdfs:subClassOf* ph:entity
    }"""
    return query_return_list(path, q)


# Load defs which are direct subclasses of entity
def ph_load_fc_entities(path=HAYSTACK_DEFS):
    q = """SELECT ?e WHERE {
        ?e rdfs:subClassOf ph:entity
    }"""
    return query_return_list(path, q)


def ph_load_all_equips(path=HAYSTACK_DEFS):
    q = """SELECT ?e WHERE {
        ?e rdfs:subClassOf* phIoT:equip
    }"""
    return query_return_list(path, q)


def ph_load_fc_equips(path=HAYSTACK_DEFS):
    q = """SELECT ?e WHERE {
        ?e rdfs:subClassOf phIoT:equip
    }"""
    return query_return_list(path, q)


def ph_load_pointFunctionTypes(path=HAYSTACK_DEFS):
    q = """SELECT ?e WHERE {
        ?e rdfs:subClassOf phIoT:pointFunctionType
    }"""
    return query_return_list(path, q)


# Given a single entity, attempt to determine the 'type'.  The following logic
# is used:
# 1. limit entity tags to only valid haystack markers
# 2. Determine the entity type
#     - Raise error if multiple or none of first class entity markers defined
def ph_typer(entity, valid_entities=ph_load_fc_entities()):
    to_return = {}
    if not 'id' in entity.keys():
        to_return['status'] = {
            'valid': False,
            'description': 'Entity does not have an id'
        }
        return to_return
    to_return['id'] = entity['id']
    # refine all tags on entity to only marker tags
    entity_markers = which_markers(entity)
    entity_markers = set(entity_markers)

    # load valid markers and first class entities (direct subClassOf ph:entity)
    # from Haystack defs.ttl
    ph_valid_entities = valid_entities

    # determine the entity type.  Should be exactly one entity type,
    # raise Exception if else.
    entity_valid_entity = entity_markers.intersection(ph_valid_entities)
    if len(entity_valid_entity) == 0:
        to_return['valid'] = False
        to_return['description'] = "No first class entity type provided"
    elif len(entity_valid_entity) > 1:
        to_return['valid'] = False
        to_return['description'] = "Mutliple first class entity types provided: {}".format(entity_valid_entity)
    else:
        to_return['valid'] = True
        to_return['fc_entity_type'] = list(entity_valid_entity)[0]
    return to_return

# Iterate through list of entities, providing a typer for each
def ph_typer_many(entities, valid_entities=ph_load_fc_entities()):
    report = []
    for e in entities:
        report.append(ph_typer(e, valid_entities))
    return report

# Expect a report from ph_typer_many, print out report
def reporter(report, name):
    valid = 0
    no_fc_entity = 0
    mult_fc_entities = 0

    for r in report:
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
    with open(os.path.join(os.getcwd(), 'output/report_{}'.format(name)), 'w') as f:
        json.dump(report, f)

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
