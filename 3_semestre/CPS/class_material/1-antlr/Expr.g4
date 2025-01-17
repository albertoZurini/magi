grammar Expr;

prog:   (expr NEWLINE)* ;

// The expression is basically for expressions such as 1 + (1 + 2)
expr:   expr ('*'|'/') expr
    |   expr ('+'|'-') expr
    |   INT
    |   '(' expr ')'
    ;

NEWLINE : [\r\n]+;
INT     : [0-9]+ ;