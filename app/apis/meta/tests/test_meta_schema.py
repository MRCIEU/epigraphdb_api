from pydantic import create_model_from_typeddict

from ..schema import MetaSchemaData, process_schema


def test_process_schema():
    SchemaModel = create_model_from_typeddict(MetaSchemaData)
    schema_data = process_schema()
    assert SchemaModel(**schema_data)
