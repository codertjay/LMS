! function(e) {
    var t = {};

    function r(a) {
        if (t[a]) return t[a].exports;
        var n = t[a] = {
            i: a,
            l: !1,
            exports: {}
        };
        return e[a].call(n.exports, n, n.exports, r), n.l = !0, n.exports
    }
    r.m = e, r.c = t, r.d = function(e, t, a) {
        r.o(e, t) || Object.defineProperty(e, t, {
            enumerable: !0,
            get: a
        })
    }, r.r = function(e) {
        "undefined" != typeof Symbol && Symbol.toStringTag && Object.defineProperty(e, Symbol.toStringTag, {
            value: "Module"
        }), Object.defineProperty(e, "__esModule", {
            value: !0
        })
    }, r.t = function(e, t) {
        if (1 & t && (e = r(e)), 8 & t) return e;
        if (4 & t && "object" == typeof e && e && e.__esModule) return e;
        var a = Object.create(null);
        if (r.r(a), Object.defineProperty(a, "default", {
                enumerable: !0,
                value: e
            }), 2 & t && "string" != typeof e)
            for (var n in e) r.d(a, n, function(t) {
                return e[t]
            }.bind(null, n));
        return a
    }, r.n = function(e) {
        var t = e && e.__esModule ? function() {
            return e.default
        } : function() {
            return e
        };
        return r.d(t, "a", t), t
    }, r.o = function(e, t) {
        return Object.prototype.hasOwnProperty.call(e, t)
    }, r.p = "/", r(r.s = 590)
}({
    590: function(e, t, r) {
        e.exports = r(591)
    },
    591: function(e, t) {
        var r, a, n;
        r = jQuery, a = {
            map: {
                checkbox: "fa fa-square-o fa-fw",
                checkboxSelected: "fa fa-check-square fa-fw",
                checkboxUnknown: "fa fa-check-square fa-fw fa-muted",
                error: "fa fa-exclamation-triangle fa-fw",
                expanderClosed: "fa fa-caret-right fa-fw",
                expanderLazy: "fa fa-angle-right fa-fw",
                expanderOpen: "fa fa-caret-down fa-fw",
                doc: "fa fa-file-o fa-fw",
                noExpander: "",
                docOpen: "fa fa-file fa-fw",
                loading: "fa fa-refresh fa-spin fa-fw",
                folder: "fa fa-folder fa-fw",
                folderOpen: "fa fa-folder-open fa-fw"
            }
        }, n = {
            autoExpandMS: 400,
            focusOnClick: !0,
            preventVoidMoves: !0,
            preventRecursiveMoves: !0,
            dragStart: function(e, t) {
                return !0
            },
            dragEnter: function(e, t) {
                return !0
            },
            dragDrop: function(e, t) {
                t.otherNode.moveTo(e, t.hitMode)
            }
        }, r.fn.APFancyTree = function() {
            if (this.length && void 0 !== r.fn.fancytree) {
                var e = ["glyph"];
                void 0 !== this.attr("data-tree-dnd") && e.push("dnd"), this.fancytree({
                    extensions: e,
                    glyph: a,
                    dnd: n,
                    clickFolderMode: 3,
                    checkbox: void 0 !== this.attr("data-tree-checkbox") || !1,
                    selectMode: void 0 !== this.attr("data-tree-select") ? parseInt(this.attr("data-tree-select")) : 2
                })
            }
        }, r('[data-toggle="tree"]').each(function() {
            r(this).APFancyTree()
        })
    }
});