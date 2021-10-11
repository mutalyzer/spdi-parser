description: ID ":" point ":" deleted? ":" inserted?

point: NUMBER

deleted: SEQUENCE | length

inserted: SEQUENCE

length: NUMBER

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
