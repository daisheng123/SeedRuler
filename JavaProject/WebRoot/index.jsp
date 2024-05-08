<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>SeedRuler</title>
    <meta name="keywords" content="layuimini">
    <meta name="description" content="layuimini">
    <meta name="renderer" content="webkit">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta http-equiv="Access-Control-Allow-Origin" content="*">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="format-detection" content="telephone=no">
    <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">
    <link rel="icon" href="resource/images/favicon.ico">
    <link rel="stylesheet" href="resource/lib/layui-v2.5.5/css/layui.css" media="all">
    <link rel="stylesheet" href="resource/lib/font-awesome-4.7.0/css/font-awesome.min.css" media="all">
    <link rel="stylesheet" href="resource/css/layuimini.css" media="all">
    <link rel="stylesheet" href="resource/css/themes/default.css" media="all">
    <link rel="stylesheet" href="resource/css/public.css" media="all">
    <!--[if lt IE 9]>
    <script src="https://cdn.staticfile.org/html5shiv/r29/html5.min.js"></script>
    <script src="https://cdn.staticfile.org/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->
    <style id="layuimini-bg-color">
    </style>
</head>
<body class="layui-layout-body layuimini-all">
<div class="layui-layout layui-layout-admin">

    <div class="layui-header header">
        <div class="layui-logo layuimini-logo layuimini-back-home"></div>

        <div class="layuimini-header-content">
            <a>
                <div class="layuimini-tool"><i title="unfold" class="fa fa-outdent" data-side-fold="1"></i></div>
            </a>

            <!--电脑端头部菜单-->
            <ul class="layui-nav layui-layout-left layuimini-header-menu layuimini-menu-header-pc layuimini-pc-show">
            </ul>

            <!--手机端头部菜单-->
            <ul class="layui-nav layui-layout-left layuimini-header-menu layuimini-mobile-show">
                <li class="layui-nav-item">
                    <a href="javascript:;"><i class="fa fa-list-ul"></i> Select module</a>
                    <dl class="layui-nav-child layuimini-menu-header-mobile">
                    </dl>
                </li>
            </ul>

            <ul class="layui-nav layui-layout-right">
					

					<li class="layui-nav-item layuimini-setting">
                    <a href="javascript:;" class="home" >HOME</a>
                    <!--  <dl class="layui-nav-child">
                       
                        <dd>
                            <a href="javascript:;" class="login-out">Login out</a>
                        </dd>
                    </dl>-->
                </li>
                <li class="layui-nav-item" lay-unselect layuimini-setting><a href="javascript:;" id="downloads">DOWNLOADS</a></li>
                <li class="layui-nav-item" lay-unselect>
                    <a href="javascript:;" data-refresh="Refresh"><i class="fa fa-refresh"></i></a>
                </li>
                <li class="layui-nav-item" lay-unselect>
                    <a href="javascript:;" data-clear="Clear" class="layuimini-clear"><i class="fa fa-trash-o"></i></a>
                </li>
                <li class="layui-nav-item mobile layui-hide-xs" lay-unselect>
                    <a href="javascript:;" data-check-screen="full"><i class="fa fa-arrows-alt"></i></a>
                </li>
                <li class="layui-nav-item layuimini-select-bgcolor" lay-unselect>
                    <a href="javascript:;" data-bgcolor="Color scheme"><i class="fa fa-ellipsis-v"></i></a>
                </li>
            </ul>
        </div>
    </div>

    <!--无限极左侧菜单-->
    <div class="layui-side layui-bg-black layuimini-menu-left">
    </div>

    <!--初始化加载层-->
    <div class="layuimini-loader">
        <div class="layuimini-loader-inner"></div>
    </div>

    <!--手机端遮罩层-->
    <div class="layuimini-make"></div>

    <!-- 移动导航 -->
    <div class="layuimini-site-mobile"><i class="layui-icon"></i></div>

    <div class="layui-body">

        <div class="layui-card layuimini-page-header layui-hide">
            <div class="layui-breadcrumb layuimini-page-title">
                <a lay-href="" href="/">Home</a><span lay-separator="">/</span>
                <a><cite>General management</cite></a><span lay-separator="">/</span>
                <a><cite>System settings</cite></a>
            </div>
        </div>

        <div class="layuimini-content-page">
        </div>

    </div>

</div>
<script src="resource/lib/layui-v2.5.5/layui.js" charset="utf-8"></script>
<script src="resource/js/lay-config.js" charset="utf-8"></script>
<script>
    layui.use(['jquery', 'layer', 'miniAdmin', 'miniTongji'], function () {
        var $ = layui.jquery,
            layer = layui.layer,
            miniAdmin = layui.miniAdmin,
            miniTongji = layui.miniTongji;

        var options = {
            iniUrl: "resource/api/init.json",    // 初始化接口
            clearUrl: "resource/api/clear.json", // 缓存清理接口
            renderPageVersion: true,    // 初始化页面是否加版本号
            bgColorDefault: false,      // 主题默认配置
            multiModule: true,          // 是否开启多模块
            menuChildOpen: false,       // 是否默认展开菜单
            loadingTime: 0,             // 初始化加载时间
            pageAnim: true,             // 切换菜单动画
        };
        miniAdmin.render(options);

        // 百度统计代码，只统计指定域名
        miniTongji.render({
            specific: true,
            domains: [
                '99php.cn',
                'layuimini.99php.cn',
                'layuimini-onepage.99php.cn',
            ],
        });

        $('.home').on("click", function () {
            layer.msg('login out Successfully', function () {
                window.location = 'https://u263790-ad15-4e65cb7d.westc.gpuhub.com:8443/IMSFGM/ ';
            });
        });
         $('#downloads').on("click", function () {
              window.location = 'https://u263790-ad15-4e65cb7d.westc.gpuhub.com:8443/IMSFGM/home.jsp#/resource/page/statistics-germinate.html';
        });
    });
</script>
</body>
</html>
