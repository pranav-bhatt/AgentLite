import json
import pprint


def managerParser():
    f = open("dereferenced_full_swagger.json")
    swagger = json.load(f)
    f.close()

    metadata = {}
    for path in swagger["paths"]:
        metadata[path] = {}
        for HTTPMethod in swagger["paths"][path]:
            metadata[path][HTTPMethod] = swagger["paths"][path][HTTPMethod]["summary"]
    json.dump(metadata, open("manager_metadata.json", "w"), indent=4)


def remove_useless_keys(dictionary, useless_keys):
    if isinstance(dictionary, dict):
        for key, value in list(dictionary.items()):
            if key in useless_keys:
                del dictionary[key]
            else:
                remove_useless_keys(value, useless_keys)
    elif isinstance(dictionary, list):
        for item in dictionary:
            remove_useless_keys(item, useless_keys)


def swaggerSplitter():
    f = open("dereferenced_full_swagger.json")
    swagger = json.load(f)
    f.close()

    useless_keys = ["type", "in", "readOnly", "format", "responses"]
    remove_useless_keys(swagger, useless_keys)

    sections = {}
    for k, v in swagger["paths"].items():
        section_name = k.split("/")[3]
        if section_name not in sections:
            sections[section_name] = {k: v}
        else:
            sections[section_name][k] = v

    for k, v in sections.items():
        json.dump(
            v,
            open(f"agent_categorised_json/{k}.json", "w"),
            separators=(",", ":"),
        )


if __name__ == "__main__":
    swaggerSplitter()
