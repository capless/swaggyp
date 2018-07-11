import yaml
import json
from valley.properties import *
from valley.contrib import Schema
from valley.utils.json_utils import ValleyEncoderNoType


class Swag(Schema):

    def __init__(self,**kwargs):
        super(Swag, self).__init__(**kwargs)
        self.validate()

    def to_yaml(self):
        jd = json.dumps(self.to_dict(),cls=ValleyEncoderNoType)
        #TODO: Write this without converting to JSON first
        jl = json.loads(jd)
        return yaml.safe_dump(jl,
                              default_flow_style=False)

    def to_json(self):
        return json.dumps(self.to_dict(),cls=ValleyEncoderNoType)

def remove_nulls(obj_dict):
    null_keys = []
    for k, v in obj_dict.items():
        if not v:
            null_keys.insert(0, k)
    for k in null_keys:
        obj_dict.pop(k)
    return obj_dict


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
    _type = ListProperty()

    def to_dict(self):
        obj_dict = remove_nulls(self._data.copy())
        _format = obj_dict.pop('_format')
        _type = obj_dict.pop('_type')
        if _format:
            obj_dict['format'] = _format
        if _type:
            obj_dict['type'] = _type
        return obj_dict

class Parameter(Swag):
    name = CharProperty()
    _in = CharProperty(required=True,choices=['query','header','path','formData','body'])
    description = CharProperty()
    required = BooleanProperty()
    schema = ForeignProperty(SwagSchema)

    def to_dict(self):
        obj_dict = remove_nulls(self._data.copy())
        _in = obj_dict.pop('_in')
        obj_dict['in'] = _in
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

    def to_dict(self):
        obj_dict = remove_nulls(self._data.copy())
        status_code = obj_dict.pop('status_code')
        return {status_code:obj_dict}

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
        obj_dict = remove_nulls(self._data.copy())
        http_method = obj_dict.pop('http_method')
        responses = obj_dict.pop('responses')
        resp_dict = dict()
        for resp in responses:
            resp_dict.update(resp.to_dict())

        obj_dict['responses'] = resp_dict
        return {http_method:obj_dict}


class Path(Swag):
    endpoint = CharProperty(required=True)
    operations = ForeignListProperty(Operation)

    def to_dict(self):
        obj_dict = remove_nulls(self._data.copy())

        endpoint = obj_dict.pop('endpoint')
        operations = obj_dict.pop('operations')
        op_dict = dict()
        for op in operations:
            op_dict.update(op.to_dict())
        return {endpoint:op_dict}


class Definition(Swag):
    name = CharProperty(required=True)
    schema = ForeignProperty(SwagSchema,required=True)

    def to_dict(self):
        obj_dict = remove_nulls(self._data.copy())
        name = obj_dict.pop('name')
        schema = obj_dict.pop('schema')
        return {name:schema}


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
        obj_dict = remove_nulls(self._data.copy())
        paths = obj_dict.pop('paths')
        definitions = obj_dict.pop('definitions')
        if definitions:
            obj_dict['definitions'] = {i._data.get('name'):i._data.get(
                'schema') for i in definitions}
        path_dict = dict()
        for obj in paths:
            path_dict.update(obj.to_dict())
        obj_dict['paths'] = path_dict
        return obj_dict