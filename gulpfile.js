var gulp = require('gulp'),
    autoprefixer = require('gulp-autoprefixer'),
    livereload = require('gulp-livereload'),
    rename = require('gulp-rename'),
    sass = require('gulp-sass'),
    sourcemaps = require('gulp-sourcemaps'),
    uglify = require('gulp-uglify');

function handleError(err) {
    console.log(err.toString());
      this.emit('end');
}

gulp.task('sass', function () {
  gulp.src('./ucitelj/assets/sass/**/*.scss')
    .pipe(sass({includePaths: ['./ucitelj/assets/sass']}))
    .pipe(sourcemaps.init())
        .pipe(sass({outputStyle: 'compressed'}).on('error', handleError))
        .pipe(autoprefixer('last 2 version', 'safari 5', 'ie 7', 'ie 8', 'ie 9', 'opera 12.1', 'ios 6', 'android 4'))
    .pipe(rename('style.css'))
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest('./ucitelj/static/css'));
});

gulp.task('uglify', function() {
  gulp.src('./ucitelj/assets/js/*.js')
    .pipe(uglify('main.js'))
    .pipe(gulp.dest('./ucitelj/js'))
});

gulp.task('watch', function(){
    livereload.listen();
    gulp.watch(['./ucitelj/assets/sass/*/*.scss', './assets/sass/**/*.scss'], ['sass']);
    gulp.watch('./ucitelj/assets/js/*.js', ['uglify']);
    gulp.watch(['./ucitelj/static/css/style.css', './ucitelj/templates/*/*.html', './js/*.js'], function (files){
        livereload.changed(files)
    });
});
