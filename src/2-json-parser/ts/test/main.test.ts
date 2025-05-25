import { readFileSync } from 'fs';
import { resolve } from 'path';
import { describe, it, expect } from 'vitest';

const input = readFileSync(
  resolve(process.cwd(), 'test/tests/step1/valid.json'),
  'utf-8'
);

describe('Test something with input', () => {
  it('should parse JSON correctly', () => {
    const data = JSON.parse(input);
    console.log(data)
    expect(data).toBeDefined();
    // Your assertions here
  });
});

// import { assert } from "jsr:@std/assert";
// import { Scanner } from "../src/lib/scanner.ts";


// Deno.test(function test() {
//   const input = Deno.readTextFileSync(Deno.cwd() + "/test/tests/step1/valid.json")

//   const scanner = new Scanner(input);
//   const tokens = scanner.scan();

//   tokens.forEach(element => {
//     console.log(JSON.stringify(element))
//   });

//   assert(tokens.length > 0)
// })
