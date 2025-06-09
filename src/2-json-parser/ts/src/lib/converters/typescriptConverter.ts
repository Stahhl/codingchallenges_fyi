import type { JsonElement } from "../jsonElement";

export class TypeScriptConverter {
    private elements: JsonElement[];

    constructor(elements: JsonElement[]) {
        this.elements = elements;
    }

    convert(): string {
        if (this.elements.length === 0) {
            return "type EmptyType = {};";
        }

        if (this.elements.length === 1) {
            return this.convertElementToType(this.elements[0], "RootType");
        }

        // Multiple elements - create a union type
        const types = this.elements.map((element) =>
            this.convertElementToTypeString(element)
        );

        return `type RootType = ${types.join(" | ")};`;
    }

    private convertElementToType(
        element: JsonElement,
        typeName: string,
    ): string {
        const typeString = this.convertElementToTypeString(element);
        return `type ${typeName} = ${typeString};`;
    }

    private convertElementToTypeString(element: JsonElement): string {
        switch (element.type) {
            case "string":
                return "string";
            case "number":
                return "number";
            case "boolean":
                return "boolean";
            case "null":
                return "null";
            case "object":
                return this.convertObjectToType(element.value);
            case "array":
                return this.convertArrayToType(element.value);
            default:
                throw new Error(
                    `Unknown element type: ${(element as any).type}`,
                );
        }
    }

    private convertObjectToType(obj: Record<string, JsonElement>): string {
        const entries = Object.entries(obj);

        if (entries.length === 0) {
            return "{}";
        }

        const properties = entries.map(([key, value]) => {
            const isOptional = value.type === "null" ? "?" : "";
            const typeString = this.convertElementToTypeString(value);

            return `${key}${isOptional}: ${typeString}`;
        });

        return `{\n${properties.join(";\n")};\n}`;
    }

    private convertArrayToType(arr: JsonElement[]): string {
        if (arr.length === 0) {
            return "unknown[]";
        }

        const uniqueTypes = new Set<string>();

        for (const element of arr) {
            uniqueTypes.add(this.convertElementToTypeString(element));
        }

        const typeArray = Array.from(uniqueTypes);

        if (typeArray.length === 1) {
            return `${typeArray[0]}[]`;
        }

        // Multiple types - create union array
        return `(${typeArray.join(" | ")})[]`;
    }
}
