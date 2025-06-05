import re

import asdf
import pytest

ALLOWED_REFS = (
    r"^http://stsci.edu/schemas/asdf/transform/transform-[0-9.]+$",
    r"^http://astropy.org/schemas/astropy/coordinates/frames/baseframe-[0-9.]+$",
    r"^frame-[0-9.]+$",
    r"^http://stsci.edu/schemas/asdf/transform/zenithal-[0-9.]+$",
    r"^http://stsci.edu/schemas/asdf/transform/conic-[0-9.]+$",
    r"^http://stsci.edu/schemas/asdf/transform/quadcube-[0-9.]+$",
    r"^http://stsci.edu/schemas/asdf/transform/pseudoconic-[0-9.]+$",
    r"^http://stsci.edu/schemas/asdf/transform/pseudocylindrical-[0-9.]+$",
    r"^http://stsci.edu/schemas/asdf/transform/cylindrical-[0-9.]+$",
    r"^#.*$",
)

UNIT_TAGS = {"tag:stsci.edu:asdf/unit/unit-1.*", "tag:astropy.org:astropy/units/unit-1.*"}


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


@pytest.mark.parametrize("tag_set", (UNIT_TAGS,))
def test_tags_in_allof(latest_schema, tag_set):
    """
    Test that some tags (unit) where the
    tag used depends on the value are always referenced in an
    allof containing all tags.
    """
    # we walk_and_modify here to use postorder

    def callback(node):
        if not isinstance(node, dict):
            return node
        if "anyOf" in node:
            # check if this anyof includes a tag in the set
            seen = set()
            for sub in node["anyOf"]:
                if not isinstance(sub, dict):
                    continue
                if "tag" not in sub:
                    continue
                if sub["tag"] in tag_set:
                    seen.add(sub["tag"])

            if seen:
                # if a tag was found, check both were found
                assert seen == tag_set, f"anyOf {node} missing: {tag_set - seen}"
                # remove the anyof so the code below can check for tags not in the anyof
                return {k: v for k, v in node.items() if k != "anyOf"}
        if tag := node.get("tag"):
            assert tag not in tag_set, f"tag {tag} must be in an anyOf with: {tag_set}"
        return node

    asdf.treeutil.walk_and_modify(latest_schema, callback, postorder=False)
