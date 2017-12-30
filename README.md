This is a solver for the iOS puzzle game [Picture Cross](https://itunes.apple.com/us/app/picture-cross/id977150768?mt=8).

# Installation

Requirements: Python 3

```bash
$ git clone git@github.com:wabain/picture-cross-solver.git
$ pip install -r requirements.txt
```

# Usage

The solver takes a JSON file as input. See the included files for the input format.

```bash
$ time python solver.py ./demo.json
✗ ▓ ▓ ▓ ▓ ▓ ▓ ▓
▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓
✗ ▓ ▓ ✗ ✗ ▓ ▓ ✗
✗ ▓ ▓ ✗ ✗ ▓ ▓ ✗
✗ ▓ ▓ ✗ ✗ ▓ ▓ ✗
✗ ▓ ▓ ✗ ✗ ▓ ▓ ✗
✗ ▓ ▓ ✗ ✗ ✗ ▓ ▓
✗ ✗ ▓ ▓ ✗ ✗ ▓ ▓
python solver.py ./demo.json  0.07s user 0.01s system 90% cpu 0.086 total
```
