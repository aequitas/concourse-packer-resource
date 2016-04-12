from helpers import cmd


def test_out(tmpdir):
    """Test packing image from template."""

    source = {
        'template_path': 'src/ami.json',
    }

    output = cmd('out', source, [str(tmpdir)])

    assert output.get('version').get('ImageId') == 'ami-01234567'
