export type Statement = {
  kind: "string";
  value: string;
} | {
  kind: "object";
  properties: {key: string; value: Statement[]}; // can be improved later
};