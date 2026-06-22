import flet as ft
import pandas as pd

# Color palette
PAGE_BG = ft.Colors.BLUE_GREY_200       # outer frame
CARD_BG = ft.Colors.BLUE_GREY_50        # card shell — same as chrome, seamless
CHROME_BG = ft.Colors.BLUE_GREY_50      # sidebar + header (very light grey)
CONTENT_BG = ft.Colors.BLUE_GREY_100    # main content area (greyish)
BORDER = ft.Colors.BLUE_GREY_200


def create_sidebar():
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    height=40,
                    width=40,
                    bgcolor=ft.Colors.GREY_800,
                    # padding=ft.padding.all(2),
                    border_radius=20,
                    alignment=ft.alignment.center,
                    content=ft.Icon(
                        ft.Icons.MENU, 
                        color=ft.Colors.WHITE,
                        size=20,
                    ),
                    on_click=lambda e: print("Menu clicked"),
                ),
           
                ft.Container(height=10),
                ft.IconButton(
                    icon=ft.Icons.EMAIL_OUTLINED,
                    icon_color=ft.Colors.BLUE_700,
                    selected=True,
                ),
                ft.IconButton(icon=ft.Icons.ASSIGNMENT_OUTLINED, icon_color=ft.Colors.GREY_600),
                ft.IconButton(icon=ft.Icons.CHAT_BUBBLE_OUTLINE, icon_color=ft.Colors.GREY_600),
                ft.IconButton(icon=ft.Icons.SEARCH, icon_color=ft.Colors.GREY_600),
                ft.IconButton(icon=ft.Icons.DESCRIPTION_OUTLINED, icon_color=ft.Colors.GREY_600),
                ft.IconButton(icon=ft.Icons.PHONE_ANDROID_OUTLINED, icon_color=ft.Colors.GREY_600),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
        width=70,
        bgcolor=CHROME_BG,
        padding=ft.padding.only(top=20),
        # border=ft.border.only(right=ft.BorderSide(1, BORDER)),
    )


def create_header():
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.BLUE_800,
                            padding=15,
                            border_radius=ft.border_radius.only(top_left=10),
                        ),
                        ft.TextButton("Календарь событий", icon=ft.Icons.CALENDAR_TODAY_OUTLINED),
                        ft.TextButton("Работа с клиентом", icon=ft.Icons.HANDSHAKE_OUTLINED),
                        ft.TextButton("Справочник", icon=ft.Icons.BOOK_OUTLINED),
                    ],
                    spacing=10,
                ),
                ft.Row(
                    controls=[
                        ft.Text(
                            "12:20\n08.09.2026",
                            size=11,
                            color=ft.Colors.GREY_600,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Chip(label=ft.Text("12% План"), bgcolor=ft.Colors.WHITE),
                        ft.Chip(label=ft.Text("50 Задач"), bgcolor=ft.Colors.WHITE),
                        ft.Chip(label=ft.Text("22 Заявок"), bgcolor=ft.Colors.WHITE),
                        ft.IconButton(icon=ft.Icons.NOTIFICATIONS_OUTLINED),
                        ft.CircleAvatar(content=ft.Text("M"), radius=16),
                    ],
                    spacing=15,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        height=65,
        bgcolor=CHROME_BG,
        padding=ft.padding.only(left=10, right=10, top=10, bottom=10),
        # border=ft.border.only(bottom=ft.BorderSide(1, BORDER)),
    )


def load_dataframe(path: str) -> pd.DataFrame:
    lower = path.lower()
    if lower.endswith(".csv"):
        return pd.read_csv(path)
    if lower.endswith((".xlsx", ".xls")):
        return pd.read_excel(path)
    raise ValueError("Unsupported file type. Use .csv, .xlsx, or .xls")

def build_columns(df):
    return [
        ft.DataColumn(ft.Text(str(col)))
        for col in df.columns
    ]
def build_rows(df: pd.DataFrame):
    rows = []
    for _, row in df.iterrows():
        cells = [
            ft.DataCell(ft.Text("" if pd.isna(row[col]) else str(row[col])))
            for col in df.columns
        ]
        rows.append(ft.DataRow(cells=cells))
    return rows


def dataframe_to_table(df: pd.DataFrame) -> ft.DataTable:
    return ft.DataTable(
        columns=build_columns(df),
        rows=build_rows(df),
        border=ft.border.all(1, BORDER),
        heading_row_color=ft.Colors.BLUE_GREY_50,
    )


def describe_dataframe(df: pd.DataFrame, path: str, shown_columns: int) -> str:
    lines = [
        f"File: {path}",
        f"Shape: {df.shape[0]} rows × {df.shape[1]} columns",
        f"Showing first 5 rows, first {shown_columns} columns in table",
        f"Columns: {list(df.columns)}",
        f"Header row: {list(df.columns)}",
        f"Dtypes:\n{df.dtypes.to_string()}",
        "",
        "Preview (first 5 rows):",
        df.head().to_string(),
    ]
    return "\n".join(lines)


def create_content(
    selected_file_text: ft.Text,
    content_body: ft.Column,
    progress: ft.ProgressRing,
    open_file_picker,
):
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            "Pick file",
                            icon=ft.Icons.UPLOAD_FILE,
                            on_click=open_file_picker,
                        ),
                        progress,
                        selected_file_text,
                    ],
                    spacing=12,
                ),
                content_body,
            ],
            spacing=16,
            expand=True,
        ),
        bgcolor=CONTENT_BG,
        border_radius=8,
        expand=True,
        padding=20,
        margin=ft.padding.all(12),
    )


