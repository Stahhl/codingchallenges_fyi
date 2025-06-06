export type TokenType =
  | "brace_left"
  | "brace_right";

export type Token = {
  type: TokenType;
  lexeme: string;
  // deno-lint-ignore no-explicit-any
  literal: any;
};
