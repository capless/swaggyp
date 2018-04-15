# swaggyp
Python library for generating Swagger API templates

## Install

```python
pip install swaggyp
```
## Example
```python
import swaggyp as sw

info = sw.Info(title='Capless',description='Test site',version='dev')
rsp = sw.Response(status_code=200,description='test')
op = sw.Operation(http_method='GET',summary='Test',description='test',responses=[rsp])
p = sw.Path(endpoint='/dev/',operations=[op])
t = sw.SwaggerTemplate(host='capless.io',basePath='/',info=info,paths=[p],schemes=['https'])

>>t.to_yaml()
basePath: /
host: capless.io
info:
  description: Test site
  title: Capless
  version: dev
paths:
  /dev/:
    GET:
      description: test
      responses:
        '200':
          description: test
      summary: Test
schemes:
- https
swagger: '2.0'


```