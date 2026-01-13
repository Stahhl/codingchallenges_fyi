import type { JsonElement } from "../jsonElement";

export class JavascriptConverter {
    private elements: JsonElement[];

    constructor(elements: JsonElement[]) {
        this.elements = elements;
    }

    convert(): string {
        if (this.elements.length === 0) {
            return "{}";
        }

        if (this.elements.length === 1) {
            return this.convertElement(this.elements[0]);
        }

        // Multiple elements - wrap in array
        const convertedElements = this.elements.map((element) =>
            this.convertElement(element)
        );
        return `[${convertedElements.join(", ")}]`;
    }

    private convertElement(element: JsonElement): string {
        switch (element.type) {
            case "string":
                return `"${element.value}"`;

            case "number":
                return element.value.toString();

            case "boolean":
                return element.value.toString();

            case "null":
                return "null";

            case "object":
                return this.convertObject(element.value);

            case "array":
                return this.convertArray(element.value);

            default:
                throw new Error(
                    `Unknown element type: ${(element as any).type}`,
                );
        }
    }

    private convertObject(obj: Record<string, JsonElement>): string {
        const entries = Object.entries(obj);

        if (entries.length === 0) {
            return "{}";
        }

        const pairs = entries.map(([key, value]) => `${key}: ${this.convertElement(value)}`);

        return `{ ${pairs.join(", ")} }`;
    }

    private convertArray(arr: JsonElement[]): string {
        if (arr.length === 0) {
            return "[]";
        }

        const elements = arr.map((element) => this.convertElement(element));
        return `[${elements.join(", ")}]`;
    }
}
