"use strict";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var CELL_SIZE = 8;

/* global $ */

var Main = function () {
    function Main(width, height) {
        _classCallCheck(this, Main);

        this.cell_size = CELL_SIZE;
        this.width = width;
        this.height = height;

        this.smallerTime = 3;

        this.canvas = document.getElementById("main");
        this.input = document.getElementById("input");
        this.canvas.width = width * this.cell_size + 1;
        this.canvas.height = height * this.cell_size + 1;

        this.input.width = Math.floor(this.canvas.width / this.smallerTime);
        this.input.height = Math.floor(this.canvas.height / this.smallerTime);

        this.ctx = this.canvas.getContext("2d");
        this.canvas.addEventListener("mousedown", this.onMouseDown.bind(this));
        this.canvas.addEventListener("mouseup", this.onMouseUp.bind(this));
        this.canvas.addEventListener("mousemove", this.onMouseMove.bind(this));
        this.initialize();
    }

    _createClass(Main, [{
        key: "initialize",
        value: function initialize() {
            this.ctx.fillStyle = "#FFFFFF";
            this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
            this.ctx.lineWidth = 1;
            this.ctx.strokeRect(0, 0, this.canvas.width, this.canvas.height);
            this.ctx.lineWidth = 0.05;

            for (var i = 0; i < this.width; i++) {
                this.ctx.beginPath();
                this.ctx.moveTo((i + 1) * this.cell_size, 0);
                this.ctx.lineTo((i + 1) * this.cell_size, this.canvas.height);
                this.ctx.closePath();
                this.ctx.stroke();
            }

            for (var _i = 0; _i < this.height; _i++) {
                this.ctx.beginPath();
                this.ctx.moveTo(0, (_i + 1) * this.cell_size);
                this.ctx.lineTo(this.canvas.width, (_i + 1) * this.cell_size);
                this.ctx.closePath();
                this.ctx.stroke();
            }

            this.drawInput();
            $("#output td").text("").removeClass("success");
        }
    }, {
        key: "onMouseDown",
        value: function onMouseDown(e) {
            this.canvas.style.cursor = "default";
            this.drawing = true;
            this.prev = this.getPosition(e.clientX, e.clientY);
        }
    }, {
        key: "onMouseUp",
        value: function onMouseUp() {
            this.drawing = false;
            this.drawInput();
        }
    }, {
        key: "onMouseMove",
        value: function onMouseMove(e) {
            if (this.drawing) {
                var curr = this.getPosition(e.clientX, e.clientY);
                this.ctx.lineWidth = this.cell_size >> 1;
                this.ctx.lineCap = "round";
                this.ctx.beginPath();
                this.ctx.moveTo(this.prev.x, this.prev.y);
                this.ctx.lineTo(curr.x, curr.y);
                this.ctx.stroke();
                this.ctx.closePath();
                this.prev = curr;
            }
        }
    }, {
        key: "getPosition",
        value: function getPosition(clientX, clientY) {
            var rect = this.canvas.getBoundingClientRect();
            return {
                x: clientX - rect.left,
                y: clientY - rect.top
            };
        }
    }, {
        key: "drawInput",
        value: function drawInput() {
            var ctx = this.input.getContext("2d");

            ctx.drawImage(this.canvas, 0, 0, this.canvas.width, this.canvas.height, 0, 0, this.input.width, this.input.height);

            var imageData = ctx.getImageData(0, 0, this.input.width, this.input.height);
            var dataArr = Main.toGrayScale(imageData);

            $.ajax({
                url: "/api/sr",
                method: "POST",
                contentType: "application/json",
                data: JSON.stringify(dataArr),
                success: function success(data) {
                    console.log(data);
                    $("#prediction").text(data);
                }
            });
        }
    }], [{
        key: "toGrayScale",
        value: function toGrayScale(imageData) {
            var dataArr = [];
            for (var i = 0; i < imageData.height; i++) {
                var rowArr = [];
                for (var j = 0; j < imageData.width; j++) {
                    var startPoint = (i * imageData.width + j) * 4;
                    var brightness = this.RGBToGrayScale(imageData.data[startPoint], imageData.data[startPoint + 1], imageData.data[startPoint + 2]);
                    rowArr.push(brightness);
                }
                dataArr.push(rowArr);
            }
            return dataArr;
        }
    }, {
        key: "RGBToGrayScale",
        value: function RGBToGrayScale(r, g, b) {
            return 0.299 * r + 0.587 * g + 0.114 * b;
        }
    }]);

    return Main;
}();

$(function () {
    var containerWidth = $("#main").parent().width();

    console.log(Math.floor(containerWidth / CELL_SIZE));
    var main = new Main(Math.floor(containerWidth / CELL_SIZE), 32);
    $("#clear").click(function () {
        main.initialize();
    });
});