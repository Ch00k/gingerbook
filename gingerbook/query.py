import re

from .utils import read_data


class Query(object):
    def __init__(self, entity_class, datastore):
        self.entity_class = entity_class
        self.datastore = datastore

    def all(self):
        data = read_data(datastore=self.datastore)
        return [self.entity_class(**record) for record in data[self.entity_class.__tablename__]]

    def filter(self, *expressions):
        expression_pattern = re.compile(r'^(.*)\s(is|not|contains)\s(.*)$')
        parsed_expressions = []
        for expression in expressions:
            match = re.match(expression_pattern, expression)
            if not match:
                raise RuntimeError("Expression '{0}' is incorrect".format(expression))
            parsed_expressions.append(match.groups())

        data = read_data(datastore=self.datastore)
        relevant = data[self.entity_class.__tablename__]
        result = []

        for field, operator, term in parsed_expressions:
            expression_result = []
            for obj in relevant:
                if field not in obj:
                    raise RuntimeError(
                        "{0} does not have {1} field".format(self.entity_class.__name__, field)
                    )

                if operator == 'is':
                    if isinstance(obj[field], list):
                        if term in obj[field]:
                            expression_result.append(obj['id'])
                    else:
                        if obj[field] == term:
                            expression_result.append(obj['id'])

                elif operator == 'not':
                    if isinstance(obj[field], list):
                        if term not in obj[field]:
                            expression_result.append(obj['id'])
                    else:
                        if obj[field] != term:
                            expression_result.append(obj['id'])

                elif operator == 'contains':
                    if isinstance(obj[field], list):
                        if any(term in item for item in obj[field]):
                            expression_result.append(obj['id'])
                    else:
                        if term in obj[field]:
                            expression_result.append(obj['id'])

                result.append(expression_result)

        result = set.intersection(*map(set, result))
        result = [item for item in relevant if item['id'] in result]

        return [self.entity_class(**record) for record in result]
