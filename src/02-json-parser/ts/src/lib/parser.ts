import type { JsonElement } from "./jsonElement";
import type { Token, TokenType } from "./token";

export class Parser {
    private tokens: Token[];
    private current: number = 0;
    public errors: string[] = [];

    constructor(tokens: Token[]) {
        this.tokens = tokens;
    }

    parse(): JsonElement[] {
        this.errors = [];
        this.current = 0;
        const elements: JsonElement[] = [];

        if (this.tokens.length <= 0) this.errors.push("no tokens to parse...");

        while (!this.isAtEnd()) {
            try {
                const element = this.parseValue();
                if (element) {
                    elements.push(element);
                }
            } catch (error) {
                this.errors.push(
                    error instanceof Error ? error.message : String(error),
                );
                // After a validation error find a good place to keep parsing. So we can present as many errors as possible to the user.
                this.synchronize();
            }
        }

        return elements;
    }

    private parseValue(): JsonElement {
        const token = this.peek();

        switch (token.type) {
            case "string":
                this.advance();
                return { type: "string", value: token.literal };

            case "number":
                this.advance();
                return { type: "number", value: token.literal };

            case "boolean":
                this.advance();
                return { type: "boolean", value: token.literal };

            case "null":
                this.advance();
                return { type: "null", value: null };

            case "brace_open":
                return this.parseObject();

            case "bracket_open":
                return this.parseArray();

            default:
                throw new Error(
                    `Unexpected token: ${token.type} at position ${this.current}`,
                );
        }
    }

    private parseObject(): JsonElement {
        this.consume("brace_open", "Expected '{' to start object");

        const obj: Record<string, JsonElement> = {};

        // Handle empty object
        if (this.check("brace_close")) {
            this.advance();
            return { type: "object", value: obj };
        }

        do {
            // Parse key
            if (!this.check("string")) {
                throw new Error(
                    `Expected string key in object at position ${this.current}`,
                );
            }
            const key = this.advance().literal;

            // Parse colon
            this.consume("colon", "Expected ':' after object key");

            // Parse value
            const value = this.parseValue();
            obj[key] = value;
        } while (this.match("comma"));

        this.consume("brace_close", "Expected '}' to close object");
        return { type: "object", value: obj };
    }

    private parseArray(): JsonElement {
        this.consume("bracket_open", "Expected '[' to start array");

        const arr: JsonElement[] = [];

        // Handle empty array
        if (this.check("bracket_close")) {
            this.advance();
            return { type: "array", value: arr };
        }

        do {
            const value = this.parseValue();
            arr.push(value);
        } while (this.match("comma"));

        this.consume("bracket_close", "Expected ']' to close array");
        return { type: "array", value: arr };
    }

    // Utility methods
    private peek(): Token {
        return this.tokens[this.current];
    }

    private advance(): Token {
        if (!this.isAtEnd()) this.current++;
        return this.previous();
    }

    private previous(): Token {
        return this.tokens[this.current - 1];
    }

    private isAtEnd(): boolean {
        return this.current >= this.tokens.length;
    }

    private check(type: TokenType): boolean {
        if (this.isAtEnd()) return false;
        return this.peek().type === type;
    }

    private match(...types: TokenType[]): boolean {
        for (const type of types) {
            if (this.check(type)) {
                this.advance();
                return true;
            }
        }
        return false;
    }

    private consume(type: TokenType, message: string): Token {
        if (this.check(type)) return this.advance();

        const current = this.isAtEnd() ? "EOF" : this.peek().type;
        throw new Error(
            `${message}. Got ${current} at position ${this.current}`,
        );
    }

    private synchronize(): void {
        // Skip tokens until we find a likely recovery point
        while (!this.isAtEnd()) {
            const token = this.peek();
            if (
                token.type === "brace_close" ||
                token.type === "bracket_close" ||
                token.type === "comma"
            ) {
                this.advance();
                break;
            }
            this.advance();
        }
    }
}
