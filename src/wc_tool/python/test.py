import os, subprocess

# Set the current working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def test_step_one():
    result = subprocess.run(
        ["python", "main.py", "-c", "test.txt"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "342190 test.txt"

def test_step_two():
    result = subprocess.run(
        ["python", "main.py", "-l", "test.txt"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "7145 test.txt"

def test_step_three():
    result = subprocess.run(
        ["python", "main.py", "-w", "test.txt"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "58164 test.txt"

def test_step_four():
    result = subprocess.run(
        ["python", "main.py", "-m", "test.txt"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "339292 test.txt"

def test_step_five():
    result = subprocess.run(
        ["python", "main.py", "test.txt"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "7145 58164 342190 test.txt"

def test_step_six():
    result = subprocess.run(
        ["cat", "test.txt", "|", "python", "main.py", "-l"],
        capture_output=True,
        text=True,
        shell=True # shell to allow pipe...
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "7145"