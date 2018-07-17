// fec.js
//
// The main entrypoint for fec-eregs specific javascript.

var $ = require('jquery');

var SiteNav = require('./site-nav').SiteNav;
var Glossary = require('glossary-panel');
var terms = require('./data/terms')

var $ = window.$;
$(function () {
  $('.js-site-nav').each(function () {
    new SiteNav(this, {
      cmsUrl: window.CMS_URL,
      webAppUrl: window.WEB_URL
    });
  });
new Glossary(terms, {}, {
    termClass: 'glossary__term accordion__button',
    definitionClass: 'glossary__definition accordion__content'
  });
});



