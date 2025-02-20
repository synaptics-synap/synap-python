import pytest
from synap.types import (
    Dim2d,
    DataType,
    Landmark,
    Layout,
    Mask,
    Rect,
    Shape
)


def test_dim2d_basic():
    """Test Dim2d class"""
    # Default constructor
    d = Dim2d()
    assert d.x == 0
    assert d.y == 0

    # Parametrized constructor
    d2 = Dim2d(5, 10)
    assert d2.x == 5
    assert d2.y == 10

    # Addition
    d3 = d2 + Dim2d(1, 2)
    assert d3.x == 6
    assert d3.y == 12

    # In-place addition
    d2 += Dim2d(10, 1)
    assert d2.x == 15
    assert d2.y == 11

    # Equality
    assert Dim2d(1, 2) == Dim2d(1, 2)
    assert Dim2d(1, 2) != Dim2d(2, 2)

    # __repr__
    assert repr(Dim2d(3, 4)) == "Dim2d(x=3, y=4)"


def test_data_type_enum():
    """Test DataType enum"""
    assert DataType.invalid.name == "invalid"
    assert DataType.byte.name == "byte"
    assert DataType.int8.name == "int8"
    assert DataType.uint8.name == "uint8"
    assert DataType.int16.name == "int16"
    assert DataType.uint16.name == "uint16"
    assert DataType.int32.name == "int32"
    assert DataType.uint32.name == "uint32"
    assert DataType.float16.name == "float16"
    assert DataType.float32.name == "float32"

    assert DataType.byte.np_type().name == "uint8"
    assert DataType.int8.np_type().name == "int8"
    assert DataType.uint8.np_type().name == "uint8"
    assert DataType.int16.np_type().name == "int16"
    assert DataType.uint16.np_type().name == "uint16"
    assert DataType.int32.np_type().name == "int32"
    assert DataType.uint32.np_type().name == "uint32"
    assert DataType.float16.np_type().name == "float16"
    assert DataType.float32.np_type().name == "float32"

    with pytest.raises(ValueError):
        DataType.invalid.np_type()


def test_landmark():
    """Test Landmark class"""
    # Default constructor
    lm = Landmark()
    assert lm.x == 0
    assert lm.y == 0
    assert lm.z == 0
    assert lm.visibility == -1.0

    # Parametrized constructor
    lm2 = Landmark(10, 20, 30, 0.5)
    assert lm2.x == 10
    assert lm2.y == 20
    assert lm2.z == 30
    assert lm2.visibility == 0.5

    # Equality
    assert lm != lm2
    lm3 = Landmark(10, 20, 30, 1.0)
    # visibility isn't checked for equality
    assert lm2 == lm3

    # __repr__
    rep = repr(lm2)
    assert rep == "Landmark(x=10, y=20, z=30, visibility=0.5)"


def test_layout_enum():
    """Test Layout enum"""
    assert Layout.none.value == 0
    assert Layout.nchw.value == 1
    assert Layout.nhwc.value == 2
    assert Layout.none.name == "none"


def test_mask_basic():
    """Test Mask class"""
    # Constructor
    m = Mask(5, 3)
    assert m.width == 5
    assert m.height == 3

    # Check .buffer()
    m.set_value(row=0, col=0, val=1.0)
    m.set_value(row=1, col=2, val=9.5)
    buf = m.buffer()
    assert len(buf) == 15
    assert buf[0] == pytest.approx(1.0)
    assert buf[7] == pytest.approx(9.5)

    # __bool__
    assert m
    m_empty = Mask(0, 0)
    assert not m_empty

    # __repr__
    assert repr(m) == "Mask(width=5, height=3)"


def test_rect_basic():
    """Test Rect class"""
    # Default constructor (empty rect)
    r = Rect()
    assert r.origin.x == 0
    assert r.origin.y == 0
    assert r.size.x == 0
    assert r.size.y == 0
    assert r.empty()

    # Parametrized constructor
    r2 = Rect(Dim2d(2, 3), Dim2d(4, 5))
    assert r2.origin.x == 2
    assert r2.origin.y == 3
    assert r2.size.x == 4
    assert r2.size.y == 5
    assert not r2.empty()

    # Equality
    assert r != r2
    r3 = Rect((2,3), (4,5))
    assert r2 == r3

    # __repr__
    rep = repr(r3)
    assert rep == "Rect(origin=(2, 3), size=(4, 5))"


def test_shape_basic():
    """Test Shape class"""
    s = Shape([1, 3, 224, 224])
    # __getitem__
    assert s[0] == 1
    assert s[3] == 224
    # out-of-range
    with pytest.raises(IndexError):
        s[4]

    # __iter__
    dims = list(s)
    assert dims == [1, 3, 224, 224]

    # item_count => 1*3*224*224
    assert s.item_count() == 3 * 224 * 224

    # valid => check if all dims > 0
    assert s.valid()

    s2 = Shape([1, 3, 224, 224])
    assert s == s2

    # __repr__
    rep = repr(s)
    assert rep == "Shape(1, 3, 224, 224)"


@pytest.mark.parametrize("shape_data", [
    [1, 2, 3],
    [10, 10],
    [1, 224, 224, 3],
])
def test_shape_parametrized(shape_data):
    """Test multiple shapes"""
    s = Shape(shape_data)
    assert list(s) == shape_data


def test_data_type_error_handling():
    """Check that invalid DataType usage raises an error"""
    with pytest.raises(ValueError):
        DataType.invalid.np_type()


def test_mask_invalid_index():
    """Test that out-of-bounds row/col raise in set_value or buffer usage"""
    m = Mask(3, 3)
    with pytest.raises(IndexError):
        m.set_value(10, 0, 1.0)
