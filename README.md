# building_graphs
Building of Haystack / Brick Graphs

# Introduction
The purpose of this repo is to provide examples and utility functions for working with Brick / Haystack data.  Haystack is used predominantly in industry, but the Haystack 4.0 standard is currently being developed to provide additional structure to the Haystack standard.  Previous concerns about the implementation of the Haystack standard across organizations (many of whom define custom tags), as well as recent [HouseOfSticks](https://brickschema.org/papers/HouseOfSticks-BuildSys-2019-Fierro.pdf) paper raises many good questions about Haystack:
1. How to understand what is in a Haystack model?
1. Which tags applied are specified in the standard vs. custom?
1. Are defined tags used correctly in combination with other tags to correctly implement typing?
1. How do I know the full set of tags required for a specific type of equipment, point, etc.?

This repository intends to provide methods / open source examples for how to accomplish this.

# Setup
1. Clone this repo
1. Create a new virtual environment and install dependencies defined in `requirements.txt`
1. Clone the [brick-examples](https://github.com/BrickSchema/brick-examples) repo to the same directory level as building_graphs:
    ```
    root_dir/
        |-building_graphs
        |-brick-examples
    ```

## examples
Example files showing how to implement and utilize utility functions to achieve a specific purpose.  Comments in the files walk the user through the WHAT and WHY.

## resources
RDF definitions serialized as TTL files for both Brick and Haystack.  Stored locally for convenience.

## scripts
Scripts designed to perform specific functions.
