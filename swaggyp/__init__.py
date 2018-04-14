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

class Info(Swag):
    title = CharProperty(required=True)
    description = CharProperty()
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


class SwaggerTemplate(Swag):
    swagger = CharProperty(default_value="2.0")
    host = CharProperty()
    basePath = CharProperty(required=True)
    info = ForeignProperty(Info,required=True)
    paths = ForeignListProperty(Path)
    schemes = ListProperty(required=True)
    consumes = ListProperty()
    produces = ListProperty()

    def to_dict(self):
        obj_dict = remove_nulls(self._data.copy())
        paths = obj_dict.pop('paths')

        path_dict = dict()
        for obj in paths:
            path_dict.update(obj.to_dict())
        obj_dict['paths'] = path_dict
        return obj_dict