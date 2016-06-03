// fec.js
//
// The main entrypoint for fec-eregs specific javascript.

var SiteNav = require('fec-style/js/site-nav').SiteNav;

var $ = window.$;
$(function () {
  $('.js-site-nav').each(function () {
    //TODO enable menus once the breakpoint overflow is fixed
    //new SiteNav(this);
  });
});
