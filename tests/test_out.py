import os
import re

import pytest

from helpers import cmd


def test_out(tmpdir):
    """Test packing image from template."""

    params = {
        'template_path': 'src/ami.json',
    }

    output = cmd('out', {}, [str(tmpdir)], params=params)

    assert output.get('version').get('ImageId') == 'ami-01234567'
    assert output.get('metadata')[0].get('name') == 'tag_version'

def test_output(tmpdir, capfd):
    """Test output to stderr."""

    params = {
        'template_path': 'src/ami.json',
    }

    # disable test debug logging to get normal output
    del os.environ['RESOURCE_DEBUG']
    cmd('out', {}, [str(tmpdir)], params=params)
    os.environ['RESOURCE_DEBUG'] = 'true'

    out, err = capfd.readouterr()
    print(err)
    assert re.search('^amazon-ebs output will be in this color\.$', err, re.MULTILINE)
    assert '==> amazon-ebs: Force Deregister flag found, skipping prevalidating AMI Name' in err

def test_fail(tmpdir):
    """Test packer error is passed."""

    params = {
        'template_path': 'src/non-existing.json',
    }

    with pytest.raises(Exception):
        cmd('out', {}, [str(tmpdir)], params=params)

def test_passing_build_vars(tmpdir):
    """Test is build vars are passed."""

    params = {
        'template_path': 'src/build-vars.json',
        'build_vars': {
            'role': 'test',
        }
    }

    assert cmd('out', {}, [str(tmpdir)], params=params)

def test_passing_build_vars_from_files(tmpdir):
    """Test is build vars can be read from files."""

    tmpdir.join('ami_id').write('ami-12345678')

    params = {
        'template_path': 'src/build-vars-from-file.json',
        'build_vars_from_file': {
            'source_ami': 'ami_id',
        }
    }

    assert cmd('out', {}, [str(tmpdir)], params=params)
