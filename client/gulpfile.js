'use strict';

var gulp = require('gulp'),
	gutil = require('gulp-util'),
	jshint = require('gulp-jshint'),
	concat = require('gulp-concat'),
	uglify = require('gulp-uglify'),
	rename = require('gulp-rename'),
	plumber = require('gulp-plumber'),
	sass = require('gulp-sass'),
	minifyCss = require('gulp-minify-css'),
	sourcemaps = require('gulp-sourcemaps'),
	browserSync = require('browser-sync').create();

var defaults = {
	buildName: 'diaspyra-chat',
	src: {
		scripts: 'src/scripts/**/*.js',
		styles: 'src/styles/index.scss'
	},
	dest: {
		scripts: 'build/',
		styles: 'build/'
	}
};

gulp.task('jshint', function() {
	return gulp.src(defaults.src.scripts)
		.pipe(jshint())
		.pipe(jshint.reporter('jshint-stylish'));
});

gulp.task('build-js', function() {
	return gulp.src(defaults.src.scripts)
		.pipe(sourcemaps.init())
		.pipe(concat('bundle.js'))
		.pipe(uglify())
		.pipe(sourcemaps.write())
		.pipe(rename(defaults.buildName + '.min.js'))
		.pipe(gulp.dest(defaults.dest.scripts));
});

gulp.task('build-css', function() {
	gulp.src(defaults.src.styles)
		.pipe(plumber())
		.pipe(sourcemaps.init())
		.pipe(sass.sync().on('error', sass.logError))
		.pipe(minifyCss())
		.pipe(sourcemaps.write())
		.pipe(rename(defaults.buildName + '.min.css'))
		.pipe(gulp.dest(defaults.dest.styles));
});

gulp.task('serve', ['build-css'], function() {
	browserSync.init({
		notify: false,
		server: {
			baseDir: './demo',
			routes: {
        '/bower_components': 'bower_components',
        '/build': 'build'
      }
		}
	});

	gulp.watch(defaults.src.scripts, ['jshint', 'build-js']);
	gulp.watch('src/styles/**/*.scss', ['build-css']);
	gulp.watch(['demo/**/*', 'build/**/*']).on("change", browserSync.reload);
});

gulp.task('default', ['serve']);