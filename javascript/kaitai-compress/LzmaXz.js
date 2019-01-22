(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define(['kaitai-struct/KaitaiStream', 'lzma'], factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = factory(require('kaitai-struct/KaitaiStream'), require('lzma'));
    } else {
        root.LzmaXz = factory(root.KaitaiStream, LZMA);
    }
}(this, function (KaitaiStream, RealLZMA) {
    var LzmaXz = (function() {
        function LzmaXz() {
        }
        LzmaXz.prototype.decode = function(src) {
            return RealLZMA.decompress(src);
        }

        return LzmaXz;
    })();
    return LzmaXz;
}));
