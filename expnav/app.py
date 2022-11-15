import sys

from textual.app import App
from textual.widgets import Header, Footer, DataTable, Static
from textual.widget import Widget
from textual.reactive import reactive

from rich import print

from expnav.model import ExperimentCollection, Experiment, _rich_tree_lines


class ExpNav(App):
    CSS_PATH = 'styles.css'
    BINDINGS = (
        ('q', 'quit', 'Quit'),
    )

    selected: reactive[str | None] = reactive(None, layout=True)

    def __init__(self, folder):
        super().__init__()
        self.folder = folder
        self.collection = ExperimentCollection(self.folder)

    def select(self, value):
        self.selected = self.collection.experiments[value]
        print(self.selected)

    def compose(self):
        print(self.folder)
        yield Header(name=self.folder)
        yield Footer()
        yield Overview()

    def action_quit(self):
        self.exit()

    def watch_selected(self, old, value):
        self.refresh(layout=True)
        self.check_idle()
        self.query('Details').remove()
        if value is not None:
            self.mount(Details(self.selected))


class Overview(DataTable):
    def __init__(self):
        super().__init__()
        self.items = []
        self.show_header = False

    def on_click(self, event):
        print(event)

    def on_mount(self):
        self.add_column('experiments', width=50)
        self.add_column('docs')
        tree = _rich_tree_lines(self.app.collection._rich_tree())
        docs = self.app.collection._rich_docs()
        names = self.app.collection.ordered_names()
        for branch, doc, name in zip(tree, docs, names):
            self.add_row(branch, doc)
            self.items.append(name)
        self.focus()
        return self
    
    def watch_cursor_cell(self, old, value):
        super().watch_cursor_cell(old, value)
        self.app.select(self.items[value.row])


class Details(Static):
    def __init__(self, experiment):
        super().__init__()
        self.experiment = experiment

    def compose(self):
        yield Docs(self.experiment.doc, 'docs')
        yield Diff(self.experiment.diff(), 'diff')
        yield Metrics(self.experiment.metrics, 'metrics')


class TextBoxWithHeader(Static):
    def __init__(self, text, title):
        super().__init__()
        self.text = text
        self.title = title

    def compose(self):
        yield TextBox(self.title, classes='title-text')
        yield TextBox(self.text, classes='content-text')


class TextBox(Static):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text

    def render(self):
        return self.text


class Docs(TextBoxWithHeader):
    pass


class Diff(TextBoxWithHeader):
    pass


class Metrics(TextBoxWithHeader):
    pass
