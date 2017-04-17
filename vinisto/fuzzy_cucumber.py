import functools
from collections import namedtuple
from string import Formatter
from fuzzywuzzy import fuzz


THRESHOLD = 96
FORMATTER = Formatter()


class Token(namedtuple('Format', 'value')):
    def __init__(self, *args):
        self.value = ' '.join(args)

    @staticmethod
    def tokenize(what):
        pass


Format = namedtuple('Format', 'value')


class StepDefinition(namedtuple('StepDefinition', 'definition, func')):
    def proximity_to(self, step):
        return fuzz.token_sort_ratio(step, self.clean_definition.value)

    @functools.lru_cache()
    def is_token(self, token):
        return isinstance(token, Token)

    @property
    @functools.lru_cache()
    def format(self):
        for strings, tokens, _, _ in FORMATTER.parse(self.definition):
            yield from Token.tokenize(strings)
            yield Format(tokens)

    @property
    @functools.lru_cache()
    def clean_definition(self):
        return Token(*(a for a in self.format if isinstance(a, Token)))


class Cucumber:
    def __init__(self):
        self.step_registry = {
            'given': [],
            'when': [],
            'then': [],
        }
        self.context = {}

        for method in self.step_registry.keys():
            setattr(self, method, lambda x: self.register(method, x))

    def register(self, what, definition):
        def _register(func):
            self.step_registry[what].append(StepDefinition(definition, func))
        return _register

    def execute_step(self, step_type, step):
        """
        Remove all variables from both the step and the definitions.
        Compare what's left.
        """

        sstep = step.split(' ')
        clean_step = ' '.join(
            [a for pos, a in enumerate(sstep) if step.definition_format[pos]])

        for step in self.step_registry[step_type]:
            yielded = False
            if step.proximity_to(clean_step) > THRESHOLD:
                assert not yielded, "Step produced two matches"
                yield step.func(
                    self.context,
                    **{a: sstep[a] for a in step.format if isinstance(a, str)})
                yielded = True
