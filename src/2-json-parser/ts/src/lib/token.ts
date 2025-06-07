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
  // | "whitespace"
  // | "unknown";

export type Token = {
  type: TokenType;
  lexeme: string;
  // deno-lint-ignore no-explicit-any
  literal: any;
};
