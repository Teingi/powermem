// Test script to demonstrate precision loss issue and solution
// Run with: node test_precision.js

// Original values as strings (from server/database)
const originalIds = {
  id1: '653423919000190976',
  id2: '653247040368672768'
};

console.log('=== Precision Loss Issue Demo ===\n');
console.log('Original IDs (from server):', originalIds, '\n');

// Test 1: Integer IDs in JSON (precision loss)
console.log('1. Integer IDs in JSON (PRECISION LOST):');
const jsonWithInts = `{"id1":${originalIds.id1},"id2":${originalIds.id2}}`;
console.log('   JSON:', jsonWithInts);
const parsedInts = JSON.parse(jsonWithInts);
console.log('   Parsed:', parsedInts);
console.log('   Original id2:', originalIds.id2);
console.log('   Parsed id2: ', parsedInts.id2.toString());
console.log('   Match:', originalIds.id2 === parsedInts.id2.toString(), '❌ (precision lost)\n');

// Test 2: String IDs (no precision loss)
console.log('2. String IDs in JSON (PRECISION PRESERVED):');
const jsonWithStrings = `{"id1":"${originalIds.id1}","id2":"${originalIds.id2}"}`;
console.log('   JSON:', jsonWithStrings);
const parsedStrings = JSON.parse(jsonWithStrings);
console.log('   Parsed:', parsedStrings);
console.log('   Original id2:', originalIds.id2);
console.log('   Parsed id2: ', parsedStrings.id2);
console.log('   Match:', originalIds.id2 === parsedStrings.id2, '✅ (exact match)\n');

// Test 3: Convert to BigInt
console.log('3. Convert String IDs to BigInt:');
const bigIntIds = {
  id1: BigInt(parsedStrings.id1),
  id2: BigInt(parsedStrings.id2)
};
console.log('   BigInt ids:', bigIntIds);
console.log('   Original as BigInt:', BigInt(originalIds.id2));
console.log('   Parsed as BigInt: ', bigIntIds.id2);
console.log('   Match:', BigInt(originalIds.id2) === bigIntIds.id2, '✅ (exact match)\n');

// Test 4: Comparison
console.log('4. Comparison:');
console.log('   Original value:     ', originalIds.id2);
console.log('   Integer approach:   ', originalIds.id2, '→', parsedInts.id2.toString(), '❌ (lost precision)');
console.log('   String approach:    ', originalIds.id2, '→', parsedStrings.id2, '✅ (exact match)');
console.log('   BigInt approach:    ', originalIds.id2, '→', bigIntIds.id2.toString(), '✅ (exact match)\n');

console.log('=== Conclusion ===');
console.log('✅ String IDs preserve precision');
console.log('✅ Can be converted to BigInt if needed');
console.log('✅ No client-side changes required for basic usage');
console.log('✅ Works with standard JSON.parse()');
