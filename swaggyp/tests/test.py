from unittest import TestCase
from swaggyp import (Swag, Contact, License, XML, ExternalDocs, SwagSchema,
                     Item, Parameter, Info, Response, Operation, Path, Definition, SwaggerTemplate)


class SwaggyP(TestCase):

    def setUp(self):
        self.info = Info(
            title='An API information',
            version='v1'
        )
        self.operation = [Operation(
            http_method='POST',
            summary='An endpoint summary',
            description='This is to create a user',
            responses=[
                    Response(status_code=200, description='Test Response')],
            consumes=['application/json',
                      'application/x-www-form-urlencoded'],
            produces=['application/json',
                      'application/x-www-form-urlencoded'])]
        self.paths = [Path(endpoint='/user', operations=self.operation)]
        self.definitions = Definition(name='User',
                                      schema=SwagSchema(ref='#/definitions/User'))

    def test_swag(self):
        obj = Swag()
        obj.to_yaml()
        obj.to_dict()
        obj.to_json()

        # if there are no exception, then everything passes
        self.assertTrue(True)

    def test_contact(self):
        obj = Contact(
            name='contact_name',
            url='https://url.com',
            email='definitelynotanonymous@email.com')
        obj.to_yaml()
        obj.to_dict()
        obj.to_json()
        self.assertTrue(True)

    def test_license(self):
        obj = License(name='License MD5', url='https://url.com')
        obj.to_yaml()
        obj.to_dict()
        obj.to_json()
        self.assertTrue(True)

    def test_xml(self):
        obj = License(
            name='XML',
            namespace='namespace',
            prefix='pref',
            attribute=True,
            wrapped=True)
        obj.to_yaml()
        obj.to_dict()
        obj.to_json()
        self.assertTrue(True)

    def test_external_docs(self):
        obj = ExternalDocs(
            description='ext docs desc',
            url='https://somewheredowntheroad.com')
        obj.to_yaml()
        obj.to_dict()
        obj.to_json()
        self.assertTrue(True)

    def test_swag_schema_ref(self):
        obj = SwagSchema(ref='#/definitions/Model')
        obj.to_yaml()
        obj.to_dict()
        obj.to_json()

        self.assertIn('$ref', obj.to_json())

    def test_item(self):
        obj = Item(
            _type='string',
            _format='csv',
        )
        obj.to_yaml()
        obj.to_dict()
        obj.to_json()

        self.assertIn('type', obj.to_json())
        self.assertIn('format', obj.to_json())

    def test_parameter_in_body(self):
        obj = Parameter(
            _in='body',
            schema=SwagSchema(ref='#/definitions/User')
        )
        obj.to_yaml()
        obj.to_dict()
        obj.to_json()
        obj_in_json = obj.to_json()

        self.assertNotIn(obj_in_json, 'allowEmptyValue')
        self.assertNotIn(obj_in_json, 'collectionFormat')
        self.assertNotIn(obj_in_json, 'exclusiveMaximum')
        self.assertNotIn(obj_in_json, 'exclusiveMinimum')
        self.assertNotIn(obj_in_json, 'uniqueItems')

    def test_parameter_in_path(self):
        obj = Parameter(
            _in='path',
            _type='string',
            name='path_name',
            description='A path param',
            required=True,
            allowEmptyValue=False,
        )
        obj.to_yaml()
        obj.to_dict()
        obj.to_json()
        obj_in_json = obj.to_json()

        self.assertNotIn(obj_in_json, 'allowEmptyValue')

    def test_info(self):
        obj = Info(
            title='An API information',
            version='v1'
        )
        obj.to_yaml()
        obj.to_dict()
        obj.to_json()
        self.assertTrue(True)

    def test_response(self):
        obj = Response(
            status_code=200,
            description='Operation success'
        )
        obj.to_yaml()
        obj.to_dict()
        obj.to_json()

        self.assertEqual(
            obj.to_dict(),
            {200: {'description': 'Operation success'}})

    def test_operation(self):
        obj = Operation(
            http_method='POST',
            summary='An endpoint summary',
            description='This is to create a user',
            responses=[
                Response(status_code=200, description='Test Response')],
            consumes=['application/json',
                      'application/x-www-form-urlencoded'],
            produces=['application/json',
                      'application/x-www-form-urlencoded'])
        obj.to_yaml()
        obj.to_dict()
        obj.to_json()

        expected = {"POST": {
            "summary": "An endpoint summary",
            "description": "This is to create a user",
            "consumes": ["application/json", "application/x-www-form-urlencoded"],
            "produces": ["application/json", "application/x-www-form-urlencoded"],
            "responses": {200: {"description": "Test Response"}}}}
        self.assertEqual(obj.to_dict(), expected)

    def test_path(self):
        obj = Path(
            endpoint='/user',
            operations=[Operation(
                http_method='POST',
                summary='An endpoint summary',
                description='This is to create a user',
                responses=[
                    Response(status_code=200, description='Test Response')],
                consumes=['application/json',
                          'application/x-www-form-urlencoded'],
                produces=['application/json',
                          'application/x-www-form-urlencoded'])]
        )
        obj.to_yaml()
        obj.to_dict()
        obj.to_json()
        self.assertTrue(True)

    def test_definition(self):
        obj = Definition(name='User',
                         schema=SwagSchema(ref='#/definitions/User'))
        obj.to_yaml()
        obj.to_dict()
        obj.to_json()
        self.assertTrue(True)

    def test_swagger_template(self):
        obj = SwaggerTemplate(
            info=self.info,
            host='swaggyp',
            basePath='/',
            paths=self.paths,
            schemes=['http', 'https'],
            definitons=self.definitions
        )
