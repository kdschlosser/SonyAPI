(function (h, l, g) {
    var q;
    var f = function (t, s) {
            if ((this.element = (typeof(t) === "string") ? e(t) : t)) {
                this.css              = {
                    idRulePrefix: "#" + this.element.id + " ",
                    sheet       : null,
                    rules       : {}
                };
                this.columns          = 0;
                this.columnWidths     = [];
                this.cellData         = {
                    head: [],
                    body: [],
                    foot: []
                };
                this.alignTimer       = null;
                this.rawData          = [];
                this.sortCache        = {};
                this.lastSortedColumn = [
                    -1, null
                ];
                this.selectedIndexes  = [];
                this.usesTouch        = (h.ontouchstart !== g);
                this.startEvt         = (this.usesTouch) ? "touchstart" : "mousedown";
                this.moveEvt          = (this.usesTouch) ? "touchmove" : "mousemove";
                this.endEvt           = (this.usesTouch) ? "touchend" : "mouseup";
                this.setOptions(s);
                this.init()
            }
        };
    (q = f.prototype).nothing          = function () {};
    q.setOptions                       = function (t) {
        var s = Object.prototype.hasOwnProperty,
            u;
        this.options = {
            srcType                   : "",
            srcData                   : "",
            allowGridResize           : false,
            allowColumnResize         : false,
            allowClientSideSorting    : false,
            allowSelections           : false,
            allowMultipleSelections   : false,
            showSelectionColumn       : false,
            onColumnSort              : this.nothing,
            onResizeGrid              : this.nothing,
            onResizeGridEnd           : this.nothing,
            onResizeColumn            : this.nothing,
            onResizeColumnEnd         : this.nothing,
            onRowSelect               : this.nothing,
            onLoad                    : this.nothing,
            supportMultipleGridsInView: false,
            fixedCols                 : 0,
            selectedBgColor           : "#eaf1f7",
            fixedSelectedBgColor      : "#dce7f0",
            colAlign                  : [],
            colBGColors               : [],
            colSortTypes              : [],
            customSortCleaner         : null
        };
        if (t) {
            for (u in this.options) {
                if (s.call(this.options, u) && t[u] !== g) {
                    this.options[u] = t[u]
                }
            }
        }
        this.options.allowColumnResize       = this.options.allowColumnResize && !this.usesTouch;
        this.options.allowMultipleSelections = this.options.allowMultipleSelections && this.options.allowSelections;
        this.options.showSelectionColumn     = this.options.showSelectionColumn && this.options.allowSelections;
        this.options.fixedCols               = (!this.usesTouch) ? this.options.fixedCols : 0
    };
    q.init                             = function () {
        var t = this.options.srcType,
            u = this.options.srcData,
            s;
        this.generateSkeleton();
        this.addEvents();
        if (t === "dom" && (u = (typeof(u) === "string") ? e(u) : u)) {
            this.convertData(this.convertDomDataToJsonData(u))
        } else {
            if (t === "json" && (s = a(u))) {
                this.convertData(s)
            } else {
                if (t === "xml" && (s = j(u))) {
                    this.convertData(this.convertXmlDataToJsonData(s))
                }
            }
        }
        this.generateGrid();
        this.displayGrid()
    };
    q.generateSkeleton                 = function () {
        var v = l,
            s = [
                [
                    "base", "mgBase", "docFrag"
                ], [
                    "head", "mgHead", "base"
                ], [
                    "headFixed", "mgHeadFixed", "head"
                ], [
                    "headStatic", "mgHeadStatic", "head"
                ], [
                    "foot", "mgFoot", "base"
                ], [
                    "footFixed", "mgFootFixed", "foot"
                ], [
                    "footStatic", "mgFootStatic", "foot"
                ], [
                    "body", "mgBody", "base"
                ], [
                    "bodyFixed", "mgBodyFixed", "body"
                ], [
                    "bodyFixed2", "mgBodyFixed2", "bodyFixed"
                ], [
                    "bodyStatic", "mgBodyStatic", "body"
                ]
            ];
        this.parentDimensions = {
            x: this.element.offsetWidth,
            y: this.element.offsetHeight
        };
        this.docFrag          = v.createDocumentFragment();
        for (var t = 0, u; u = s[t]; t++) {
            (this[u[0]] = v.createElement("DIV")).className = u[1];
            this[u[2]].appendChild(this[u[0]])
        }
        if (this.options.allowGridResize) {
            (this.baseResize = v.createElement("DIV")).className = "mgBaseResize";
            this.base.appendChild(this.baseResize)
        }
    };
    q.addEvents                        = function () {
        var s;
        if (this.options.fixedCols > 0 && !this.usesTouch && !i) {
            try {
                s = (WheelEvent("wheel")) ? "wheel" : g
            } catch (t) {
                s = (l.onmousewheel !== g) ? "mousewheel" : "DOMMouseScroll"
            }
            if (s) {
                n(this.bodyFixed, s, r(this.simulateMouseScroll, this))
            }
        }
        if (this.options.allowGridResize) {
            n(this.baseResize, this.startEvt, r(this.initResizeGrid, this))
        }
        if (this.options.allowColumnResize || this.options.allowClientSideSorting) {
            n(this.head, this.startEvt, r(this.delegateHeaderEvent, this))
        }
        if (this.options.allowSelections) {
            n(this.body, this.startEvt, r(this.selectRange, this));
            if (this.options.showSelectionColumn) {
                n(this.body, "click", r(this.preventSelectionInputStateChange, this))
            }
        }
    };
    q.convertDomDataToJsonData         = function (v) {
        var z = {
                thead: "Head",
                tbody: "Body",
                tfoot: "Foot"
            },
            y,
            D,
            C,
            B,
            w,
            x,
            u,
            t,
            s,
            A = {};
        if (((v || {}).tagName || "").toLowerCase() === "table") {
            for (u = 0, t = 0, D = v.rows; C = D[u]; u++) {
                if (C.sectionRowIndex === 0 && (y = z[C.parentNode.tagName.toLowerCase()])) {
                    A[y] = w = (A[y] || []);
                    t    = w.length
                }
                w[t++] = x = [];
                s      = (B = C.cells).length;
                while (s) {
                    x[--s] = B[s].innerHTML
                }
            }
        }
        return A
    };
    q.convertXmlDataToJsonData         = function (J) {
        var A = {
                thead: "Head",
                tbody: "Body",
                tfoot: "Foot"
            },
            t = (i < 9) ? "text" : "textContent",
            C,
            D,
            y,
            z,
            x,
            v,
            u,
            K,
            B,
            F,
            E,
            s,
            w,
            H,
            I,
            G = {};
        if ((C = (J.getElementsByTagName("table")[0] || {}).childNodes)) {
            for (B = 0; D = C[B]; B++) {
                if ((y = A[D.nodeName]) && (z = D.childNodes)) {
                    G[y] = s = (G[y] || []);
                    H    = s.length;
                    for (F = 0; x = z[F]; F++) {
                        if (x.nodeName === "tr" && (v = x.childNodes)) {
                            s[H++] = w = [];
                            I      = 0;
                            for (E = 0; u = v[E]; E++) {
                                if ((K = u.nodeName) === "td" || K === "th") {
                                    w[I++] = u[t] || ""
                                }
                            }
                        }
                    }
                }
            }
        }
        return G
    };
    q.convertData                      = function (w) {
        var v,
            x,
            t,
            s,
            u;
        this.addSelectionColumn(w);
        this.rawData = w.Body || [];
        if ((v = w.Head || w.Body || w.Foot || null)) {
            x = this.columns = v[0].length;
            t = this.cellData.head;
            s = this.cellData.body;
            u = this.cellData.foot;
            while (x) {
                t[--x] = [];
                s[x]   = [];
                u[x]   = []
            }
            x = this.columns;
            if (w.Head) {
                this.convertDataItem(t, w.Head, "<DIV class='mgC mgHR mgR", x, this.options.allowColumnResize)
            } else {
                this.css.rules[".mgHead"] = {
                    display: "none"
                }
            }
            if (w.Body) {
                this.convertDataItem(s, w.Body, "<DIV class='mgC mgBR mgR", x, false)
            } else {
                this.css.rules[".mgBodyFixed"] = {
                    display: "none"
                }
            }
            if (w.Foot) {
                this.convertDataItem(u, w.Foot, "<DIV class='mgC mgFR mgR", x, false)
            } else {
                this.css.rules[".mgFoot"] = {
                    display: "none"
                }
            }
        }
    };
    q.convertDataItem                  = function (x, A, w, y, t) {
        var s = A.length,
            u,
            z,
            v;
        while (s) {
            u = w + (--s) + "'>";
            z = A[s];
            v = y;
            while (v) {
                x[--v][s] = u + (z[v] || "&nbsp;")
            }
        }
        if (t && (s = A.length)) {
            v = y;
            while (v) {
                x[--v][0] = ("<SPAN class='mgRS mgRS" + v + "'>&nbsp;</SPAN>") + x[v][0]
            }
        }
    };
    q.addSelectionColumn               = function (v) {
        var t,
            u,
            s;
        if (this.options.showSelectionColumn) {
            this.options.colBGColors.unshift(this.options.colBGColors[0] || "");
            this.options.colSortTypes.unshift("none");
            this.options.colAlign.unshift("left");
            if (!this.usesTouch) {
                this.options.fixedCols++
            }
            if ((u = v.Head) && (s = u.length)) {
                while (s) {
                    u[--s].unshift("")
                }
            }
            if ((u = v.Body) && (s = u.length)) {
                t = "<LABEL class=mgSH><INPUT tabIndex='-1' type=";
                t += ((this.options.allowMultipleSelections) ? "checkbox class=mgCb" : "radio  class=mgRd");
                t += ">&nbsp;</LABEL>";
                while (s) {
                    u[--s].unshift(t)
                }
            }
            if ((u = v.Foot) && (s = u.length)) {
                while (s) {
                    u[--s].unshift("")
                }
            }
        }
    };
    q.generateGrid                     = function () {
        this.hasHead       = ((this.cellData.head[0] || []).length > 0);
        this.hasBody       = ((this.cellData.body[0] || []).length > 0);
        this.hasFoot       = ((this.cellData.foot[0] || []).length > 0);
        this.hasHeadOrFoot = (this.hasHead || this.hasFoot);
        this.hasFixedCols  = (this.options.fixedCols > 0);
        this.generateGridHead();
        this.generateGridBody();
        this.generateGridFoot()
    };
    q.generateGridHead                 = function () {
        var s;
        if (this.hasHead) {
            s                         = this.generateGridSection(this.cellData.head);
            this.headStatic.innerHTML = s.fullHTML;
            if (this.hasFixedCols) {
                this.headFixed.innerHTML = s.fixedHTML
            }
        }
    };
    q.generateGridBody                 = function () {
        var s;
        if (this.hasBody) {
            s                         = this.generateGridSection(this.cellData.body);
            this.bodyStatic.innerHTML = s.fullHTML;
            if (this.hasFixedCols) {
                this.bodyFixed2.innerHTML = s.fixedHTML
            }
        } else {
            this.bodyStatic.innerHTML = "<DIV class='mgEmptySetMsg'>No results returned.</DIV>"
        }
    };
    q.generateGridFoot                 = function () {
        var s;
        if (this.hasFoot) {
            s                         = this.generateGridSection(this.cellData.foot);
            this.footStatic.innerHTML = s.fullHTML;
            if (this.hasFixedCols) {
                this.footFixed.innerHTML = s.fixedHTML
            }
        }
    };
    q.generateGridSection              = function (t) {
        var w = function (z, A) {
                return t[parseInt(A, 10)].join("</DIV>")
            },
            v = /@(\d+)@/g,
            y = this.options.fixedCols,
            s = [],
            u = [],
            x = t.length;
        while (x) {
            if ((--x) < y) {
                s[x] = "<DIV class='mgCl mgCl" + x + " mgFCl'>@" + x + "@</DIV></DIV>";
                u[x] = "<DIV class='mgCl mgCl" + x + " mgFCl'></DIV>"
            } else {
                u[x] = "<DIV class='mgCl mgCl" + x + "'>@" + x + "@</DIV></DIV>"
            }
        }
        return {
            fixedHTML: (y) ? s.join("").replace(v, w) : "",
            fullHTML : u.join("").replace(v, w)
        }
    };
    q.displayGrid                      = function () {
        var t = this.options.srcType,
            v = this.options.srcData,
            s = false;
        this.lastScrollLeft = 0;
        this.lastScrollTop  = 0;
        this.body.onscroll  = r(this.syncScrolls, this);
        try {
            this.css.sheet.parentNode.removeChild(this.css.sheet)
        } catch (u) {
            (this.css.sheet = l.createElement("STYLE")).id = this.element.id + "SS";
            this.css.sheet.type                            = "text/css"
        }
        if (t === "dom" && (v = (typeof(v) === "string") ? e(v) : v)) {
            if ((s = (this.element === v.parentNode))) {
                this.element.replaceChild(this.docFrag, v)
            }
        }
        if (!s) {
            this.element.appendChild(this.docFrag)
        }
        this.alignTimer = h.setTimeout(r(this.alignColumns, this, false, true), 16)
    };
    q.alignColumns                     = function (x, fromInit) {
        var u = [this.headStatic.children || [],
                this.bodyStatic.children || [],
                this.footStatic.children || []],
            w = [this.headFixed.children || [],
                this.bodyFixed2.children || [],
                this.footFixed.children || []],
            s = this.options.allowColumnResize,
            v = this.options.colBGColors,
            C = this.options.colAlign,
            B = this.options.fixedCols,
            D = this.css.rules,
            z,
            t;
        if (x !== true) {
            this.computeBaseStyles()
        } else {
            for (var y = 0, A = this.columns; y < A; y++) {
                delete D[".mgCl" + y].width
            }
            this.setRules()
        }
        this.columnWidths = [];
        for (var y = 0, A = this.columns; y < A; y++) {
            t                   = (y < B) ? w : u;
            z                   = Math.max((t[0][y] || {}).offsetWidth || 0, (t[1][y] || {}).offsetWidth || 0, (t[2][y] || {}).offsetWidth || 0);
            this.columnWidths[y] = z;
            D[".mgCl" + y]      = {
                width       : z + "px",
                "text-align": (C[y] || "left")
            };
            if ((v[y] || "#ffffff") !== "#ffffff") {
                D[".mgCl" + y]["background-color"] = v[y]
            }
            if (s) {
                D[".mgRS" + y] = {
                    "margin-left": (z - 2) + "px"
                }
            }
        }
        this.setRules();
        if (fromInit === true) {
            this.options.onLoad.call(this);
        }
    };
    q.computeBaseStyles                = function () {
        var v = this.css.rules,
            u = (this.hasHead) ? this.head.offsetHeight : 0,
            t = (this.hasFoot) ? this.foot.offsetHeight : 0,
            s = {
                x: this.body.offsetWidth - this.body.clientWidth,
                y: this.body.offsetHeight - this.body.clientHeight
            };
        var styleParent = "#" + this.element.id + " "; // patched.
        v[styleParent + ".mgC"]          = {
            visibility: "visible"
        };
        v[styleParent + ".mgCl"]         = {
            "background-color": "#fff"
        };
        v[styleParent + ".mgBodyStatic"] = {
            padding: u + "px 0px " + t + "px 0px"
        };
        if (this.hasHead) {
            v[styleParent + ".mgHead"] = {
                right: s.x + "px"
            }
        }
        if (this.hasFoot) {
            v[styleParent + ".mgFoot"] = {
                bottom: s.y + "px",
                right : s.x + "px"
            }
        }
        if (this.hasFixedCols) {
            v[styleParent + ".mgBodyFixed" + ((i < 8) ? "2" : "")] = {
                top   : u + "px",
                bottom: s.y + "px"
            }
        }
        if (this.options.allowGridResize) {
            v[styleParent + ".mgBaseResize"] = {
                width : s.x + "px",
                height: s.y + "px"
            }
        }
        if (this.options.allowColumnResize) {
            v[styleParent + ".mgResizeDragger"] = {
                bottom: s.y + "px"
            };
            v[styleParent + ".mgRS"]            = {
                display        : "block",
                position       : "relative",
                "margin-bottom": (u * -1) + "px",
                height         : u + "px"
            }
        }
    };
    q.syncScrolls                      = function (t) {
        var u = (this.hasHeadOrFoot) ? this.body.scrollLeft : 0,
            s = (this.hasFixedCols) ? this.body.scrollTop : 0;
        if (u !== this.lastScrollLeft) {
            this.lastScrollLeft = u;
            if (this.hasHead) {
                this.headStatic.style.marginLeft = (-1 * u) + "px"
            }
            if (this.hasFoot) {
                this.footStatic.style.marginLeft = (-1 * u) + "px"
            }
        }
        if (s !== this.lastScrollTop) {
            this.lastScrollTop              = s;
            this.bodyFixed2.style.marginTop = (-1 * s) + "px"
        }
    };
    q.simulateMouseScroll              = function (t) {
        var t = t || h.event,
            s = 0;
        if (t.deltaY !== g) {
            s = t.deltaY
        } else {
            if (t.wheelDelta !== g) {
                s = t.wheelDelta * (-1 / 40)
            } else {
                if (t.detail !== g) {
                    s = t.detail
                }
            }
        }
        this.body.scrollTop += (s * 33);
        this.syncScrolls()
    };
    q.setRules                         = function () {
        var u = (this.options.supportMultipleGridsInView) ? this.css.idRulePrefix : "",
            v = Object.prototype.hasOwnProperty,
            B = this.css.rules,
            w = this.css.sheet,
            t = [],
            x = 0,
            z,
            y,
            s,
            A = l;
        for (z in B) {
            if (v.call(B, z) && (y = B[z])) {
                t[x++] = u + z + "{";
                for (s in y) {
                    if (v.call(y, s)) {
                        t[x++] = s + ":" + y[s] + ";"
                    }
                }
                t[x++] = "} "
            }
        }
        if (!w.styleSheet) {
            w.appendChild(A.createTextNode(t.join("")))
        }
        if (!e(w.id)) {
            (A.head || A.getElementsByTagName("head")[0]).appendChild(w)
        }
        if (w.styleSheet) {
            w.styleSheet.cssText = t.join("")
        }
    };
    q.initResizeGrid                   = function (t) {
        var t = t || h.event,
            s;
        if (t.button !== 2 && this.options.allowGridResize) {
            s        = b(t, "page");
            this.tmp = {
                throttle    : -1,
                origX       : s.x,
                origY       : s.y,
                origWidth   : this.parentDimensions.x,
                origHeight  : this.parentDimensions.y,
                boundMoveEvt: r(this.resizeGrid, this),
                boundEndEvt : r(this.endResizeGrid, this)
            };
            n(l, this.moveEvt, this.tmp.boundMoveEvt);
            n(l, this.endEvt, this.tmp.boundEndEvt);
            return p(t)
        }
    };
    q.resizeGrid                       = function (y) {
        var w,
            v,
            s,
            x,
            t,
            u;
        if ((this.tmp.throttle++) & 1) {
            w                     = b(y || h.event, "page");
            v                     = w.x - this.tmp.origX;
            s                     = w.y - this.tmp.origY;
            x                     = Math.max(60, (v > 0) ? this.tmp.origWidth + v : this.tmp.origWidth - Math.abs(v));
            t                     = Math.max(30, (s > 0) ? this.tmp.origHeight + s : this.tmp.origHeight - Math.abs(s));
            u                     = this.element.style;
            u.width               = x + "px";
            u.height              = t + "px";
            this.parentDimensions = {
                x: x,
                y: t
            };
            this.syncScrolls();
            d();
            this.options.onResizeGrid.apply(this, [
                x, t
            ])
        }
    };
    q.endResizeGrid                    = function (s) {
        o(l, this.moveEvt, this.tmp.boundMoveEvt);
        o(l, this.endEvt, this.tmp.boundEndEvt);
        this.options.onResizeGridEnd.apply(this, [
            this.parentDimensions.x, this.parentDimensions.y
        ]);
        this.tmp = g
    };
    q.delegateHeaderEvent              = function (t) {
        var t = t || h.event,
            u = t.target || t.srcElement,
            s = u.className || "";
        if (t.button !== 2) {
            if (this.options.allowColumnResize && s.indexOf("mgRS") > -1) {
                return this.initResizeColumn(t, u, s)
            } else {
                if (this.hasBody && this.options.allowClientSideSorting) {
                    while (s.indexOf("mgCl") === -1 && s !== "mgHead") {
                        s = (u = u.parentNode).className || ""
                    }
                    if (s.indexOf("mgCl") > -1) {
                        this.sortColumn(parseInt(/mgCl(\d+)/.exec(s)[1], 10))
                    }
                }
            }
        }
    };
    q.initResizeColumn                 = function (t, v, s) {
        var w = parseInt(s.replace(/mgRS/g, ""), 10),
            u = l;
        this.tmp                    = {
            lastLeft    : -1,
            colIdx      : w,
            origX       : b(t, "client").x,
            origWidth   : this.columnWidths[w],
            origLeft    : v.offsetLeft,
            boundMoveEvt: r(this.resizeColumn, this),
            boundEndEvt : r(this.endResizeColumn, this),
            dragger     : u.createElement("DIV")
        };
        this.tmp.dragger.className  = "mgResizeDragger";
        this.tmp.dragger.style.left = this.tmp.origLeft + "px";
        this.base.insertBefore(this.tmp.dragger, this.base.firstChild);
        n(u, this.moveEvt, this.tmp.boundMoveEvt);
        n(u, this.endEvt, this.tmp.boundEndEvt);
        return p(t)
    };
    q.resizeColumn                     = function (w) {
        var v = b(w || h.event, "client").x,
            s = v - this.tmp.origX,
            u = Math.max(15, (s > 0) ? this.tmp.origWidth + s : this.tmp.origWidth - Math.abs(s)),
            t = (s > 0) ? this.tmp.origLeft + s : this.tmp.origLeft - Math.abs(s);
        this.tmp.newWidth = u;
        if (this.tmp.lastLeft !== t && u > 15) {
            this.tmp.dragger.style.left = t + "px";
            this.tmp.lastLeft           = t
        }
        d();
        this.options.onResizeColumn.apply(this, [
            this.tmp.colIdx, u
        ])
    };
    q.endResizeColumn                  = function (t) {
        var s = this.tmp.newWidth || this.tmp.origWidth,
            u = this.tmp.colIdx;
        o(l, this.moveEvt, this.tmp.boundMoveEvt);
        o(l, this.endEvt, this.tmp.boundEndEvt);
        this.tmp.dragger.parentNode.removeChild(this.tmp.dragger);
        this.css.rules[".mgCl" + u]["width"]       = s + "px";
        this.css.rules[".mgRS" + u]["margin-left"] = (s - 2) + "px";
        this.columnWidths[u]                        = s;
        this.setRules();
        this.syncScrolls();
        this.options.onResizeColumnEnd.apply(this, [
            u, s
        ]);
        this.tmp = g
    };
    q.sortColumn                       = function (v, t) {
        var v = (!isNaN(v || -1)) ? v || -1 : -1,
            u = (v > -1) ? this.options.colSortTypes[v] || "string" : "none",
            s = this.lastSortedColumn;
        if (u !== "none") {
            t = (t === g) ? ((v === s[0]) ? !s[1] : true) : !!t;
            this.sortRawData(v, u, t)
        }
    };
    q.sortRawData                      = function (x, v, w) {
        var C,
            A,
            t,
            y,
            s = this.rawData,
            B = [],
            u = [],
            z = this;
        y = s.length;
        while (y) {
            s[--y].pIdx = y
        }
        A = (w) ? -1 : 1;
        t = (w) ? 1 : -1;
        s.sort(function (E, D) {
            return z.getSortResult(v, x, A, t, E[x], D[x])
        });
        this.convertDataItem(this.cellData.body, s, "<DIV class='mgC mgBR mgR", this.columns, false);
        this.generateGridBody();
        y = s.length;
        while (y) {
            u[--y] = s[y].pIdx
        }
        if (this.options.allowSelections && (C = this.selectedIndexes.concat()).length) {
            y = C.length;
            while (y) {
                B[--y] = c(u, C[y])
            }
            this.highlightRows((this.selectedIndexes = B), [])
        }
        this.options.onColumnSort.apply(this, [
            u.concat(), x, this.lastSortedColumn[0]
        ]);
        this.lastSortedColumn = [
            x, w
        ]
    };
    q.getSortResult                    = function (x, z, y, u, w, t, v, s) {
        if (w === t) {
            return 0
        }
        if (this.sortCache[(v = x + "_" + w)] === g) {
            this.sortCache[v] = (x === "string") ? w : (x === "number") ? parseFloat(w) || -Infinity : (x === "date") ? new Date(w).getTime() || -Infinity : (x === "custom") ? this.options.customSortCleaner(w, z) : w
        }
        if (this.sortCache[(s = x + "_" + t)] === g) {
            this.sortCache[s] = (x === "string") ? t : (x === "number") ? parseFloat(t) || -Infinity : (x === "date") ? new Date(t).getTime() || -Infinity : (x === "custom") ? this.options.customSortCleaner(t, z) : t
        }
        return (this.sortCache[v] < this.sortCache[s]) ? y : u
    };
    q.toggleSelectAll                  = function (s) {
        var w = this.selectedIndexes,
            v = [],
            u = [],
            t;
        if (this.hasBody && this.options.allowSelections) {
            if (s) {
                v = [0];
                if (this.options.allowMultipleSelections) {
                    t = this.rawData.length;
                    while (t) {
                        v[--t] = t
                    }
                }
                this.selectIndexes(v)
            } else {
                if (w.length) {
                    u                    = w.concat();
                    this.selectedIndexes = [];
                    this.highlightRows(v, u);
                    this.options.onRowSelect.apply(this, [
                        v, u, -1
                    ])
                }
            }
        }
    };
    q.selectIndexes                    = function (x) {
        var w = this.selectedIndexes,
            v = [],
            u = [],
            t = x.length,
            s = 0;
        if (t && this.hasBody && this.options.allowSelections) {
            if (this.options.allowMultipleSelections) {
                while (t) {
                    if (c(w, x[--t]) === -1) {
                        v[s++] = x[t]
                    }
                }
            } else {
                u    = w.concat();
                v[0] = x[0];
                w    = []
            }
            this.selectedIndexes = w.concat(v);
            this.highlightRows(v, u);
            this.options.onRowSelect.apply(this, [
                v, u, -1
            ])
        }
    };
    q.selectRange                      = function (v) {
        var v = v || h.event,
            w = v.target || v.srcElement,
            u,
            s,
            x,
            y,
            t;
        if (v.button !== 2 && this.options.allowSelections) {
            u = w.className || "";
            while (u.indexOf("mgBR") === -1 && u !== "mgBody") {
                u = (w = w.parentNode).className || ""
            }
            if (u.indexOf("mgBR") > -1) {
                y = true;
                t = parseInt(/mgR(\d+)/.exec(u)[1], 10);
                u = (w = w.parentNode).className || "";
                s = (this.options.showSelectionColumn && (u.indexOf("mgCl0") > -1));
                x = this.usesTouch || s;
                if (this.usesTouch && this.options.showSelectionColumn && (y = s)) {
                    p(v)
                }
                if (y) {
                    this.updateSelectedIndexes(t, v.ctrlKey || x, v.shiftKey)
                }
            }
        }
    };
    q.updateSelectedIndexes            = function (t, A, u) {
        var B = this.selectedIndexes.concat(),
            C = (c(B, t) > -1),
            x = [],
            s = [],
            z,
            w,
            v,
            y;
        if (!this.options.allowMultipleSelections || !B.length || (!A && !u)) {
            x = (C && B.length === 1) ? [] : [t];
            s = B.concat()
        } else {
            if (A) {
                x = C ? [] : [t];
                s = C ? [t] : []
            } else {
                if (u) {
                    if ((z = B[0]) <= t) {
                        for (w = z + 1, v = 0; w <= t; w++) {
                            if (c(B, w) === -1) {
                                x[v++] = w
                            }
                        }
                    } else {
                        for (w = z - 1, v = 0; w >= t; w--) {
                            if (c(B, w) === -1) {
                                x[v++] = w
                            }
                        }
                    }
                }
            }
        }
        for (w = 0, y = s.length; w < y; w++) {
            if ((v = c(B, s[w])) > -1) {
                B.splice(v, 1)
            }
        }
        this.selectedIndexes = B.concat(x);
        this.highlightRows(x, s);
        if (A || u) {
            (!i) ? d() : h.setTimeout(d, 25)
        }
        this.options.onRowSelect.apply(this, [
            x, s, t
        ])
    };
    q.highlightRows                    = function (x, s) {
        var t = [
                this.bodyFixed2.children, this.bodyStatic.children
            ],
            u = this.options.fixedSelectedBgColor,
            C = this.options.selectedBgColor,
            z = this.options.fixedCols,
            w = this.columns,
            A,
            B,
            y,
            v;
        while (w) {
            B = (((--w) < z) ? t[0] : t[1])[w].children;
            A = (w < z) ? u : C;
            v = s.length;
            while (v) {
                B[s[--v]].style.backgroundColor = ""
            }
            v = x.length;
            while (v) {
                B[x[--v]].style.backgroundColor = A
            }
        }
        if (this.options.showSelectionColumn) {
            y = t[(!this.usesTouch) ? 0 : 1][0].getElementsByTagName("INPUT");
            v = s.length;
            while (v) {
                y[s[--v]].checked = false
            }
            v = x.length;
            while (v) {
                y[x[--v]].checked = true
            }
        }
    };
    q.preventSelectionInputStateChange = function (u) {
        var u = u || h.event,
            v = u.target || u.srcElement,
            t = v.className || "",
            s;
        if (u.button !== 2) {
            if (t.indexOf("mgCb") > -1 || t.indexOf("mgRd") > -1) {
                do {
                    t = (v = v.parentNode).className || ""
                } while (t.indexOf("mgBR") === -1 && t !== "mgBody");
                if (t.indexOf("mgBR") > -1) {
                    s = parseInt(/mgR(\d+)/.exec(t)[1], 10);
                    (u.target || u.srcElement).checked = (c(this.selectedIndexes, s) > -1)
                }
            }
        }
    };
    q.cleanUp                          = function () {
        this.alignTimer        = (this.alignTimer) ? h.clearTimeout(this.alignTimer) : null;
        this.element.innerHTML = "";
        try {
            this.css.sheet.parentNode.removeChild(this.css.sheet)
        } catch (s) {}
        return null
    };
    var k = function () {
            var t,
                s;
            if ((t = navigator).appName === "Microsoft Internet Explorer") {
                if (new RegExp("MSIE ([0-9]{1,}[.0-9]{0,})").exec(t.userAgent)) {
                    s = parseFloat(RegExp.$1)
                }
            }
            return (s > 5) ? s : g
        };
    var a = function (u) {
            var t,
                s,
                v;
            if ((t = typeof(u)) === "string") {
                if (((v = h).JSON || {}).parse) {
                    s = v.JSON.parse(u)
                } else {
                    s = (function () {
                        try {
                            return (new Function("return " + u))()
                        } catch (w) {
                            return
                        }
                    })()
                }
            }
            return s || (t === "object" && (s = u)) || null
        };
    var j = function (u) {
            var t,
                v,
                s;
            if ((t = typeof(u)) === "string") {
                if (h.DOMParser) {
                    s = new DOMParser().parseFromString(u, "text/xml")
                } else {
                    if (h.ActiveXObject) {
                        s       = new ActiveXObject("Microsoft.XMLDOM");
                        s.async = false;
                        s.loadXML(u)
                    }
                }
            } else {
                if (t === "object") {
                    v = (u.ownerDocument || u).documentElement || {};
                    if (v.nodeName && v.nodeName.toUpperCase() !== "HTML") {
                        s = u
                    }
                }
            }
            return s || null
        };
    var n = (l.addEventListener) ? function (t, s, u) {
            t.addEventListener(s, u, false)
        } : function (t, s, u) {
            t.attachEvent("on" + s, u)
        };
    var p = function (s) {
            if (s.stopPropagation) {
                s.stopPropagation();
                s.preventDefault()
            } else {
                s.returnValue  = false;
                s.cancelBubble = true
            }
            return false
        };
    var o = (l.addEventListener) ? function (t, s, u) {
            t.removeEventListener(s, u, false)
        } : function (t, s, u) {
            t.detachEvent("on" + s, u)
        };
    var b = function (w, u) {
            var t = w.pageX,
                s = w.pageY,
                x,
                v;
            if (u === "client") {
                if (t !== g || s !== g) {
                    return {
                        x: t - h.pageXOffset,
                        y: s - h.pageYOffset
                    }
                }
                return {
                    x: w.clientX,
                    y: w.clientY
                }
            }
            if (t === g || s === g) {
                v = ((x = l).documentElement.scrollLeft !== g) ? x.documentElement : x.body;
                return {
                    x: w.clientX + v.scrollLeft,
                    y: w.clientY + v.scrollTop
                }
            }
            return {
                x: t,
                y: s
            }
        };
    var r = function (u, t) {
            var s = m.call(arguments, 2);
            return function () {
                return u.apply(t, s.concat(m.call(arguments)))
            }
        };
    var c = ([].indexOf) ? function (s, t) {
            return s.indexOf(t)
        } : function (t, v) {
            for (var u = 0, s = t.length; u < s; u++) {
                if (t[u] === v) {
                    return u
                }
            }
            return -1
        };
    var d = (h.getSelection) ? function () {
            h.getSelection().removeAllRanges();
            return false
        } : (l.selection) ? function () {
            l.selection.empty();
            return false
        } : function () {
            return false
        };
    var e = function (s) {
            return l.getElementById(s)
        },
        m = Array.prototype.slice,
        i = k();
    h.Grid = f
})(this, this.document);
