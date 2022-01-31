from typing import Dict, List, Set


class ParamHolder():
    name: str
    required: bool
    type_instance: str

    def __init__(self, name: str, type_instance: str, required: bool = True) -> None:
        self.name = name
        self.type_instance = type_instance
        self.required = required

    def as_arg(self):
        res = self.name
        if self.type_instance:
            res += f": {self.type_instance}"
        if not self.required:
            res += " = None"
        return res

    def as_msg(self):
        res = f"'{self.name}': {self.name}"
        return res


class FunctionHolder():
    prefix: str
    name: str
    params: List[ParamHolder]
    short_version = False

    def __init__(self, name, prefix: str = None, short_version: bool = False) -> None:
        self.name = name
        self.prefix = prefix
        self.params = []
        self.short_version = short_version

    def add_param(self, param: ParamHolder):
        self.params.append(param)

    def build_args(self):
        sorted_params = sorted(self.params, key=lambda p: not p.required)
        args = ", ".join([p.as_arg() for p in sorted_params])
        return args

    def build_body(self):
        body = '\treturn {'
        body += f"'{self.name}': "
        body += "{"
        body += ", ".join([p.as_msg() for p in self.params])
        body += '}}'
        return body

    def build_short_body(self):
        body = '\treturn {'
        body += ", ".join([p.as_msg() for p in self.params])
        body += '}'
        return body

    def build_lines(self) -> List[str]:
        lines = []
        # first line is `def fun(arg: type = Default, arg2...):``
        headline = "def "
        if self.prefix:
            headline += self.prefix
            headline += "_"
        headline += self.name
        headline += f'({self.build_args()}):'
        lines.append(headline)

        if self.short_version:
            lines.append(self.build_body())
        else:
            lines.append(self.build_short_body())
        return lines


class ClassHolder():
    name: str
    functions: List[FunctionHolder]

    def __init__(self, name) -> None:
        self.name = name
        self.functions = []

    def add_function(self, func: FunctionHolder):
        self.functions.append(func)

    def build_lines(self):
        lines = []
        lines.append(f"class {self.name}():")
        for func in self.functions:
            lines.append("")
            func_lines = func.build_lines()
            for func_line in func_lines:
                lines.append("\t" + func_line)
        return lines


def test_param():
    p = ParamHolder("amount", "int", False)
    expected = "amount: int = None"
    assert(p.as_arg() == expected)

    p = ParamHolder("amount", "int", True)
    expected = "amount: int"
    assert(p.as_arg() == expected)

    p = ParamHolder("amount", None, True)
    expected = "amount"
    assert(p.as_arg() == expected)

    p = ParamHolder("amount", None, False)
    expected = "amount = None"
    assert(p.as_arg() == expected)

    print("[+] Test param passed")


def test_function():
    f = FunctionHolder("InstantiateMsg")
    f.add_param(ParamHolder("anchor_token", "str"))
    f.add_param(ParamHolder("genesis_time", "int"))
    f.add_param(ParamHolder("owner", "str"))
    expected = []
    expected.append(
        "def InstantiateMsg(anchor_token: str, genesis_time: int, owner: str):")
    expected.append(
        "\treturn {'anchor_token': anchor_token, 'genesis_time': genesis_time, 'owner': owner}")
    assert(f.build_lines() == expected)

    print("[+] Test function passed")


def test_class():
    expected = ["class Airdrop():"]
    expected.append("")
    expected.append(
        "\tdef InstantiateMsg(anchor_token: str, genesis_time: int, owner: str):")
    expected.append(
        "\t\treturn {'anchor_token': anchor_token, 'genesis_time': genesis_time, 'owner': owner}")
    expected.append("")
    expected.append(
        "\tdef InstantiateMsg(anchor_token: str, genesis_time: int, owner: str):")
    expected.append(
        "\t\treturn {'anchor_token': anchor_token, 'genesis_time': genesis_time, 'owner': owner}")

    c = ClassHolder("Airdrop")
    f = FunctionHolder("InstantiateMsg")
    f.add_param(ParamHolder("anchor_token", "str"))
    f.add_param(ParamHolder("genesis_time", "int"))
    f.add_param(ParamHolder("owner", "str"))
    c.add_function(f)
    c.add_function(f)
    lines = c.build_lines()

    # print("\n".join(lines))
    assert(lines == expected)

    print("[+] Test class passed")


if __name__ == "__main__":
    test_param()
    test_function()
    test_class()
