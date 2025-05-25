import { assert } from "@std/assert";
import { Scanner } from "../src/lib/scanner.ts";


Deno.test(function test() {
  const input = Deno.readTextFileSync(Deno.cwd() + "/test/tests/step1/valid.json")

  const scanner = new Scanner(input);
  const tokens = scanner.scan();

  tokens.forEach(element => {
    console.log(JSON.stringify(element))
  });

  assert(tokens.length > 0)
})
