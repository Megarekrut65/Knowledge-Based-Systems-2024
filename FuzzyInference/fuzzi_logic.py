from typing import Callable


def try_parse(text):
    if (isinstance(text, str)
            and text.startswith('"') and text.endswith('"')
            or text.startswith("'") and text.endswith("'")):
        return text[1:-1]

    types = [int, float, bool]

    for type_ in types:
        try:
            return type_(text)
        except:
            pass

    return text


class FuzzySet:
    def __init__(self, items: str | dict = "", surface: list = None):
        """
        :param items: items from fuzzy set like 'a/0.1; b/0.2; c/1 ...' or '{a/0.1; b/0.2; c/1 ...}' or
        like dict: {a:0.1, b:0.2, c:1 ...}
        :param surface: fuzzy surface like [a, b, c ...]. If no provided - takes from items
        """

        self.__items = {}

        if isinstance(items, str):
            parts = items.replace("{", "").replace("}", "").split(";")
            self.__items = {try_parse(elem[0]): float(elem[1])
                            for part in parts if len(elem := part.strip().split("/")) == 2}
        elif isinstance(items, dict):
            self.__items = items

        if surface is None:
            self.__surface = list(self.__items.keys())
            return

        self.__surface = surface

        for item in surface:
            if self.__items.get(item, None) is None:
                self.__items[item] = 0

    def __getitem__(self, item):
        return self.__items[item]

    def surface(self):
        return self.__surface

    def items(self):
        return self.__items.items()

    def __str__(self):
        return "{" + "; ".join([f"{key}/{item}" for key, item in self.__items.items()]) + "}"


class FuzzyRelation:
    def __init__(self, set1: FuzzySet, set2: FuzzySet, norm_func: Callable[[float, float], float] = min):
        """

        :param set1: first fuzzy set
        :param set2: second fuzzy set
        :param norm_func: T-norm function for relation
        """

        self.__relations = {}
        self.__surface1 = set1.surface()
        self.__surface2 = set2.surface()
        self.__norm_func = norm_func

        for elem1, freq1 in set1.items():
            for elem2, freq2 in set2.items():
                self.__relations[(elem1, elem2)] = norm_func(freq1, freq2)

    def surfaces(self):
        return self.__surface1, self.__surface2

    def get(self, item1, item2):
        return self.__relations[(item1, item2)]

    def transpose(self):
        instance = FuzzyRelation(FuzzySet(), FuzzySet(), norm_func=self.__norm_func)
        instance.__surface1 = self.__surface2
        instance.__surface2 = self.__surface1

        for item1, item2, freq in self.__relations.items():
            instance.__relations[(item2, item1)] = freq

        return instance

    def aggregate(self, other: "FuzzyRelation", agg_func: Callable[[float, float], float] = max):
        if set(self.__surface1) != set(other.__surface1) or set(self.__surface2) != set(other.__surface2):
            raise ArithmeticError("Can't aggregate relations with different surfaces!")

        instance = FuzzyRelation(FuzzySet(), FuzzySet())
        instance.__surface1 = self.__surface1
        instance.__surface2 = self.__surface2

        for item1 in self.__surface1:
            for item2 in self.__surface2:
                key = (item1, item2)
                instance.__relations[key] = agg_func(self.__relations[key], other.__relations[key])

        return instance

    def __str__(self):
        return "\n".join(
            [" ".join([str(self.__relations.get((item1, item2), 0)) for item2 in self.__surface2])
             for item1 in self.__surface1])


def build_inference(input_set: FuzzySet, relation: FuzzyRelation, func_in: Callable[[float, float], float]=min,
                     func_out: Callable[[float, float], float]=max) -> FuzzySet:
    input_surface, output_surface = relation.surfaces()
    if set(input_set.surface()) != set(input_surface):
        raise ArithmeticError("Can't build inference for set and relation with different surfaces!")

    output_set = {}

    for item2 in output_surface:
        res = None
        for item1 in input_surface:
            value = func_in(input_set[item1], relation.get(item1, item2))
            if res is None:
                res = value
            else:
                res = func_out(res, value)

        output_set[item2] = res

    return FuzzySet(output_set)