import { assertEquals } from "@std/assert";
import { sum } from "../src/lib/parser.ts"

Deno.test(function addTest() {
  assertEquals(sum(2, 3), 5);
});
