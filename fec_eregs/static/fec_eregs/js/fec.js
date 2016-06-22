// fec.js
//
// The main entrypoint for fec-eregs specific javascript.

var helpers = require('fec-style/js/helpers');
var SiteNav = require('fec-style/js/site-nav').SiteNav;

// Override the breakpoints
helpers.BREAKPOINTS.MEDIUM = 720;
helpers.BREAKPOINTS.LARGE = 720;

var $ = window.$;
$(function () {
  $('.js-site-nav').each(function () {
    new SiteNav(this);
  });
});
