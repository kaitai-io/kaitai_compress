(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define(['kaitai-struct/KaitaiStream', 'lz4'], factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = factory(require('kaitai-struct/KaitaiStream'), require('lz4'));
    } else {
        root.Lz4 = factory(root.KaitaiStream, LZ4);
    }
}(this, function (KaitaiStream, RealLZ4) {
    var Lz4 = (function() {
        function Lz4() {
        }
        Lz4.prototype.decode = function(src) {
            return RealLZ4.decode(src);
        }

        return Lz4;
    })();
    return Lz4;
}));
