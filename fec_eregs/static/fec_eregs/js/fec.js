// fec.js
//
// The main entrypoint for fec-eregs specific javascript.

var SiteNav = require('fec-style/js/site-nav').SiteNav;

var $ = window.$;
$(function () {
  console.log('ready');
  $('.js-site-nav').each(function () {
    new SiteNav(this);
  });
});
