'use strict';

module.exports = function(grunt) {
  require('load-grunt-tasks')(grunt);

  grunt.initConfig({
    copy: {
      'fec-style': {
        files: [
          {
            expand: true,
            cwd: 'node_modules/fec-style',
            src: 'img/**',
            dest: 'fec_eregs/static/fec_eregs/'
          },
          {
            expand: true,
            cwd: 'node_modules/fec-style',
            src: 'fonts/**',
            dest: 'fec_eregs/static/fec_eregs/'
          }
        ]
      }
    },
    sass: {
      options: {
        includePaths: [
          'fec_eregs/static/fec_eregs/scss',
          'node_modules/fec-style/scss'
        ]
      },
      dist: {
        files: {
          'fec_eregs/static/fec_eregs/css/main.css': 'fec_eregs/static/fec_eregs/scss/main.scss'
        }
      }
    }
  });

  grunt.registerTask('build:css', ['copy:fec-style', 'sass']);
  grunt.registerTask('build', ['build:css']);

  grunt.registerTask('default', ['build']);
};
