import warnings
warnings.warn("This module is deprecated. You want to use defaultdict instead.", DeprecationWarning,
              stacklevel=2)

class Aggregator:
    def __init__(self) -> None:
        pass

    def update(self, *args) -> None:
        pass

    def compute(self):
        pass


class ListAggregator(Aggregator):
    def __init__(self) -> None:
        self.list = []

    def update(self, *args):
        self.list.append(args)

    def compute(self):
        return self.list

class SumAggregator(Aggregator):
    def __init__(self) -> None:
        self.sum = 0

    def update(self, val) -> None:
        self.sum += val

    def compute(self):
        return self.sum


class RatioAggregator(Aggregator):
    def __init__(self) -> None:
        self.positive, self.all = 0, 0

    def update(self, pos, all) -> None:
        self.positive += pos
        self.all += all

    def compute(self):
        return self.positive / self.all


class TaggedAggregator():
    '''
    Compute metrics grouped by tags. 
    '''

    def __init__(self, aggregator: Aggregator):
        self.aggregator_type = aggregator
        self.aggregators = {}

    def update(self, tag, *args) -> None:
        if tag not in self.aggregators:
            self.aggregators[tag] = self.aggregator_type()

        self.aggregators[tag].update(*args)

    def compute(self):
        result = {}
        for tag, aggregator in self.aggregators.items():
            result[tag] = aggregator.compute()
        return result