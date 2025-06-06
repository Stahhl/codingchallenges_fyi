import type { Token } from "./token";

export class Scanner {
  private tokens: Token[] = [];
  private source: string;
  private start = 0;
  private current = 0;

  constructor(data: string) {
    this.source = data;
  }

  scan(): Token[] {
    while (this.current < this.source.length) {
      this.start = this.current
      this.scanToken()
    }

    return this.tokens;
  }

  private scanToken() {
    const c = this.advance();

    switch (c) {
      case "{": {
        this.tokens.push({ type: "brace_left", lexeme: "{", literal: null })
        break
      }
      case "}": {
        this.tokens.push({ type: "brace_right", lexeme: "}", literal: null })
        break
      }
      default: {
        break
      }
    }
  }

  private advance(): string {
    return this.source[this.current++];
  }
}


