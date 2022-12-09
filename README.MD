This is a very simple textual app for browsing a folder with deep learning experiments.

# Usage

```
```

The folder is expected to have the following structure:

```
├── experiment1
│   ├── meta.txt
│   ├── log.txt
│   ├── model.padl
│   │   ├── transform.py
│   │   [...]
│   [...]
├── experiment2
│   ├── meta.txt
│   ├── log.txt
│   ├── model.padl
│   │   ├── transform.py
│   │   [...]
│   [...]
[...]
```

where `meta.txt` contains 

```
parent: <name of parent experiment>

<some documentation>
```

The app shows a tree of all experiments with their ancestors. Detail views for the individual
experiments show the documentation text from `meta.txt`, their logs, and a diff wrt to the
parent model.

![screenshot](screenshots/latest.png)


# Installation

```
pip install -r requirements.txt
```

Requires at least python3.10.