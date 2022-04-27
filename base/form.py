import copy


class Form:
    def __init__(self, elements: dict, title: str = ""):
        self.title = title
        self.elements = elements
        self._init_elements = copy.deepcopy(elements)

    def display(self):
        print(self.title)
        for key, element in self.elements.items():
            element.display()

    def set_title(self, title: str):
        self.title = title

    def reset(self):
        self.elements = copy.deepcopy(self._init_elements)

    def get_data(self) -> dict:
        return {key: element.value for key, element in self.elements.items()}
