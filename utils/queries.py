import os
from rdflib import Namespace, Graph, RDFS, RDF, OWL

# Define namespaces for Project Haystack
PH = Namespace("https://project-haystack.org/def/ph/3.9.7#")
PHICT = Namespace("https://project-haystack.org/def/phIct/3.9.7#")
PHSCIENCE = Namespace("https://project-haystack.org/def/phScience/3.9.7#")
PHIOT = Namespace("https://project-haystack.org/def/phIoT/3.9.7#")

# Location to Haystack RDFs
HAYSTACK_DEFS = os.path.join(os.getcwd(), "resources/defs.ttl")


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


def ph_subclass_of(cl, path=HAYSTACK_DEFS):
    q = """SELECT ?e WHERE {
        ?e rdfs:subClassOf phIoT:%s
    }""" % cl
    return query_return_list(path, q)

def ph_load_all_phenomenon(path=HAYSTACK_DEFS):
    q = """SELECT ?phenom WHERE {
        ?phenom rdfs:subClassOf* phScience:phenomenon
    }"""
    return query_return_list(path, q)

def ph_load_fc_phenomenon(path=HAYSTACK_DEFS):
    q = """SELECT ?phenom WHERE {
        ?phenom rdfs:subClassOf phScience:phenomenon
    }"""
    return query_return_list(path, q)

def ph_load_all_quantities(path=HAYSTACK_DEFS):
    q = """SELECT ?q WHERE {
        ?q rdfs:subClassOf* phScience:quantity
    }"""
    return query_return_list(path, q)

def ph_load_fc_quantities(path=HAYSTACK_DEFS):
    q = """SELECT ?q WHERE {
        ?q rdfs:subClassOf phScience:quantity
    }"""
    return query_return_list(path, q)

def ph_load_all_vals(path=HAYSTACK_DEFS):
    q = """SELECT ?q WHERE {
        ?q ph:is* ph:val
    }"""
    return query_return_list(path, q)
