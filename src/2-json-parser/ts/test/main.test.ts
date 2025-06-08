import { readFileSync } from "fs";
import { resolve } from "path";
import { describe, expect, it } from "vitest";
import { Scanner } from "../src/lib/scanner";
import { Parser } from "../src/lib/parser";

function readFile(path: string): string {
  return readFileSync(resolve(process.cwd(), "test/tests" + path), "utf-8");
}

describe("Test something with input", () => {
  it("should parse JSON correctly", () => {
    const data = readFile("/step1/valid.json");
    const obj = JSON.parse(data);
    expect(obj).toBeDefined();
  });
});

describe("step 1", () => {
  it("1 - should be valid", () => {
    const data = readFile("/step1/valid.json");
    const scanner = new Scanner(data);
    const tokens = scanner.scan();

    const parser = new Parser(tokens);
    parser.parse();

    expect(parser.errors.length).toBe(0);
  }),
    it("2 - should be invalid", () => {
      const data = readFile("/step1/invalid.json");
      const scanner = new Scanner(data);
      const tokens = scanner.scan();

      const parser = new Parser(tokens);
      parser.parse();

      expect(parser.errors.length).toBe(1);
    });
});

describe("step 2", () => {
  it("1 - should be valid 1", () => {
    const data = readFile("/step2/valid.json");

    const scanner = new Scanner(data);
    const tokens = scanner.scan();

    const parser = new Parser(tokens);
    parser.parse();

    expect(parser.errors.length).toBe(0);
  }),
    it("2 - should be valid", () => {
      const data = readFile("/step2/valid2.json");

      const scanner = new Scanner(data);
      const tokens = scanner.scan();

      const parser = new Parser(tokens);
      parser.parse();

      expect(parser.errors.length).toBe(0);
    }),
    it("3 - should be invalid", () => {
      const data = readFile("/step2/invalid.json");

      const scanner = new Scanner(data);
      const tokens = scanner.scan();

      const parser = new Parser(tokens);
      parser.parse();

      expect(parser.errors.length).toBe(1);
    }),
    it("4 - should be invalid", () => {
      const data = readFile("/step2/invalid2.json");

      const scanner = new Scanner(data);
      const tokens = scanner.scan();

      const parser = new Parser(tokens);
      parser.parse();

      expect(parser.errors.length).toBe(1);
    });
});

describe("step 3", () => {
  it("1 - shuld be valid", () => {
    const data = readFile("/step3/valid.json");

    const scanner = new Scanner(data);
    const tokens = scanner.scan();

    const parser = new Parser(tokens);
    parser.parse();

    expect(parser.errors.length).toBe(0);
  }),
   it("2 - shuld be invalid", () => {
    const data = readFile("/step3/invalid.json");

    const scanner = new Scanner(data);
    const tokens = scanner.scan();

    const parser = new Parser(tokens);
    parser.parse();

    // parser.errors.forEach(e => console.log(e));

    expect(parser.errors.length).toBe(4);
  }) 
});

describe("step 4", () => {
  it("1 - shuld be valid", () => {
    const data = readFile("/step4/valid.json");

    const scanner = new Scanner(data);
    const tokens = scanner.scan();

    const parser = new Parser(tokens);
    parser.parse();

    expect(parser.errors.length).toBe(0);
  }),
   it("2 - shuld be valid", () => {
    const data = readFile("/step4/valid2.json");

    const scanner = new Scanner(data);
    const tokens = scanner.scan();

    const parser = new Parser(tokens);
    parser.parse();

    expect(parser.errors.length).toBe(0);
  }),
  it("3 - should be invalid", () => {
    const data = readFile("/step4/invalid.json");

    const scanner = new Scanner(data);
    const tokens = scanner.scan();

    scanner.errors.forEach(e => console.log(e));
    tokens.forEach(t => console.log(t));

    const parser = new Parser(tokens);
    const elements = parser.parse();

    parser.errors.forEach(e => console.log(e));
    elements.forEach(e => console.log(e));

    expect(scanner.errors.length).toBeGreaterThan(0);
    expect(parser.errors.length).toBe(0);
  }) 
});