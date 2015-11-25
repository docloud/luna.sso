/*
 Copyright 2015 SSO Project
 */


var Bootstrap = require("bootstrap");

$(document).ready(function () {
    var environ = {
        user: null,
        title: "Luna 统一身份认证",
        url: "http://127.0.0.1:8001",
        dash: "#dashboard",
        token: $.cookie("Authorization")
    };

    var services = {
        docmanage: {
            name: "文档中心",
            url: "http://127.0.0.1:3002/docmanage.html",
            logo: "http://7xj20w.com1.z0.glb.clouddn.com/images/doc_alpha.svg",
            description: "文档中心"
        }
    };

    var state = {
        login_success: function (data) {
            $.cherry.environ.token = data.token;
            console.log(data.token);
            $.cookie("Authorization", data.token);
            $($.cherry.environ.dash).switch_page("#auth-page", {services: services});
        },
        logout: function() {
            $.removeCookie("Authorization");
            $.cherry.switch_page("#login-form");
        },
        error: function (data) {
            $($.cherry.environ.dash).switch_page("#error-page", data.responseJSON);
        }
    };

    $.cherry.setup(environ, state);
    $("#nav").switch_page("#nav-page", {});

    if ($.cherry.environ.token == undefined) {
        $.cherry.switch_page("#login-form");
    } else {
        $($.cherry.environ.dash).switch_page("#auth-page", {services: services});
        $.sso.load_user($.cherry.environ.token);
        $.cherry.environ.user = $.sso.user;
        $("#nav").switch_page("#nav-page", {});
    }
});
