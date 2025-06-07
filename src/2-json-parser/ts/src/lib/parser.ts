import type { Statement } from "./statements";
import type { Token, TokenType } from "./token";

export class Parser {
    private tokens: Token[];
    private current = 0;
    public errors: string[] = [];

    constructor(tokens: Token[]) {
        this.tokens = tokens;
    }

    parse(): Statement[] {
        if (this.tokens.length <= 0) {
            this.errors.push("Invalid input...");
            return [];
        }

        const statements: Statement[] = [];

        while (!this.isAtEnd()) {
            this.advance();
        }

        return statements;
    }

    private advance(): Token {
        return this.tokens[this.current++];
    }

    private isAtEnd(): boolean {
        return this.current >= this.tokens.length;
    }
}
