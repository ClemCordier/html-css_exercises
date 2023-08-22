expected_answers = {
    "space":
        [
            ("body", {"font-family": {"'comic sans ms'", '"comic sans ms"'} })
        ],
    "multiple_fonts":
        [
            ("body", {"font-family": {"'comic sans ms', consolas", '"comic sans ms", consolas'} })
        ],
    "generic_font":
        [
            ("body", {"font-family": {"'comic sans ms', consolas, sans-serif", '"comic sans ms", consolas, sans-serif'} })
        ]
}