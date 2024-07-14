# snek bits 🐍
Random bag of Python utilities.

## Config
Config is a recursive, dot-notation-accessed python dictionary ("dotdict") with various features. Its main use is to contain configuration settings that need to be passed to various sub-components of a project/application.

### Features
1. Load configurations from YAML files (see .from_yaml method).
2. Import & create class instances (see .create_instance method).
3. Convert to normal Python dictionary (see .dict method).
4. Perform check for available keys (see .has method).

## Plugin
Plugin provides a way to make Python classes flexible by allowing their methods' inputs, outputs, or definitions be modified. Users can wrap class methods with the Plugin.pluginable decorator, and the write plugins that modify this method with prefixes ("pre_", "post_", or "override_"). Below is a simple example:

```python
# Imports
from .plugin import Plugin

# Example
class MyCoolClass:

    def __init__(self, plugins: list[Plugin]) -> None:
        self.plugins = plugins

    @Plugin.pluginable
    def my_cool_method(self, x: int, y: int) -> int:
        return x + y

class MyCoolMethodPlugin(Plugin):

    def __init__(self):
        super().__init__()

    def pre_my_cool_method(self, my_instance: MyCoolClass,
                           x: int, y: int) -> tuple:
        x -= 1; y -= 2
        return (x, y)

def main() -> None:
    plugins = [MyCoolMethodPlugin()]
    my_cool_class_instance = MyCoolClass(plugins=plugins)
    x, y = 3, 5
    my_cool_class_instance.my_cool_method(x=x, y=y)
    # returns -> 5
    # Explanation:
    #   1. plugin use pre_ to modify my_cool_method input
    #      x: 3 - 1 -> 2
    #      y: 5 - 2 -> 3
    #
    #   2. Updated inputs get passed to my_cool_method
    #
    #   3. my_cool_method sums x & y
    #       2 + 3 -> 5
```


