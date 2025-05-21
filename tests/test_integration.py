import asdf
import yaml


def test_resource_id(resource_path):
    resource_manager = asdf.get_config().resource_manager

    with resource_path.open("rb") as f:
        resource_content = f.read()
    resource = yaml.safe_load(resource_content)
    resource_uri = resource["id"]
    assert resource_manager[resource_uri] == resource_content


def test_manifest(manifest_path):
    resource_manager = asdf.get_config().resource_manager

    with manifest_path.open("rb") as f:
        manifest_content = f.read()
    manifest = yaml.safe_load(manifest_content)

    manifest_schema = asdf.schema.load_schema("asdf://asdf-format.org/core/schemas/extension_manifest-1.0.0")

    # The manifest must be valid against its own schema:
    asdf.schema.validate(manifest, schema=manifest_schema)

    for tag_definition in manifest["tags"]:
        # The tag's schema must be available:
        assert tag_definition["schema_uri"] in resource_manager

    assert manifest["id"].endswith(manifest_path.stem)
