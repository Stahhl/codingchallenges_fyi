export type TokenType =
  | "brace_open"
  | "brace_close"
  | "bracket_open"
  | "bracket_close"
  | "colon"
  | "comma"
  | "string"
  | "number"
  | "boolean"
  | "null";

export type Token = {
  type: TokenType;
  lexeme: string;
  literal: any;
};
