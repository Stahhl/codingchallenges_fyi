import type { Token, TokenType } from "./token";

export class Scanner {
  private tokens: Token[] = [];
  private source: string;
  private start = 0;
  private current = 0;
  errors: string[] = [];

  constructor(data: string) {
    this.source = data.replace(/\s+/g, ""); // remove whitespace, linebreaks
  }

  scan(): Token[] {
    while (!this.isAtEnd()) {
      this.start = this.current;
      this.scanToken();
    }

    return this.tokens;
  }

  private scanToken() {
    const c = this.advance();

    switch (c) {
      case "{": {
        this.addToken({ type: "brace_open", lexeme: "{", literal: null });
        break;
      }
      case "}": {
        this.addToken({ type: "brace_close", lexeme: "}", literal: null });
        break;
      }
      case "[": {
        this.addToken({ type: "bracket_open", lexeme: "[", literal: null });
        break;
      }
      case "]": {
        this.addToken({ type: "bracket_close", lexeme: "]", literal: null });
        break;
      }
      case ":": {
        this.addToken({ type: "colon", lexeme: ":", literal: null });
        break;
      }
      case ",": {
        this.addToken({ type: "comma", lexeme: ",", literal: null });
        break;
      }
      case '"': {
        this.string();
        break;
      }
      default: {
        console.log(`DEFAULT: ${c}`);
        if (this.number(c)) break;
        if (this.keyword()) break;
        this.errors.push(`Unrecognized '${c}' at position ${this.current}`);
        break;
      }
    }
  }

  private number(char: string): boolean {
    if (!this.isDigit(char)) return false;
    while (this.isDigit(this.peek())) this.advance();

    // decimals
    if (this.peek() == "." && this.isDigit(this.peek(1))) {
      this.advance();

      while (this.isDigit(this.peek())) this.advance();
    }

    const lexeme = this.source.substring(this.start, this.current);

    this.addToken({
      type: "number",
      lexeme: lexeme,
      literal: parseFloat(lexeme),
    });

    return true;
  }

  private keyword(): boolean {
    while (!this.isAtEnd()) {
      const nc = this.peek();

      if (nc == "," || nc == "}" || nc == "]") {
        break;
      }

      this.advance();
    }

    if (this.isAtEnd()) {
      this.errors.push("Unterminated keyword...");
      return false;
    }

    const lexeme = this.source.substring(this.start, this.current);

    if (lexeme == "null") {
      this.addToken({ type: "null", lexeme: lexeme, literal: null });
      return true;
    }
    if (lexeme == "true") {
      this.addToken({ type: "boolean", lexeme: lexeme, literal: true });
      return true;
    }
    if (lexeme == "false") {
      this.addToken({ type: "boolean", lexeme: lexeme, literal: false });
      return true;
    }

    return false;
  }

  private isDigit(char: string): boolean {
    return /^[0-9]$/.test(char);
  }

  private string() {
    while (this.peek() != '"' && !this.isAtEnd()) {
      this.advance();
    }

    if (this.isAtEnd()) {
      this.errors.push("Unterminated string...");
      return;
    }

    this.advance();

    const lexeme = this.source.substring(this.start, this.current);
    const literal = this.source.substring(this.start + 1, this.current - 1);

    this.addToken({ type: "string", lexeme: lexeme, literal: literal });
  }

  private addToken(token: Token) {
    this.tokens.push(token);
  }

  private peek(offset: number = 0): string {
    if (this.isAtEnd(offset)) return "";
    return this.source[this.current + offset];
  }

  private advance(): string {
    return this.source[this.current++];
  }

  private isAtEnd(offset: number = 0): boolean {
    return this.current + offset >= this.source.length;
  }
}
