expected_answers = {
    "px":
        [
            ("h1", {"font-size": "38px"}),
            ("h2", {"font-size": "28px"}),
            ({"p, ul", "li, p"}, {"font-size": "18px"})
        ],
    "em":
        [
            ("p, strong", {"font-size": "1.5em"})
        ],
    "rem":
        [
            ("p, strong", {"font-size": "1.5rem"})
        ]
}
