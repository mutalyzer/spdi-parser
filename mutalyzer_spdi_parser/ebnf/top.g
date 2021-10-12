description: ID ":" position ":" (deleted_sequence | deleted_length)? ":" inserted_sequence?

position: NUMBER

deleted_sequence: SEQUENCE

deleted_length: NUMBER

inserted_sequence: SEQUENCE

ID: (LETTER | DIGIT) (LETTER | DIGIT | "." | "_" | "-")*

NUMBER: DIGIT+

SEQUENCE: NT+

LETTER: UCASE_LETTER | LCASE_LETTER

DIGIT: "0".."9"

NT: "a" | "c" | "g" | "t" | "u" | "r" | "y" | "k"
  | "m" | "s" | "w" | "b" | "d" | "h" | "v" | "n"
  | "A" | "C" | "G" | "T" | "U" | "R" | "Y" | "K"
  | "M" | "S" | "W" | "B" | "D" | "H" | "V" | "N"

LCASE_LETTER: "a".."z"

UCASE_LETTER: "A".."Z"
