from asdf_pydantic import AsdfPydanticModel

from asdf_lightkurve import __version__


class AsdfLightCurve(AsdfPydanticModel):
    """ASDF-serializable data model for light curves. Proxies the class
    {class}`lightkurve.LightCurve`
    """

    _tag = f"asdf://asdf-lightkurve/tags/lightcurve-{__version__}"
