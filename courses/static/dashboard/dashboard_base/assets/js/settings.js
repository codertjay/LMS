! function(e) {
    var r = {};

    function t(n) {
        if (r[n]) return r[n].exports;
        var o = r[n] = {
            i: n,
            l: !1,
            exports: {}
        };
        return e[n].call(o.exports, o, o.exports, t), o.l = !0, o.exports
    }
    t.m = e, t.c = r, t.d = function(e, r, n) {
        t.o(e, r) || Object.defineProperty(e, r, {
            enumerable: !0,
            get: n
        })
    }, t.r = function(e) {
        "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(e, Symbol.toStringTag, {
            value: "Module"
        }), Object.defineProperty(e, "__esModule", {
            value: !0
        })
    }, t.t = function(e, r) {
        if (1 & r && (e = t(e)), 8 & r) return e;
        if (4 & r && "object" == typeof e && e && e.__esModule) return e;
        var n = Object.create(null);
        if (t.r(n), Object.defineProperty(n, "default", {
                enumerable: !0,
                value: e
            }), 2 & r && "string" != typeof e)
            for (var o in e) t.d(n, o, function(r) {
                return e[r]
            }.bind(null, o));
        return n
    }, t.n = function(e) {
        var r = e && e.__esModule ? function() {
            return e.default
        } : function() {
            return e
        };
        return t.d(r, "a", r), r
    }, t.o = function(e, r) {
        return Object.prototype.hasOwnProperty.call(e, r)
    }, t.p = "/", t(t.s = 487)
}({
    487: function(e, r, t) {
        e.exports = t(488)
    },
    488: function(e, r, t) {
        "use strict";
        t.r(r);
        t(489)
    },
    489: function(e, r) {
        var t, n, o, a, i, c = {
                gray: {
                    300: "#E3EBF6",
                    600: "#95AAC9",
                    700: "#6E84A3",
                    800: "#152E4D",
                    900: "#283E59"
                },
                primary: {
                    50: "#e3f2fd",
                    100: "#bbdefb",
                    200: "#90c9f9",
                    300: "#63b4f6",
                    400: "#42a4f5",
                    500: "#2196F3",
                    600: "#1f87e5",
                    700: "#1a75d2",
                    800: "#1764c0",
                    900: "#1045a1"
                },
                success: {
                    50: "#e8f5e9",
                    100: "#c8e6c9",
                    200: "#a5d6a7",
                    300: "#81c784",
                    400: "#66BB6A",
                    500: "#4caf50",
                    600: "#43a047",
                    700: "#388e3c",
                    800: "#2e7d32",
                    900: "#1b5e20"
                },
                black: "#383B3D",
                white: "#FFFFFF",
                transparent: "transparent"
            },
            f = {
                fonts: {
                    base: 'Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"'
                },
                colors: c,
                charts: {
                    colorScheme: "light",
                    colors: {
                        area: (t = c.primary[500], n = .24, o = parseInt(t.slice(1, 3), 16), a = parseInt(t.slice(3, 5), 16), i = parseInt(t.slice(5, 7), 16), n ? "rgba(" + o + ", " + a + ", " + i + ", " + n + ")" : "rgb(" + o + ", " + a + ", " + i + ")")
                    }
                }
            };
        "undefined" != typeof window && (window.settings = f)
    }
});