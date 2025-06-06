import type { Statement } from "./statements";
import type { Token } from "./token";

export class Parser {
    private tokens: Token[];
    private current = 0;
    public errors: string[] = [];

    constructor(tokens: Token[]) {
        this.tokens = tokens;
    }

    parse(): Statement[] {
        if (this.tokens.length <= 0) this.errors.push("No tokens...");

        return [];
    }
}
