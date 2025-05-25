import { readFileSync } from 'fs';
import { resolve } from 'path';
import { describe, it, expect } from 'vitest';

const input = readFileSync(
  resolve(process.cwd(), 'test/tests/step1/valid.json'),
  'utf-8'
);

// test

describe('Test something with input', () => {
  it('should parse JSON correctly', () => {
    const data = JSON.parse(input);
    console.log(data)
    expect(data).toBeDefined();
    // Your assertions here
  });
});
