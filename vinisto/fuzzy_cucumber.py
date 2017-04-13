import parse


class Cucumber:
    def __init__(self):
        self.step_registry = {
            'given': [],
            'when': [],
            'then': [],
        }
        # No hooks right now.
        self.context = {}

        for method in self.step_registry.keys():
            setattr(self, method, lambda x: self.register(method, x))

    @staticmethod
    def guess_type(step):
        # TODO, this will be handled by the gherkins parser
        return step.split(' ')[0]

    def execute_step(self, step):
        step_type = self.guess_type(step)
        for definition, func in self.step_registry[step_type]:
            result = definition.parse(step)
            if result:
                func(self.context, **result)

    def register(self, what, phrase):
        def _register(func):
            self.step_registry[what].append({parse.compile(phrase): func})
        return _register
