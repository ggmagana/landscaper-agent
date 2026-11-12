import io

import pytest
from PIL import Image


@pytest.fixture
def pricing():
    from landscaper.calculator import load_pricing
    return load_pricing()


@pytest.fixture
def conn():
    from landscaper import db
    c = db.connect()
    db.add_business(c, "Acme Lawns", "secret-A", "+15550000001", "tok-A")
    db.add_business(c, "Other Co", "secret-B", "+15550000002", "tok-B")
    return c


def make_jpeg(size=(40, 30), exif=False):
    im = Image.new("RGB", size, (30, 140, 40))
    out = io.BytesIO()
    if exif:
        ex = Image.Exif()
        ex[0x010F] = "SecretCamera"
        im.save(out, format="JPEG", exif=ex)
    else:
        im.save(out, format="JPEG")
    return out.getvalue()
