'use strict';

module.exports = function(grunt) {
  require('load-grunt-tasks')(grunt);

  grunt.initConfig({
    sass: {
      options: {
        includePaths: [
          'fec_eregs/static/fec_eregs/scss'
        ]
      },
      dist: {
        files: {
          'fec_eregs/static/fec_eregs/css/main.css': 'fec_eregs/static/fec_eregs/scss/main.scss'
        }
      }
    }
  });

  grunt.registerTask('build:css', ['sass']);
  grunt.registerTask('build', ['build:css']);

  grunt.registerTask('default', ['build']);
};
