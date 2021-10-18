description: ID ":" position ":" (deleted_sequence | deleted_length)? ":" inserted_sequence?

position: NUMBER

deleted_sequence: sequence

deleted_length: NUMBER

inserted_sequence: sequence

ID: (LETTER | DIGIT) (LETTER | DIGIT | "." | "_" | "-")*

NUMBER: DIGIT+

sequence: D_SEQUENCE | R_SEQUENCE | P_SEQUENCE

LETTER: UCASE_LETTER | LCASE_LETTER

DIGIT: "0".."9"

D_SEQUENCE: D_NT+

D_NT: "A" | "C" | "G" | "T" | "B" | "D" | "H" | "K" | "M"
     | "N" | "R" | "S" | "V" | "W" | "Y"

R_SEQUENCE: R_NT+

R_NT: "a" | "c" | "g" | "u" | "b" | "d" | "h" | "k" | "m"
    | "n" | "r" | "s" | "v" | "w" | "y"

P_SEQUENCE: AA+

AA: "Ala" | "Arg" | "Asn" | "Asp" | "Cys" | "Gln" | "Glu"
  | "Gly" | "His" | "Ile" | "Leu" | "Lys" | "Met" | "Phe"
  | "Pro" | "Ser" | "Thr" | "Trp" | "Tyr" | "Val"
  | "Sec"
  | "Ter"
  | "Xaa"
  | "A"   | "R"   | "N"   | "D"   | "C"   | "Q"   | "E"
  | "G"   | "H"   | "I"   | "L"   | "K"   | "M"   | "F"
  | "P"   | "S"   | "T"   | "W"    | "Y"  | "V"
  | "U"
  | "*"
  | "X"

LCASE_LETTER: "a".."z"

UCASE_LETTER: "A".."Z"
