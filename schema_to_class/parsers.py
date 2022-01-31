from typing import Dict, List, Set


class Metadata():
    id: str = None
    title: str = None
    description: str = None
    default = None
    deprecated: bool = None
    read_only: bool = None
    write_only: bool = None
    examples: list = None

    def __init__(self, schema_data) -> None:
        if '$id' in schema_data:
            self.id = schema_data['$id']
        if 'title' in schema_data:
            self.title = schema_data['title']
        if 'description' in schema_data:
            # usually for definitions
            self.description = schema_data['description']
        if 'default' in schema_data:
            self.default = schema_data['default']
        if 'deprecated' in schema_data:
            self.deprecated = schema_data['deprecated']
        if 'readOnly' in schema_data:
            self.read_only = schema_data['readOnly']
        if 'writeOnly' in schema_data:
            self.write_only = schema_data['writeOnly']
        if 'examples' in schema_data:
            self.examples = schema_data['examples']


class SchemaObject():
    metadata: Metadata
    instance_type = None
    format = None
    enum_values = None
    const_values = None
    ref = None
    items: List = None  # List[SchemaObject]
    required = None  # Set(str)
    properties = None  # Dic[str, SchemaObject]
    any_of = None  # List[SchemaObject]
    one_of = None  # List[SchemaObject]

    def __init__(self, schema_data) -> None:
        # pprint(schema_data)
        self.metadata = Metadata(schema_data)
        if 'type' in schema_data:
            self.instance_type = schema_data['type']
        if '$ref' in schema_data:
            self.ref = schema_data['$ref']
        if 'format' in schema_data:
            self.format = schema_data['format']
        if 'enum' in schema_data:
            self.enum_values = schema_data['enum']
        if 'const' in schema_data:
            self.const_values = schema_data['const']
        if 'items' in schema_data:
            self.items = schema_data['items']
        if 'required' in schema_data:
            self.required = schema_data['required']
        if 'properties' in schema_data:
            self.properties = schema_data['properties']
        if 'anyOf' in schema_data:
            any_of_datas = schema_data['anyOf']
            self.any_of = []
            for any_of_data in any_of_datas:
                self.any_of.append(SchemaObject(any_of_data))
        if 'oneOf' in schema_data:
            one_of_datas = schema_data['oneOf']
            self.one_of = []
            for one_of_data in one_of_datas:
                self.one_of.append(SchemaObject(one_of_data))


class RootSchema():
    """
    https://docs.rs/schemars/latest/schemars/schema/struct.RootSchema.html
    """
    meta_schema: str = None
    schema: SchemaObject = None
    definitions: Dict[str, SchemaObject] = None

    def __init__(self, root_data: dict) -> None:
        if '$schema' in root_data:
            self.meta_schema = root_data['$schema']
        if 'definitions' in root_data:
            self.definitions = dict()
            definitions_data = root_data['definitions']
            for k in definitions_data:
                schema_data = definitions_data[k]
                # May be a boolean ? Never came across this
                self.definitions[k] = SchemaObject(schema_data)
        self.schema = SchemaObject(root_data)

    def getName(self):
        return self.schema.properties.title
