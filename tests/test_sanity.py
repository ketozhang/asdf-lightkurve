import asdf
import pytest
from asdf.extension import Extension
from asdf_pydantic import AsdfPydanticConverter

import asdf_lightkurve
from asdf_lightkurve import AsdfLightCurve


@pytest.fixture()
def asdf_extension():
    converter = AsdfPydanticConverter()
    converter.add_models(AsdfLightCurve)

    class TestExtension(Extension):
        extension_uri = "asdf://asdf-lightkurve/test/extensions/lightkurve-0.0.0"
        converters = [converter]
        tags = [*converter.tags]

    asdf.get_config().add_extension(TestExtension())


def test_sanity(asdf_extension):
    assert asdf_lightkurve
    assert str(AsdfLightCurve._tag).startswith("asdf://")


def test_write(asdf_extension, tmp_path):
    lc = AsdfLightCurve()
    af = asdf.AsdfFile({"data": lc})
    af.write_to(tmp_path / "lightcurve.asdf")

    with asdf.open(tmp_path / "lightcurve.asdf") as af2:
        assert isinstance(af2["data"], AsdfLightCurve)
        assert af2["data"]._tag == lc._tag
