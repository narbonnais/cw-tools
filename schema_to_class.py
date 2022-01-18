"""
Hello, my job is to make easier the writing of each class for the contracts.
I read the schemas and translate it into python code.

How to use ?
- Go to project root
- in function `main` line 167, change the name of the contract that you want to parse
- run, you should get a result like:

```py
def instantiate_msg(proposal_deposit, quorum, snapshot_period: int, threshold, timelock_period: int, voting_period: int) -> str:
        return {'instantiate': {'proposal_deposit': proposal_deposit, 'quorum': quorum, 'snapshot_period': snapshot_period, 'threshold': threshold, 'timelock_period': timelock_period, 'voting_period': voting_period}}

def execute_receive_msg() -> str:
        return {'receive': {}}

def execute_execute_poll_msgs_msg(poll_id: int) -> str:
        return {'execute_poll_msgs': {'poll_id': poll_id}}
```

Now, create a class and copy & paste result
"""

import json

type_match = {
    'string': 'str',
    'integer': 'int',
    'array': 'list',
}


class Param():
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type
        self.required = False

    def to_string(self):
        return f"({self.name}, {self.type}, {self.required})"


class Message():
    def __init__(self, name: str, prefix: str = None):
        self.name = name
        self.params = []
        self.prefix = prefix

    def add_param(self, param_name: str, param_type: str = None) -> None:
        if param_type in type_match:
            param_type = type_match[param_type]
        else:
            param_type = None
        param = Param(param_name, param_type)
        self.params.append(param)
        # print(f"Added {param.to_string()} to {self.name}")

    def require_param(self, param_name):
        for p in self.params:
            if p.name == param_name:
                p.required = True

    def compile_params(self) -> str:
        # sort params first
        sorted_params = sorted(self.params, key=lambda p: not p.required)

        res = ""
        for p in sorted_params:
            # Get data from param
            name = p.name
            type = p.type
            required = p.required
            # Create string
            res += name
            if type:
                res += f": {type}"
            if not required:
                res += " = None"
            res += ", "
        # Strip the last ", "
        res = res.strip(", ")
        return res

    def compile_body(self) -> str:
        res = "return "
        res += "{'" + self.name + "': {"
        for p in self.params:
            name = p.name
            # Create string
            res += f"'{name}': {name}, "
        res = res.strip(", ")
        res += "}}"
        return res

    def compile(self) -> str:
        params = self.compile_params()
        body = self.compile_body()
        prefix = ""
        if self.prefix:
            prefix = self.prefix + "_"
        res = f"def {prefix}{self.name}_msg({params}) -> str:\n"
        res += f"\t{body}\n"

        return res


# msg = Message("execute_vesting_account")
# msg.add_param("address", "str")
# msg.add_param("address", "str")

def process_schema(schema, prefix: str):
    """
    Takes the json schema as input and returns the string that has to be written in the contract file
    """
    if "anyOf" not in schema:
        # It's an instantiate message
        buffer_msg = Message("instantiate")
        if "properties" in schema:
            optional_props = schema["properties"]
            for prop_name in optional_props:
                prop_type = None
                if "type" in optional_props[prop_name]:
                    prop_type = optional_props[prop_name]["type"]
                    if type(prop_type) == str:
                        pass
                    else:
                        prop_type = prop_type[0]
                buffer_msg.add_param(prop_name, prop_type)
            if "required" in schema:
                required_props = schema["required"]
                for prop_name in required_props:
                    buffer_msg.require_param(prop_name)
        print(buffer_msg.compile())
    else:
        for msg in schema["anyOf"]:
            msg_name = msg["required"][0]
            buffer_msg = Message(msg_name, prefix)
            msg_prop = msg["properties"][msg_name]
            if "properties" in msg_prop:
                optional_props = msg_prop["properties"]
                for prop_name in optional_props:
                    prop_type = None
                    if "type" in optional_props[prop_name]:
                        prop_type = optional_props[prop_name]["type"]
                        if type(prop_type) == str:
                            pass
                        else:
                            prop_type = prop_type[0]
                    buffer_msg.add_param(prop_name, prop_type)
                if "required" in msg_prop:
                    required_props = msg_prop["required"]
                    for prop_name in required_props:
                        buffer_msg.require_param(prop_name)
            print(buffer_msg.compile())


def get_json_data(path: str) -> json:
    with open(path) as f:
        raw_data = f.read()
        json_data = json.loads(raw_data)
        return json_data


def main():
    # CHANGE ME
    # vvvvvvvvv
    name = "gov"
    # ^^^^^^^^^
    # CHANGE ME

    input_schema = f"contracts/{name}/schema/instantiate_msg.json"
    json_schema = get_json_data(input_schema)
    process_schema(json_schema, "instantiate")
    input_schema = f"contracts/{name}/schema/execute_msg.json"
    json_schema = get_json_data(input_schema)
    process_schema(json_schema, "execute")
    input_schema = f"contracts/{name}/schema/query_msg.json"
    json_schema = get_json_data(input_schema)
    process_schema(json_schema, "query")


if __name__ == "__main__":
    main()
