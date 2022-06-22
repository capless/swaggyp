import yaml
import json

from valley.exceptions import ValidationException
from valley.properties import *
from valley.contrib import Schema
from valley.utils.json_utils import ValleyEncoderNoType


def remove_nulls(obj_dict):
    null_keys = []
    for k, v in obj_dict.items():
        if v == None:
            null_keys.insert(0, k)
    for k in null_keys:
        obj_dict.pop(k)
    return obj_dict


TYPE_CHOICES = {
    'string': 'string',
    'number': 'number',
    'integer': 'integer',
    'boolean': 'boolean',
    'array': 'array',
    'file': 'file'
}

IN_CHOICES = {
    'query': 'query',
    'header': 'header',
    'path': 'path',
    'formData': 'formData',
    'body': 'body'
}

COLLECTION_FORMATS = {
    'csv': 'csv',
    'ssv': 'ssv',
    'tsv': 'tsv',
    'pipes': 'pipes',
    'multi': 'multi'
}


class Swag(Schema):

    def __init__(self, **kwargs):
        super(Swag, self).__init__(**kwargs)
        self.validate()

    def to_yaml(self):
        jd = json.dumps(self.to_dict(), cls=ValleyEncoderNoType)
        # TODO: Write this without converting to JSON first
        jl = json.loads(jd)
        return yaml.safe_dump(jl,
                              default_flow_style=False)

    def to_json(self):
        return json.dumps(self.to_dict(), cls=ValleyEncoderNoType)

    def to_dict(self):
        return remove_nulls(self.cleaned_data.copy())


class Contact(Swag):
    name = CharProperty()
    url = CharProperty()
    email = EmailProperty()


class License(Swag):
    name = CharProperty()
    url = CharProperty()


class XML(Swag):
    name = CharProperty()
    namespace = CharProperty()
    prefix = CharProperty()
    attribute = BooleanProperty()
    wrapped = BooleanProperty()


class ExternalDocs(Swag):
    description = CharProperty()
    url = CharProperty(required=True)


class SwagSchema(Swag):
    ref = CharProperty()
    _format = CharProperty()
    title = CharProperty()
    description = CharProperty()
    default = DictProperty()
    multipleOf = FloatProperty()
    maximum = IntegerProperty()
    exclusiveMaximum = IntegerProperty()
    minimum = IntegerProperty()
    exclusiveMinimum = IntegerProperty()
    maxLength = IntegerProperty()
    minLength = IntegerProperty()
    pattern = CharProperty()
    maxItems = IntegerProperty()
    minItems = IntegerProperty()
    uniqueItems = BooleanProperty()
    maxProperties = IntegerProperty()
    minProperties = IntegerProperty()
    required = ListProperty()
    enum = ListProperty()
    items = DictProperty()
    properties = DictProperty()
    additionalProperties = DictProperty()
    allOf = ListProperty()
    discriminator = CharProperty()
    readOnly = BooleanProperty()
    xml = ForeignProperty(XML)
    externalDocs = ForeignProperty(ExternalDocs)
    example = BaseProperty()
    _type = CharProperty()

    def to_dict(self):
        obj_dict = super(SwagSchema, self).to_dict()
        _format = obj_dict.pop('_format', None)
        _type = obj_dict.pop('_type', None)
        ref = obj_dict.pop('ref', None)
        if ref:
            obj_dict['$ref'] = ref
        if _format:
            obj_dict['format'] = _format
        if _type:
            obj_dict['type'] = _type
        return obj_dict


class Item(Swag):
    _type = CharProperty(choices=TYPE_CHOICES)
    _format = CharProperty()
    collectionFormat = CharProperty(choices=COLLECTION_FORMATS, default_value='csv')
    default = BaseProperty()
    maximum = IntegerProperty()
    exclusiveMaximum = BooleanProperty()
    minimum = IntegerProperty()
    exclusiveMinimum = BooleanProperty()
    maxLength = IntegerProperty()
    minLength = IntegerProperty()
    pattern = CharProperty()
    maxItems = IntegerProperty()
    minItems = IntegerProperty()
    uniqueItems = BooleanProperty()
    enum = ListProperty()
    multipleOf = FloatProperty()

    def to_dict(self):
        obj_dict = super(Item, self).to_dict()
        _format = obj_dict.pop('_format', None)
        _type = obj_dict.pop('_type', None)
        if _type:
            obj_dict['type'] = _type
        if _format:
            obj_dict['format'] = _format
        return obj_dict


