def test_manifest_tag_order(latest_manifest):
    """Tags should be sorted alphabetically"""
    tag_uris = [tag_def["tag_uri"] for tag_def in latest_manifest["tags"]]
    assert tag_uris == sorted(tag_uris)


def test_tags_match_schemas(latest_manifest):
    """Check that tag and schema versions match"""
    for tag_def in latest_manifest["tags"]:
        tag_uri = tag_def["tag_uri"]
        schema_uri = tag_def["schema_uri"]
        assert tag_uri.split(":")[-1] in schema_uri


def test_uses_latest_schemas(latest_manifest, latest_schema_uris):
    """The latest manifest should always use the latest schemas"""
    for tag_def in latest_manifest["tags"]:
        schema_uri = tag_def["schema_uri"]
        assert schema_uri in latest_schema_uris
