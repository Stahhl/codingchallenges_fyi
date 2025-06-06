export type Statement = {
  kind: "string";
  value: string;
} | {
  kind: "object";
  properties: Statement[]; // can be improved later
};