# Imports
from abc import ABC
from typing import Any
import functools

# Plugin
class Plugin(ABC):
    """
    Abstract base class which all plugins derive from.
    """
    def __init__(self):
        super().__init__()

    def pre_(self, *args, **kwargs) -> tuple|None:
        """
        pre_<function-name>:
            modify input to a function or perform a
            task before function is called.
        returns:
            Either a tuple with updated args or None.
        """
        raise NotImplementedError

    def post_(self, output: Any) -> Any|None:
        """
        post_<function-name>:
            modify output of a function or perform a
            task after function is called.
        """
        raise NotImplementedError

    def override_(self, *args, **kwargs) -> Any:
        """
        override_<function-name>:
            overwrite a function's definition.
        """
        raise NotImplementedError

    @staticmethod
    def pluginable(func):
        """
        Method decorator to allow a
            class method to support plugins.
        """
        @functools.wraps(func)
        def hooked(self, *args, **kwargs):
            func_name = func.__name__
            while func_name[0] == '_':
                func_name = func_name[1:]
            if self.plugins:
                # Override-function plugins
                overridden, override_func = None, None
                for plugin in self.plugins:
                    if (hasattr(plugin, f'override_{func_name}')
                        and not overridden):
                        override_func = getattr(
                            plugin, f'override_{func_name}')
                        overridden = plugin.__class__.__name__
                    elif (hasattr(plugin, f'override_{func_name}') and overridden):
                        raise RuntimeError('Only 1 plugin can override a function. '
                                            f'Plugin {plugin.__class__.__name__} is '
                                            f'trying to override function {func_name}, '
                                            f'but plugin {overridden} already did!')
                # Pre-function plugins
                for plugin in self.plugins:
                    if hasattr(plugin, f'pre_{func_name}'):
                        hook = getattr(
                            plugin, f'pre_{func_name}')
                        prehook_return = hook(self, *args, **kwargs)
                        if prehook_return:
                            args = prehook_return
                # Run function
                if override_func:
                    output = override_func(
                        self, *args, **kwargs)
                else:
                    output = func(
                        self, *args, **kwargs)
                # Post-function plugins
                for plugin in self.plugins:
                    if hasattr(plugin, f'post_{func_name}'):
                        hook = getattr(plugin, f'post_{func_name}')
                        og_output = output
                        if isinstance(output, (tuple, list)):
                            output = hook(self, *output)
                        elif output is None:
                            output = hook(self)
                        else:
                            output = hook(self, output)
                        if output is None:
                            output = og_output
            else:
                output = func(self, *args, **kwargs)
            return output
        return hooked
