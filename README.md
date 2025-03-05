## Installation
You can either clone or download this github repo, or alternatively you can 
install this via pip:

```commandline
pip install factories
```


## Overview
factories is a module which exposes a take on the Factory/Plugin design pattern. The idea behind this pattern is to be able to define a structure which your functionality sits within - allowing you to call that functionality without ever really knowing what it is doing.

This approach is particularly useful when building systems which are likely to expand in unknown ways over time. Example use cases might include:

+ Toolboxes, where each tool is represented as a plugin - and an interface which is arbitrarily populated with those tools

+ Node graphs, where we have no up-front knowledge of what nodes may be available to use

+ Data parsers which include data that changes format over time due to deprecation, meaning each data type can be represented by a plugin allowing the framework to never care about the storage details of the data

The commonality between all these structures is that the core of each system needs to do something but it does not have to care about the detail of how that task is achieved. Instead the detail is held within plugins libraries which can be expanded and contracted over time.

This pattern is incredibly useful but tends to come with an overhead of writing dynamic loading mechanisms and functionality to easily interact and query the plugins. The Factories module aims to diminish that overhead - allowing you to focus on your end goal and the development of plugins.

## Quick Example
To utilise a factory we first need to declare what the factory will contain. This is class where you define exactly what functionality should be adhered to - consider this to be the base class of all your plugins.

```python
class Tool(object):
    name = 'unknonw'
    
    def activate(self):
        return None
       
    def about(self):
        return ''
```


In this example we're defining a tool as a class which has a name attribute and two methods. Now we can instance a factory giving our base class.

```python
import factories

factory = factories.Factory(
    abstract=Tool,
    plugin_identifier='name',
)
```


Note here that we're giving the Factory the Tool class type - it uses this when searching to know what to look for. We also give it an (optional) identifier, this can be used to request specific plugins from the factory.

We can now start adding paths to our factory. The factory will immediately search these locations looking for plugins (any classes which inherit form the Tool clas).

```python
# -- Register with a hard coded path
factory.add_path(
    'c:/some/plugin/location'
)

# -- Register relatively
factory.add_path(
    os.path.join(
        os.path.dirname(__file__),
        'our_plugins',
    ),
)
```


We can now begin to interact with our factory

```python

# -- Perhaps we're dealing with something  obscure, like a 
# -- UI where we do not know exactly what is needed up front.
# -- So we add a button for each tool
for tool_name in factory.identifiers():
    ui.addButton(tool_name)
   
# -- In a scenario where we connect the click event to a function
# -- which passes the tool name
def button_click(button):
    tool = factory.request(button.text())
    tool().activate()
```


In this example our tool box has no pre-conception of what tools it contains, instead it is populated dynamically using the factory and we only instance the tool at the time the user is actually requesting it to be activated.


## Further Examples
Factories comes with two additional examples. One which shows how plugins can be used to parse data - and giving authority to the plugins to determine which should parse what rather than the core functionality. The other example is a demonstration of using plugins to represent 'animals in a zoo'. 

These examples live under ```factories.examples.reader``` and ```factories.examples.zoo``` respectively.


## Testing and Stability

This module comes with a suite of unit tests which give a 96% coverage. It is therefere highly recommended that you run these tests prior to making any alterations, and again before putting forward fixes or contributions.

Whilst every effort goes into stability, given that this is a relatively new module it is always appreciated if you can communicate any bugs or issues to [mike.malinowski@outlook.com](mike.malinowski@outlook.com)


## Compatability

This has been tested under Python 2.7.13 and Python 3.6.6 under both Windows and Ubuntu.
