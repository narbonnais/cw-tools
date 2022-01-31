import json
from pprint import pprint
import sys
from typing import Dict, List, Set
import os
from holders import ClassHolder, ParamHolder, FunctionHolder
from parsers import RootSchema, SchemaObject, Metadata


def get_json_data(path: str) -> json:
    """
    Simply reads a file from path and returns data in JSON format
    """
    with open(path) as f:
        raw_data = f.read()
        json_data = json.loads(raw_data)
        return json_data


def process_arguments(argv: list) -> str:
    """
    Extract `path` argument from the console or exit
    """
    if len(sys.argv) < 2:
        print("usage: python3 schema_to_class.py ./terraswap/contracts/terraswap_token")
        print("commands list: python3 schema_to_class.py -h")
        exit()

    path = sys.argv[1]

    arguments = sys.argv

    if "-h" in arguments or "-help" in arguments:
        print("usage: python3 schema_to_class.py ./terraswap/contracts/terraswap_token")
        print("commands list: python3 schema_to_class.py -h")
        exit()

    return path


def extract_name_from_path(contract_path: str) -> str:
    """
    Extract the name of the contract by splitting `/`. Assumes that contracts are located
    in a `contracts` folder
    """
    contract_path = contract_path.split("/")

    index_of_contract = contract_path.index("contracts")
    index_of_name = index_of_contract + 1

    return contract_path[index_of_name]


simple_types = {"array": "list",
                "boolean": "bool",
                "integer": "int",
                "null": "None",
                "number": "float",
                "object": "dict",
                "string": "str"}


def collect_schemas(contract_path: str) -> List[RootSchema]:
    """
    Goes into `contract_path` directory, list the messages (only) schemas,
    and returns the schemas in a list
    :param contract_path: path of the contract directory, father of the `/schema/` dir
    """
    res = []
    schema_directory_path = f"{contract_path}/schema/"
    for schema_path in os.listdir(schema_directory_path):
        # We don't use the Response res
        if not schema_path.endswith("msg.json"):
            continue

        schema_path = os.path.join(schema_directory_path, schema_path)

        # Extract JSON data and process the schema
        root_data = get_json_data(schema_path)
        res.append(root_data)
    return res


def build(contract_name: str, contract_path: str) -> None:
    classes = []
    defined_types = []  # [{'Uint128': 'str'}]
    root_schemas_data = collect_schemas(contract_path)
    class_holder = ClassHolder(contract_name.capitalize())

    # Go through each JSON msg data
    for root_schema_data in root_schemas_data:

        # Parse into RootSchema format
        root_schema = RootSchema(root_schema_data)

        # The class object holding all messages constructors
        # Compiled to string at the end of the script

        # If instance is `object`, it is an InstantiateMsg
        if root_schema.schema.instance_type == "object":

            # We want to call it like `Contract.InstantiateMsg()` so we need a function
            func_name = root_schema.schema.metadata.title
            if func_name == "InstantiateMsg":
                func_name = "instantiate"

            function_holder = FunctionHolder(func_name)

            # Go through all properties like `{'claim': {'type': 'object'}}`
            for prop_key in root_schema.schema.properties:

                # There is a required `"required": ["anchor_token","genesis_time","owner"]`
                # at the root of the schema, we check inclusion
                required = False
                if root_schema.schema.required:
                    required = prop_key in root_schema.schema.required

                # Get the type of the prop, and map it to a python type
                # ex: integer -> int, string -> str
                type_instance = None
                if "type" in root_schema.schema.properties[prop_key]:
                    type_instance = root_schema.schema.properties[prop_key]["type"]

                    # Sometimes they could be a type like [str, null], we take the first one
                    if type(type_instance) == list:
                        type_instance = type_instance[0]

                    # Map to python type
                    if type_instance in simple_types:
                        type_instance = simple_types[type_instance]
                    else:
                        pass  # TODO
                else:
                    pass  # TODO

                # Add the parameter to the InstantiateMsg function holder
                function_holder.add_param(ParamHolder(
                    prop_key, type_instance, required))

            # Add the function holder to the class holder
            class_holder.add_function(function_holder)

        # Else, it is a ExecuteMsg or QueryMsg
        else:

            # Get the prefix (execute or query)
            prefix = root_schema.schema.metadata.title
            if prefix == "ExecuteMsg":
                prefix = "execute"
            elif prefix == "QueryMsg":
                prefix = "query"
            elif prefix == "Cw20HookMsg":
                prefix = "cw20"

            # Messages are pretty deep in the object:
            # ./oneOf/{message index}/properties/{message definition}

            schema_object: SchemaObject
            schema_list = []
            if root_schema.schema.any_of:
                for s in root_schema.schema.any_of:
                    schema_list.append(s)
            if root_schema.schema.one_of:
                for s in root_schema.schema.one_of:
                    schema_list.append(s)
            for schema_object in schema_list:
                # ./oneOf/{message index}

                for func_name in schema_object.properties:
                    func_schema = SchemaObject(
                        schema_object.properties[func_name])

                    # We want to call it like `Contract.InstantiateMsg()` so we need a function
                    function_holder = FunctionHolder(func_name, prefix, True)

                    # Go through all properties like `{'claim': {'type': 'object'}}`
                    # Sometimes it could just be `{'claim': {}}`
                    if func_schema.properties == None:
                        continue
                    for prop_key in func_schema.properties:

                        # There is a required `"required": ["anchor_token","genesis_time","owner"]`
                        # at the root of the schema, we check inclusion
                        required = False
                        if func_schema.required:
                            required = prop_key in func_schema.required

                        # Get the type of the prop, and map it to a python type
                        # ex: integer -> int, string -> str
                        # Sometimes it may be a ref to a definition `{'$ref': '#/definitions/Uint128'}`
                        type_instance = None
                        if "type" in func_schema.properties[prop_key]:
                            type_instance = func_schema.properties[prop_key]["type"]

                            # Sometimes they could be a type like [str, null], we take the first one
                            if type(type_instance) == list:
                                type_instance = type_instance[0]

                            # Map to python type
                            if type_instance in simple_types:
                                type_instance = simple_types[type_instance]
                            else:
                                pass  # TODO
                        else:
                            pass  # TODO

                        # Add the parameter to the InstantiateMsg function holder
                        function_holder.add_param(ParamHolder(
                            prop_key, type_instance, required))

                        # lines = function_holder.build_lines()
                        # print("\n".join(lines))

                # Add the function holder to the class holder
                class_holder.add_function(function_holder)
    # Compile the class holder to string
    lines = class_holder.build_lines()
    print("\n".join(lines))


def main():
    """
    # Entry function
    Expects the program to receive 1 argument, specifying the directory to handle.
    """

    contract_path = process_arguments(sys.argv)
    contract_name = extract_name_from_path(contract_path)

    build(contract_name, contract_path)


if __name__ == "__main__":
    main()
