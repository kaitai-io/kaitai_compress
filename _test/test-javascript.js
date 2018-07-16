var assert = require('assert');
var KaitaiStream = global.KaitaiStream = require("kaitai-struct/KaitaiStream");
var fs = require('fs');

function testData(parser, dataName, dataExt) {
    describe(dataExt + " - " + dataName, function() {
        it('parses test properly', function(done) {
            fs.readFile("compressed/" + dataName + "." + dataExt, function(err, compBuf) {
                var st = new KaitaiStream(compBuf);
                var r = new parser(st);

                var uncompHex = fs.readFileSync("uncompressed/" + dataName + ".dat").toString('hex');
                var actualHex = Buffer.from(r.body).toString('hex');
                assert.strictEqual(actualHex, uncompHex);
                done();
            });
        });
    });
}

let tests = {
    "lz4": require("TestLz4"),
}

for (var testName in tests) {
    var parser = tests[testName];
    testData(parser, "90_a", testName);
    testData(parser, "25k_uuids", testName);
    testData(parser, "ascii_text", testName);
}

