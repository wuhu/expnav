import json
from pathlib import Path

from rich.tree import Tree
from rich.text import Text
from rich.table import Table
from rich.segment import Segments
from rich import print, get_console

from .diff import rich_diff


class ExperimentCollection:
    def __init__(self, folder):
        self.folder = Path(folder)
        self.experiments = {}
        self.refresh()

    def refresh(self):
        self.experiments = {}
        for experiment in self.folder.glob('*'):
            if experiment.is_dir():
                self.experiments[experiment.name] = Experiment.read(self.folder / experiment, self)

    def __rich__(self):
        table = Table()
        table.add_column('experiments', overflow='ellipsis', no_wrap=True)
        table.add_column('docs', overflow='ellipsis', no_wrap=True)
        for experiment, doc in zip(_rich_tree_lines(self._rich_tree()), self._rich_docs()):
            table.add_row(experiment, doc)
        return table

    def _tree(self):
        tree = {}
        nodes = {}
        for experiment in self.experiments.values():
            self._sub_tree(experiment, nodes, tree)
        return tree
    
    def ordered_names(self):
        return depth_first(self._tree())

    def _sub_tree(self, experiment, nodes, root):
        if experiment is None:
            return root
        if experiment.name in nodes:
            return nodes[experiment.name]
        tree = {}
        self._sub_tree(experiment.parent, nodes, root)[f'{experiment.name}'] = tree
        nodes[experiment.name] = tree
        return tree

    def _rich_tree(self):
        tree = Tree(f'{self.folder.name}')
        tree.hide_root = True
        nodes = {None: tree}
        for experiment_name in self.ordered_names():
            nodes[experiment_name] = (
                nodes[self.experiments[experiment_name].parent_name].add(experiment_name)
            )
        return tree

    def _rich_docs(self):
        docs = []
        for experiment_name in depth_first(self._tree()):
            docs.append(self.experiments[experiment_name].doc.replace('\n', ' '))
        return docs

def depth_first(tree):
    for node, children in tree.items():
        yield node
        if children:
            yield from depth_first(children)


def _rich_tree_lines(tree):
    console = get_console()
    lines = []
    current = []
    for segment in tree.__rich_console__(console, console.options):
        if segment.text == '\n':
            lines.append(Segments(current))
            current = []
            continue
        current.append(segment)
    return lines


def parse_meta(string):
    '''Parse a meta string formatted like this:

        parent: ...

        [... doc ...]

    and return a dict {'parent': ..., 'doc': ...}
    '''
    string = string.strip()
    parent_line, doc_lines = string.split('\n', 1)
    parent = parent_line.split('parent:')[1].strip()
    doc = doc_lines.strip()
    return {
        'parent': parent or None,
        'doc': doc
    }


def parse_metrics(string):
    return string


class Experiment:
    def __init__(self, name, doc, parent_name, metrics, collection):
        self.name = name
        self.doc = doc
        self.parent_name = parent_name
        self.metrics = metrics
        self.collection = collection

    @property
    def parent(self):
        if self.parent_name is None:
            return None
        return self.collection.experiments[self.parent_name]

    @classmethod
    def read(self, folder, collection):
        name = folder.name

        with open(folder / 'meta.txt') as f:
            meta = parse_meta(f.read())

        parent = meta['parent']
        doc = meta['doc']

        with open(folder / 'log.txt') as f:
            metrics = parse_metrics(f.read())

        return Experiment(name, doc, parent, metrics, collection)

    @property
    def code(self):
        with open(self.collection.folder / self.name / 'model.padl' / 'transform.py') as f:
            return f.read()

    def diff(self):
        if self.parent is None:
            return ''
        return rich_diff(self.parent.code, self.code)
