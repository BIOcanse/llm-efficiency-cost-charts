import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import {paretoRows} from "../../site/assets/interactive-scatter.js";

const keys = {subscription: "subscription_per_attempt", api: "api_per_attempt", token: "token_per_attempt"};
const counts = {"4.0": [5, 5, 4], "3.0": [4, 4, 5], "2.1": [5, 5, 5], "2.0": [0, 0, 0], "1.0": [0, 0, 0]};
let checked = 0;
for (const [version, expectedCounts] of Object.entries(counts)) {
  const payload = JSON.parse(readFileSync(new URL(`../../site/data/terminal-bench/${version}/2026-09-05.json`, import.meta.url), "utf8"));
  const actualCounts = [];
  for (const [metric, key] of Object.entries(keys)) {
    const selected = paretoRows(payload.rows, key);
    assert.deepEqual(selected.map(row => row.id), payload.frontiers[metric]);
    const eligible = payload.rows.filter(row => Number.isFinite(row[key]));
    const oracle = eligible.filter(row => !eligible.some(other => other[key] <= row[key] && other.score >= row.score && (other[key] < row[key] || other.score > row.score)));
    assert.deepEqual(new Set(selected.map(row => row.id)), new Set(oracle.map(row => row.id)));
    actualCounts.push(selected.length); checked++;
  }
  assert.deepEqual(actualCounts, expectedCounts);
}
const ties = [{id:"a",x:0,score:10}, {id:"b",x:0,score:10}, {id:"c",x:1,score:10}, {id:"d",x:1,score:20}, {id:"e",x:2,score:19}, {id:"f",x:3,score:30}, {id:"g",x:null,score:100}, {id:"h",x:NaN,score:100}, {id:"i",x:-1,score:100}, {id:"j",x:0,score:null}];
assert.deepEqual(paretoRows(ties, "x").map(row => row.id), ["a","b","d","f"]);
assert.deepEqual(paretoRows([], "x"), []);
console.log(JSON.stringify({checkedVersionMetrics: checked, sharedJsMatchesPythonAndPairwiseOracle: true, tiesAndMissing: "pass"}));
