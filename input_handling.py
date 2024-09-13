from typing import Any, Callable, Optional
class Input:
    """
    A class to handle user input, encapsulating setting, retrieving, and type coercion of input values.

    Attributes:
        _input: Stores the current input value, initially set to None.
    """
    def __init__(self):
        """Initializes the Input object with a default value of None."""
        self._input = None 
    
    def set(self, value: Any) -> None:
        """
        Sets the input value.

        Args:
            value (Any): The value to set as input.
        """
        self._input = value 
    
    def get(self) -> Any: 
        """
        Retrieves the current input value.

        Returns:
            Any: The stored input value, or None if no input has been set.
        """
        return self._input
    
    def force_type(self, value:object, target_type:Callable[[Any], Any]) -> Any:
        """
        Attempts to convert the given value to a specified target type.

        Args:
            value (Any): The input value to be converted.
            target_type (Callable): A callable, typically a type like int, float, or str.

        Returns:
            Any: The converted value if successful, or None if the conversion fails.
        """
        try: 
            return target_type(value)
        except (ValueError, TypeError):
            return None 
    
    def read(self, prompt:str="", force_type: Optional[Callable[[Any], Any]]=None) -> Any:
        """
        Prompts the user for input and optionally forces a type conversion.

        Args:
            prompt (str): A prompt string displayed to the user.
            force_type (Optional[Callable]): A callable to convert the user input, such as int or float.

        Returns:
            Any: The user input after optional type conversion, or None if conversion fails.
        """
        user_input = input(prompt)
        if force_type:
            user_input = self.force_type(user_input, force_type)
        self.set(user_input)
        return user_input

    def check_type(self, type:Any) -> bool: 
        """
        Checks if the current input value matches the specified type.

        Args:
            target_type (Any): The type to check against (e.g., int, float, str).

        Returns:
            bool: True if the input matches the target type, False otherwise.
        """
        return isinstance(self.get(), type)
    
# InputGroup is a dictionary mapping strings (keys) to Input objects (values)
InputGroup = dict[str, Input]