# credits to smitmartijn - discord-table-builder - https://github.com/smitmartijn/discord-table-builder.git
# convert php to python with chatgpt

class DiscordEmbedTable:
    def __init__(self, options: dict):
        # Required titles
        if "titles" not in options:
            raise Exception("Titles/headers are required")

        self.titles = options["titles"]
        self.start = options.get("start", "`")
        self.end = options.get("end", "`")
        self.padding = options.get("padding", 0)
        self.white_space = options.get("whiteSpace", False)

        self.rows = []

        # Initialize column widths based on titles
        self.column_widths = [len(title) for title in self.titles]

    def add_row(self, columns: list, options: dict | None = None):
        if options is None:
            options = {}

        row_data = {
            "columns": columns,
            "url": options.get("url")
        }

        self.rows.append(row_data)

        # Update column widths
        self.update_column_widths(columns)

        return self

    def update_column_widths(self, columns: list):
        """Update column widths based on row content."""
        for i, column in enumerate(columns):
            if i >= len(self.column_widths):
                self.column_widths.append(len(column))
            else:
                self.column_widths[i] = max(self.column_widths[i], len(column))

    def render_row(self, row_data: dict) -> str:
        """Render a single table row."""
        row_string = self.start

        for i, column in enumerate(row_data["columns"]):
            padding_char = "\u200B" if self.white_space else " "
            width = self.column_widths[i] + self.padding
            row_string += column.ljust(width, padding_char)

        row_string = row_string.rstrip() + self.end

        if row_data.get("url"):
            row_string = f"[{row_string}]({row_data['url']})"

        return row_string

    def render_title_row(self) -> str:
        """Render the header row."""
        title_string = self.start

        for i, title in enumerate(self.titles):
            padding_char = "\u200B" if self.white_space else " "
            width = self.column_widths[i] + self.padding
            title_string += title.ljust(width, padding_char)

        return title_string.rstrip() + self.end

    def to_field(self, options: dict | None = None) -> dict:
        if options is None:
            options = {}

        title_row = self.render_title_row()
        rows = [self.render_row(row) for row in self.rows]

        field = {
            "name": title_row,
            "value": "\n".join(rows),
            "inline": options.get("inline", False)
        }

        if not options.get("keepRows", False):
            self.clear()

        return field

    def to_string(self, options: dict | None = None) -> str:
        if options is None:
            options = {}

        title_row = self.render_title_row()
        rows = [self.render_row(row) for row in self.rows]

        result = title_row + "\n" + "\n".join(rows)

        if not options.get("keepRows", False):
            self.clear()

        return result

    def has_rows(self) -> bool:
        return len(self.rows) > 0

    def clear(self):
        self.rows = []
