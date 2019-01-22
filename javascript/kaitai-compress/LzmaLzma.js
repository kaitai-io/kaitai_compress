(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define(['kaitai-struct/KaitaiStream', 'lzma'], factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = factory(require('kaitai-struct/KaitaiStream'), require('lzma'));
    } else {
        root.LzmaLzma = factory(root.KaitaiStream, LZMA);
    }
}(this, function (KaitaiStream, RealLZMA) {
    var LzmaLzma = (function() {
        function LzmaLzma() {
        }
        LzmaLzma.prototype.decode = function(src) {
            return RealLZMA.decompress(src);
        }

        return LzmaLzma;
    })();
    return LzmaLzma;
}));
