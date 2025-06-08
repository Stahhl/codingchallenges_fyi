export type JsonElement =
    | { type: "string"; value: string }
    | { type: "number"; value: number }
    | { type: "boolean"; value: boolean }
    | { type: "null"; value: null }
    | { type: "object"; value: Record<string, JsonElement> }
    | { type: "array"; value: JsonElement[] };
