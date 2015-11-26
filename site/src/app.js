/*
 Copyright 2015 SSO Project
 */


var Bootstrap = require("bootstrap");

$(document).ready(function () {
    var environ = {
        user: null,
        title: "Luna 统一身份认证",
        url: "http://127.0.0.1:3001",
        sso_service: "http://139.196.37.224:8001",
        dash: "#dashboard",
        token: $.cookie("Authorization")
    };

    var services = {
        docmanage: {
            name: "文档中心",
            url: "http://139.196.37.224/docloud/docmanage.html",
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
            load_user($.cherry.environ.token);
            $("#nav").switch_page("#nav-page", {});
        },
        logout: function() {
            $.removeCookie("Authorization");
            $.cherry.switch_page("#login-form");
            $.cherry.environ.user = null;
            $("#nav").switch_page("#nav-page", {});
        },
        error: function (data) {
            $($.cherry.environ.dash).switch_page("#error-page", data.responseJSON);
        }
    };

    var load_user = function (token) {
        return $.ajax({
            url: environ.sso_service + '/sso/user',
            type: "get",
            async: false,
            headers: {
                Authorization: token
            }
        }).done(function (data) {
            $.cherry.environ.user = data;
        }).error(function (data) {
            $.cherry.switch_page("#login-form");
        });
    };

    $.cherry.setup(environ, state);

    if ($.cherry.environ.token == undefined) {
        $.cherry.switch_page("#login-form");
        $("#nav").switch_page("#nav-page", {});
    } else {
        $($.cherry.environ.dash).switch_page("#auth-page", {services: services});
        load_user($.cherry.environ.token);
        $("#nav").switch_page("#nav-page", {});
    }
});
