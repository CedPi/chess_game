import re
from abc import ABC, abstractmethod
from datetime import datetime


class Widget(ABC):
    def __init__(self, label: str, error_msg: str, required: bool):
        self.label = label
        self._error_msg = error_msg
        self.required = required
        self.init()

    def init(self):
        self.value = None
        self._is_valid = False
        self._first_entry = True

    def display(self):
        while not self._is_valid:
            if not self._first_entry:
                print(f"\n/!\\ ERREUR: {self._error_msg}")
            self._first_entry = False
            self.value = input(self.label)
            self._is_valid = self._check()
            if not self.required:
                self._is_valid = True

    @abstractmethod
    def _check(self) -> bool():
        pass


class WidgetText(Widget):
    def __init__(self, label: str, error_msg: str, required=True):
        super().__init__(label, error_msg, required)

    def _check(self):
        if self.required:
            if self.value == "":
                return False
            pattern = re.compile("^[a-zA-Z+]+$")
            return re.search(pattern, self.value)


class WidgetInt(Widget):
    def __init__(self, label: str, error_msg: str, required=True):
        super().__init__(label, error_msg, required)

    def _check(self):
        pattern = re.compile("^[0-9]+$")
        return re.search(pattern, self.value)


class WidgetIntRange(Widget):
    def __init__(self, label: str, error_msg: str, min=0, max=100, required=True):
        super().__init__(label, error_msg, required)
        self.min = min
        self.max = max

    def _check(self):
        pattern = re.compile("^[0-9]+$")
        pattern_is_valid = re.search(pattern, self.value)
        if pattern_is_valid:
            self.value = int(self.value)
        range_is_valid = self.min <= self.value <= self.max
        return pattern_is_valid and range_is_valid


class WidgetAlphaNum(Widget):
    def __init__(self, label: str, error_msg: str, required=True):
        super().__init__(label, error_msg, required)

    def _check(self):
        pattern = re.compile("^[a-zA-Z0-9 ]+$")
        return re.search(pattern, self.value)


class WidgetDate(Widget):
    def __init__(self, label: str, error_msg: str, required=True):
        super().__init__(label, error_msg, required)

    def _check(self):
        if self.required and self.value == "":
            return False
        try:
            datetime.strptime(self.value, "%d/%m/%Y")
            return True
        except ValueError:
            return False


class WidgetChoice(Widget):
    def __init__(self, label: str, error_msg: str, choices: list):
        super().__init__(label, error_msg, required=True)
        self.choices = choices

    def _check(self):
        if self.value not in self.choices:
            return False
        return True


class WidgetMultiChoices(WidgetChoice):
    def __init__(
        self,
        label: str,
        error_msg: str,
        choices: dict,
        separator=" ",
        choice_number=8,
        prompt="Vos choix (séparés par un espace): ",
    ):
        super().__init__(label, error_msg, choices)
        self.separator = separator
        self.choice_number = choice_number
        self.prompt = prompt

    def _check(self):
        self.value = self.value.split(sep=self.separator)
        if len(self.value) != self.choice_number:
            self._error_msg = f"Vous devez sélectionner {self.choice_number} éléments"
            return False
        duplicates = [choice for choice in self.value if self.value.count(choice) > 1]
        if len(duplicates) > 0:
            self._error_msg = "Il y a des doublons dans votre sélection"
            return False
        for choice in self.value:
            if choice not in self.choices.keys():
                self._error_msg = "Au moins un choix ne fait pas partie de la liste"
                return False
        return True

    def display(self):
        while not self._is_valid:
            if not self._first_entry:
                print(f"\n/!\\ ERREUR: {self._error_msg}")
            self._first_entry = False
            self.value = print(self.label)
            for key, choice in self.choices.items():
                print(f"\t{key} : {choice}")
            self.value = input(self.prompt)
            self._is_valid = self._check()


class WidgetMenu(Widget):
    def __init__(self, label: str, error_msg: str, options: dict, prompt="Votre choix: "):
        super().__init__(label, error_msg, required=True)
        self.options = options
        self.prompt = prompt

    def display(self):
        while not self._is_valid:
            if not self._first_entry:
                print(f"\n/!\\ ERREUR: {self._error_msg}")
            self._first_entry = False
            self.value = print(self.label)
            for key, option in self.options.items():
                print(f"\t{key} : {option}")
            self.value = input(self.prompt)
            self._is_valid = self._check()

    def _check(self):
        if self.value not in self.options.keys():
            return False
        return True
