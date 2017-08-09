def test_vinisto_is_callable():
    import subprocess

    subprocess.check_call(['vinisto', '--help'])


def test_vinisto_is_importable():
    import vinisto
