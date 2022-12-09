import difflib


def format_row(row):
    """Color the + / - rows in the diff. """
    if row.startswith('+'):
        return f'[bold green]{row}[/bold green]'
    if row.startswith('-'):
        return f'[red]{row}[/red]'
    return row


def format_diff(diff):
    """Format a diff as gotten from difflib.unified_diff. """
    return ''.join(format_row(row) for row in diff)


def rich_diff(a, b):
    return format_diff(difflib.unified_diff(a.splitlines(keepends=True),
                                            b.splitlines(keepends=True)))
