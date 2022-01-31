# TerraTools

This repository holds my tools that help me work on CosmWasm and Terra blockchains.

- [terra_sdk_wrapper](terra_sdk_wrapper)): python module that wraps `terra_sdk.py`, and proposes a framework to initialize and interact with contracts. Why ? I like python 🐍
- [schema to class](schema_to_class): it's quite long to write all the classes before starting to work, so I made my job easier with this. Point it to a contract and it will generate all the useful code to build messages.
- [audit/starter](audit/starter.ipynb): a python notebook that uses `terra_sdk_wrapper` and `schema_to_class` generated classes. You can read how to store contract code, instantiate contract, execute and query stuff.
