(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        define(['kaitai-struct/KaitaiStream', 'brotli'], factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = factory(require('kaitai-struct/KaitaiStream'), require('brotli'));
    } else {
        root.Brotli = factory(root.KaitaiStream, brotli);
    }
}(this, function (KaitaiStream, brotli) {
    var Brotli = (function() {
        function Brotli() {
        }
        Brotli.prototype.decode = function(src) {
            return brotli.decompress(src);
        }

        return Brotli;
    })();
    return Brotli;
}));
