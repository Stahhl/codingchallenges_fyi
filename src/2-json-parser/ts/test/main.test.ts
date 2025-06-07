import { readFileSync } from "fs";
import { resolve } from "path";
import { describe, expect, it } from "vitest";
import { Scanner } from "../src/lib/scanner";
import { Parser } from "../src/lib/parser";

function readFile(path: string): string {
  return readFileSync(resolve(process.cwd(), "test/tests" + path), "utf-8");
}

// describe("Test something with input", () => {
//   it("should parse JSON correctly", () => {
//     const data = readFile("/step1/valid.json");
//     const obj = JSON.parse(data);
//     expect(obj).toBeDefined();
//   });
// });

// describe("step 1", () => {
//   it("should be valid", () => {
//     const data = readFile("/step1/valid.json");
//     const scanner = new Scanner(data);
//     const tokens = scanner.scan();
    
//     const parser = new Parser(tokens);
//     parser.parse();

//     expect(parser.errors.length).toBe(0)
//   }),
//     it("should be invalid", () => {
//       const data = readFile("/step1/invalid.json");
//       const scanner = new Scanner(data);
//       const tokens = scanner.scan();

//       const parser = new Parser(tokens);
//       parser.parse();

//       expect(parser.errors.length).toBe(1);
//     });
// });

describe("step 2", () => {
  it("should be valid", () => {
    const data = readFile("/step3/valid.json")
    console.log(data)
    
    const scanner = new Scanner(data);
    const tokens = scanner.scan();

    tokens.forEach(token => console.log(token));

    scanner.errors.forEach(e => console.log(e));

    expect(scanner.errors.length).toBe(0)
  })
})
