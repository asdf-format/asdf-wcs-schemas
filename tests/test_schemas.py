import re

import asdf

ALLOWED_REFS = (
    r"^http://stsci.edu/schemas/asdf/transform/transform-[0-9.]+$",
    r"^http://astropy.org/schemas/astropy/coordinates/frames/baseframe-[0-9.]+$",
    r"^frame-[0-9.]+$",
    r"^#.*$",
)


def test_only_known_refs(latest_schema):
    """Latest schemas should only contain specific refs"""
    for node in asdf.treeutil.iter_tree(latest_schema):
        if not isinstance(node, dict):
            continue
        if "$ref" in node:
            uri = node["$ref"]
            if not any(re.match(pattern, uri) for pattern in ALLOWED_REFS):
                assert False, f"Unexpected $ref: {uri}"


def test_wildcard_tags(latest_schema):
    """Latest schemas should only contain wildcarded tags"""
    for node in asdf.treeutil.iter_tree(latest_schema):
        if not isinstance(node, dict):
            continue
        if "tag" in node:
            pattern = node["tag"]
            if "*" not in pattern:
                assert False, f"tag pattern missing wildcard: {pattern}"


def test_required_properties(schema):
    assert schema["$schema"] == "http://stsci.edu/schemas/yaml-schema/draft-01"
    assert "id" in schema
    assert "title" in schema


def test_required(schema):
    def callback(node):
        if isinstance(node, dict) and "required" in node:
            assert node.get("type") in ["object", "string", None]
            property_names = set(node.get("properties", {}).keys())
            required_names = set(node["required"])
            if not required_names.issubset(property_names):
                missing_list = ", ".join(required_names - property_names)
                message = "required references names that do not exist: " + missing_list
                assert False, message

    asdf.treeutil.walk(schema, callback)
