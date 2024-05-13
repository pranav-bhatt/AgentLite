import json
import pprint


def remove_unecessary_keys(dictionary, useless_keys):
    if isinstance(dictionary, dict):
        for key, value in list(dictionary.items()):
            if key in useless_keys:
                del dictionary[key]
            else:
                remove_unecessary_keys(value, useless_keys)
    elif isinstance(dictionary, list):
        for item in dictionary:
            remove_unecessary_keys(item, useless_keys)


def swaggerSplitter(threshold=2):
    f = open("dereferenced_full_swagger.json")
    swagger = json.load(f)
    f.close()

    useless_keys = [
        "type",
        "in",
        "readOnly",
        "format",
        "responses",
        "operationId",
        "tags",
    ]
    remove_unecessary_keys(swagger, useless_keys)

    metadata = {}
    buckets = {}
    for path, methods in swagger["paths"].items():
        path_parts = path.split("/")
        bucket_name = (
            "_".join(path_parts[3 : 3 + threshold])
            if len(path_parts) > 3
            else path_parts[3]
        )
        while bucket_name in buckets and len(buckets[bucket_name]) >= threshold:
            threshold += 1
            bucket_name = (
                "_".join(path_parts[3 : 3 + threshold])
                if len(path_parts) > 3
                else path_parts[3]
            )

        if bucket_name not in buckets:
            buckets[bucket_name] = {}

        buckets[bucket_name][path] = methods

    for bucket_name, paths in buckets.items():
        # set the initial data for manager metadata along with where the files are being stored
        for path in paths:
            metadata[path] = {}
            metadata[path]["methods"] = {}
            metadata[path]["file"] = f"{bucket_name}.json"

            for method in paths[path]:
                metadata[path]["methods"][method] = paths[path][method]["summary"]

        # populate the individual json files with api information
        json.dump(
            paths,
            open(f"agent_categorised_json/{bucket_name}.json", "w"),
            separators=(",", ":"),
        )
    json.dump(metadata, open("manager_metadata.json", "w"), indent=4)


if __name__ == "__main__":
    swaggerSplitter()
