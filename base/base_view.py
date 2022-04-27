from abc import ABC


class BaseView(ABC):
    INT_SPACING = 30

    def format(self, str_to_display: str, space_str: str = " ", repeat: int = INT_SPACING) -> str:
        """Adds characters to a string

        Args:
            str_to_display (str): Original string
            space_str (str, optional): Character to add. Defaults to " ".
            repeat (int, optional): Number of characters to add. Defaults to INT_SPACING.

        Returns:
            str: The formatted string
        """
        space_int = repeat - len(str_to_display)
        space_str = space_str * space_int
        return f"{str_to_display}{space_str}"
