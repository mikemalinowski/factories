"""
factories is a module which exposes a take on the Factory/Plugin design 
pattern. The idea behind this pattern is to be able to define a structure 
which your functionality sits within - allowing you to call that 
functionality without ever really knowing what it is doing.

This approach is particularly useful when building systems which are 
likely to expand in unknown ways over time. Example use cases might include:

    * Toolboxes, where each tool is represented as a plugin - and an 
        interface which is arbitrarily populated with those tools

    * Node graphs, where we have no up-front knowledge of what nodes 
        may be available to use

    * Data parsers which include data that changes format over time due 
        to deprecation, meaning each data type can be represented by a 
        plugin allowing the framework to never care about the storage 
        details of the data

The commonality between all these structures is that the core of each 
system needs to do something but it does not have to care about the 
detail of how that task is achieved. Instead the detail is held within 
plugins libraries which can be expanded and contracted over time.

This pattern is incredibly useful but tends to come with an overhead 
of writing dynamic loading mechanisms and functionality to easily 
interact and query the plugins. The Factories module aims to diminish
that overhead - allowing you to focus on your end goal and the 
development of plugins.

This library was written based from the information here:
https://sourcemaking.com/design_patterns/factory_method

It is also designed based on the principals given during the
GDC 2018 Talk - A Practical Approach to Developing Forward-Facing Rigs, Tools and
Pipelines. Which can be explored in more detail here:
https://www.gdcvault.com/play/1025427/A-Practical-Approach-to-Developing
"""
from .factory import (
    Factory,
)

from .constants import (
    log,
)
