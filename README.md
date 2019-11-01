# building-graphs
Building of Haystack / Brick Graphs

# Introduction
The purpose of this repo is to create both Brick / Haystack graphs.  The intended workflow is as follows:

1. Use the JSON files in the haystack/ directory copied from [brick-examples](https://github.com/BrickSchema/brick-examples) to create BRICK / Haystack 4.0 graphs
    - resources/def.ttl includes the Haystack 3.9.7 ttl file
    - resources/Brick.ttl includes the Brick 1.0.3 ttl file
    - resources/BrickFrame.ttl includes the Brick Frame 1.0.3 ttl file
2. Serialize as a ttl file
3. Utilize a graph database technology (Neo4j) to import the model.
