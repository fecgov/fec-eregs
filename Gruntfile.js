'use strict';

module.exports = function(grunt) {
  require('load-grunt-tasks')(grunt);

  grunt.initConfig({
    sass: {
      options: {
        includePaths: [
          'fec_eregs/static/fec_eregs/fec-style/css/scss',
          'node_modules/fec-style/scss'
        ]
      },
      dist: {
        files: {
          'fec_eregs/static/fec_eregs/fec-style/css/main.css': 'fec_eregs/static/fec_eregs/fec-style/css/scss/main.scss'
        }
      }
    }
  });

  grunt.registerTask('default', ['sass']);
};
