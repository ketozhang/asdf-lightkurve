import asdf
import asdf.schema
import astropy.units as u
import numpy as np
import pytest
import yaml
from asdf.extension import Extension
from asdf_pydantic import AsdfPydanticConverter
from lightkurve import LightCurve

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

    with asdf.config_context() as asdf_config:
        asdf_config.add_resource_mapping(
            {
                yaml.safe_load(AsdfLightCurve.model_asdf_schema())[
                    "id"
                ]: AsdfLightCurve.model_asdf_schema()
            }
        )
        print(AsdfLightCurve.model_asdf_schema())
        asdf_config.add_extension(TestExtension())
        yield asdf_config


def test_sanity(asdf_extension):
    assert asdf_lightkurve
    assert str(AsdfLightCurve._tag).startswith("asdf://")


@pytest.mark.usefixtures("asdf_extension")
def test_write(tmp_path):
    lc = AsdfLightCurve(
        time=np.array([1]) * u.s,
        flux=np.array([1]) * u.Jy,
        flux_err=np.array([0.1]) * u.Jy,
    )
    af = asdf.AsdfFile({"data": lc})
    af.write_to(tmp_path / "lightcurve.asdf")

    with asdf.open(tmp_path / "lightcurve.asdf") as af2:
        assert isinstance(af2["data"], AsdfLightCurve)
        assert af2["data"]._tag == lc._tag


@pytest.mark.xfail(
    run=False,
    reason=(
        "Although LightCurve is a subtype of astropy Table, "
        "ASDF does not recognize it as compatible with Table."
    ),
)
def test_lightkurve_as_is(tmp_path):
    lc = LightCurve(time=[1], flux=[1], flux_err=[1])
    af = asdf.AsdfFile({"data": lc})
    af.write_to(tmp_path / "lightcurve.asdf")

    with asdf.open(tmp_path / "lightcurve.asdf") as af2:
        assert isinstance(af2["data"], AsdfLightCurve)
        assert af2["data"]._tag == lc._tag


@pytest.mark.usefixtures("asdf_extension")
def test_schema(tmp_path):
    """tests the model schema is correct."""

    schema = yaml.safe_load(AsdfLightCurve.model_asdf_schema())
    with open(tmp_path / str(AsdfLightCurve._tag).split("/")[-1], "wt") as f:
        yaml.dump(schema, f)

    asdf.schema.check_schema(schema)
