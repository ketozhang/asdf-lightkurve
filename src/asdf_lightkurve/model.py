from typing import Annotated

import astropy.time
import astropy.units as u
from asdf_pydantic import AsdfPydanticModel
from asdf_pydantic.schema import AsdfTag

from asdf_lightkurve import __version__


class AsdfLightCurve(AsdfPydanticModel):
    """ASDF-serializable data model for light curves. Proxies the class
    {class}`lightkurve.LightCurve`
    """

    _tag = f"asdf://asdf-lightkurve/tags/lightcurve-{__version__}"

    time: (
        Annotated[u.Quantity, AsdfTag("tag:stsci.edu:asdf/core/quantity-1.*")]
        | Annotated[astropy.time.Time, AsdfTag("tag:stsci.edu:asdf/core/time-1.*")]
    )
    flux: Annotated[u.Quantity, AsdfTag("tag:stsci.edu:asdf/core/quantity-1.*")]
    flux_err: Annotated[u.Quantity, AsdfTag("tag:stsci.edu:asdf/core/quantity-1.*")]

    # def to_lightkurve(self) -> LightCurve:
    #     raise NotImplementedError()
