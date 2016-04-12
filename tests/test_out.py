import pytest

from helpers import cmd


def test_out(tmpdir):
    """Test packing image from template."""

    params = {
        'template_path': 'src/ami.json',
    }

    output = cmd('out', {}, [str(tmpdir)], params=params)

    assert output.get('version').get('ImageId') == 'ami-01234567'

def test_fail(tmpdir):
    """Test packer error is passed."""

    params = {
        'template_path': 'src/non-existing.json',
    }

    with pytest.raises(Exception):
        cmd('out', {}, [str(tmpdir)], params=params)