def main(page: ft.Page):
    page.title = "Telesales"
    page.window_width = 1000
    page.window_height = 700
    page.bgcolor = PAGE_BG
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

    selected_file_text = ft.Text("No file selected", color=ft.Colors.GREY_700)
    file_summary = ft.Text(
        "Pick a CSV or Excel file to inspect columns, shape, and preview.",
        size=12,
        color=ft.Colors.GREY_800,
        selectable=True,
    )
    progress = ft.ProgressRing(visible=False, width=20, height=20)
    table_container = ft.Container(
        content=ft.Text("Pick a file to preview data", color=ft.Colors.GREY_700),
        expand=True,
    )
    content_body = ft.Column(
        controls=[
            file_summary,
            table_container,
        ],
        spacing=12,
        expand=True,
    )

    def set_loading(loading: bool, message: str):
        progress.visible = loading
        selected_file_text.value = message
        progress.update()
        selected_file_text.update()

    def on_file_picker_result(e: ft.FilePickerResultEvent):
        if not e.files:
            set_loading(False, "Cancelled")
            return

        file = e.files[0]
        path = file.path
        set_loading(True, f"Loading {file.name}...")

        try:
            df = load_dataframe(path)
            max_cols = 6
            shown_columns = min(max_cols, df.shape[1])
            subset = df.head().iloc[:, :shown_columns]
            summary = describe_dataframe(df, path, shown_columns)
            file_summary.value = summary
            selected_file_text.value = file.name
            table_container.content = ft.Column(
                controls=[dataframe_to_table(subset)],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            )
            print(summary)
        except Exception as ex:
            file_summary.value = f"Failed to load file:\n{ex}"
            selected_file_text.value = "Load failed"
            table_container.content = ft.Text(f"Failed to load file:\n{ex}", color=ft.Colors.RED)
            print(ex)
        finally:
            progress.visible = False
            progress.update()
            file_summary.update()
            selected_file_text.update()
            table_container.update()

    file_picker = ft.FilePicker(on_result=on_file_picker_result)
    page.overlay.append(file_picker)

    def open_file_picker(e):
        file_picker.pick_files(
            dialog_title="Select spreadsheet",
            allow_multiple=False,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["csv", "xlsx", "xls"],
        )

    page.controls = [
        ft.Container(
            content=ft.Row(
                controls=[
                    create_sidebar(),
                    ft.Column(
                        expand=True,
                        spacing=0,
                        controls=[
                            create_header(),
                            create_content(
                                selected_file_text,
                                content_body,
                                progress,
                                open_file_picker,
                            ),
                        ],
                    ),
                ],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
            expand=True,
            padding=12,
            bgcolor=CARD_BG,
            border_radius=ft.border_radius.all(10),
            border=ft.border.all(1, BORDER),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            shadow=ft.BoxShadow(
                color=ft.Colors.BLUE_GREY_300,
                blur_radius=10,
                offset=ft.Offset(0, 2),
            ),
        ),
    ]
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
