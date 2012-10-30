# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import pytest

from .utils import load_psd, decode_psd

from psd_tools import PSDImage
from psd_tools.decoder.image_resources import ResolutionInfo
from psd_tools.constants import DisplayResolutionUnit, DimensionUnit, ImageResourceID

DIMENSIONS = (
    ('1layer.psd',              (101, 55)),
    ('2layers.psd',             (101, 55)),
    ('32bit.psd',               (100, 150)),
    ('300dpi.psd',              (100, 150)),
    ('clipping-mask.psd',       (360, 200)),
    ('gradient fill.psd',       (100, 150)),
    ('group.psd',               (100, 200)),
    ('hidden-groups.psd',       (100, 200)),
    ('hidden-layer.psd',        (100, 150)),
    ('history.psd',             (100, 150)),
    ('mask.psd',                (100, 150)),
    ('note.psd',                (300, 300)),
    ('pen-text.psd',            (300, 300)),
    ('smart-object-slice.psd',  (100, 100)),
    ('transparentbg.psd',       (100, 150)),
    ('vector mask.psd',         (100, 150)),
)

RESOLUTIONS = (
    ('1layer.psd', ResolutionInfo(
        h_res=72.0, h_res_unit=DisplayResolutionUnit.PIXELS_PER_INCH,
        v_res=72.0, v_res_unit=DisplayResolutionUnit.PIXELS_PER_INCH,
        width_unit=DimensionUnit.INCH, height_unit=DimensionUnit.INCH)),
    ('group.psd', ResolutionInfo(
        h_res=72.0, h_res_unit=DisplayResolutionUnit.PIXELS_PER_INCH,
        v_res=72.0, v_res_unit=DisplayResolutionUnit.PIXELS_PER_INCH,
        width_unit=DimensionUnit.CM, height_unit=DimensionUnit.CM)),
)


@pytest.mark.parametrize(("filename", "size"), DIMENSIONS)
def test_dimensions(filename, size):
    w, h = size
    psd = load_psd(filename)
    assert psd.header.width == w
    assert psd.header.height == h


@pytest.mark.parametrize(("filename", "resolution"), RESOLUTIONS)
def test_resolution(filename, resolution):
    psd = decode_psd(filename)
    psd_res = dict((block.resource_id, block.data) for block in psd.image_resource_blocks)
    assert psd_res[ImageResourceID.RESOLUTION_INFO] == resolution

@pytest.mark.parametrize(("filename", "size"), DIMENSIONS)
def test_dimensions_api(filename, size):
    psd = PSDImage(decode_psd(filename))
    assert psd.header.width == size[0]
    assert psd.header.height == size[1]