class Parameter(Item):
    name = CharProperty()
    _in = CharProperty(required=True, choices=IN_CHOICES)
    description = CharProperty()
    required = BooleanProperty()
    items = ForeignProperty(Item)
    allowEmptyValue = BooleanProperty()
    schema = ForeignProperty(SwagSchema)

    def to_dict(self):
        obj_dict = super(Parameter, self).to_dict()
        _in = obj_dict.pop('_in')
        schema = obj_dict.get('schema')

        obj_dict['in'] = _in
        if _in != 'body' and self.cleaned_data.get('_type') == None:
            raise ValidationException('_type is required if _in is not equal to "body"')
        if _in == 'path':
            obj_dict.pop('allowEmptyValue')
        if _in == 'body' and schema:
            obj_dict.pop('allowEmptyValue')
            obj_dict.pop('collectionFormat')
            obj_dict.pop('exclusiveMaximum')
            obj_dict.pop('exclusiveMinimum')
            obj_dict.pop('uniqueItems')
        return obj_dict


class Info(Swag):
    title = CharProperty(required=True)
    description = CharProperty()
    termsOfService = CharProperty()
    contact = ForeignProperty(Contact)
    license = ForeignProperty(License)
    version = CharProperty(required=True)


class Response(Swag):
    status_code = IntegerProperty(required=True)
    description = CharProperty()
    schema = ForeignProperty(SwagSchema)

    def to_dict(self):
        obj_dict = remove_nulls(self.cleaned_data.copy())
        status_code = obj_dict.pop('status_code')
        return {status_code: obj_dict}


class Operation(Swag):
    http_method = CharProperty(required=True)
    summary = CharProperty()
    description = CharProperty()
    externalDocs = DictProperty()
    operationId = CharProperty()
    consumes = ListProperty()
    produces = ListProperty()
    parameters = ForeignListProperty(Parameter)

    responses = ForeignListProperty(Response)

    def to_dict(self):
        obj_dict = super(Operation, self).to_dict().copy()
        http_method = obj_dict.pop('http_method')
        responses = obj_dict.pop('responses')
        resp_dict = dict()
        for resp in responses:
            resp_dict.update(resp.to_dict())

        obj_dict['responses'] = resp_dict
        return {http_method: obj_dict}


class Path(Swag):
    endpoint = CharProperty(required=True)
    operations = ForeignListProperty(Operation)

    def to_dict(self):
        obj_dict = super(Path, self).to_dict()

        endpoint = obj_dict.pop('endpoint')
        operations = obj_dict.pop('operations')
        op_dict = dict()
        for op in operations:
            op_dict.update(op.to_dict())
        return {endpoint: op_dict}


class Definition(Swag):
    name = CharProperty(required=True)
    schema = ForeignProperty(SwagSchema, required=True)

    def to_dict(self):
        obj_dict = super(Definition, self).to_dict()
        name = obj_dict.pop('name')
        schema = obj_dict.pop('schema')
        return {name: schema}


class SwaggerTemplate(Swag):
    swagger = CharProperty(default_value="2.0")
    info = ForeignProperty(Info, required=True)
    host = CharProperty()
    basePath = CharProperty(required=True)
    schemes = ListProperty(required=True)
    consumes = ListProperty()
    produces = ListProperty()
    paths = ForeignListProperty(Path)
    definitions = ForeignListProperty(Definition)
    parameters = DictProperty()
    responses = DictProperty()
    securityDefinitions = DictProperty()
    security = DictProperty()
    tags = DictProperty()
    externalDocs = DictProperty()

    def to_dict(self):
        obj_dict = super(SwaggerTemplate, self).to_dict().copy()
        paths = obj_dict.pop('paths', [])
        definitions = obj_dict.pop('definitions', None)
        if definitions:
            obj_dict['definitions'] = {i.cleaned_data.get('name'): i.cleaned_data.get(
                'schema') for i in definitions}
        path_dict = dict()
        if paths:
            for obj in paths:
                path_dict.update(obj.to_dict())
            obj_dict['paths'] = path_dict
        return obj_dict

    def add_path(self, path):
        self._base_properties.get('paths').validate([path], 'paths')
        paths = self.cleaned_data.get('paths') or []
        paths.append(path)
        self.cleaned_data['paths'] = list(set(paths))
