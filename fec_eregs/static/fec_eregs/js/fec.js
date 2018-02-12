// fec.js
//
// The main entrypoint for fec-eregs specific javascript.

var SiteNav = require('./site-nav').SiteNav;

var $ = window.$;
$(function () {
  $('.js-site-nav').each(function () {
    new SiteNav(this, {
      cmsUrl: window.CMS_URL,
      webAppUrl: window.WEB_URL
    });
  });
});
