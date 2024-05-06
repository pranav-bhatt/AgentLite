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


def swaggerSplitter():
    f = open("dereferenced_full_swagger.json")
    swagger = json.load(f)
    f.close()

    sections = {}
    for k, v in swagger["paths"].items():
        section_name = k.split("/")[3]
        if section_name not in sections:
            sections[section_name] = {k: v}
        else:
            sections[section_name][k] = v

    for k, v in sections.items():
        json.dump(v, open(f"agent_categorised_json/{k}.json", "w"), indent=4)


if __name__ == "__main__":
    swaggerSplitter()
