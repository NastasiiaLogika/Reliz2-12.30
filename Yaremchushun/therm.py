# theme.py
def apply_theme(widget, input_field, is_dark):
    if is_dark:
        widget.setStyleSheet("background-color: #2e2e2e; color: white;")
        input_field.setStyleSheet("background: #3c3c3c; color: white; border: none; padding: 10px;")
    else:
        widget.setStyleSheet("background-color: red; color: black;")
        input_field.setStyleSheet("background: white; color: black; border: none; padding: 10px;")
