// JavaScript Document
chrome.app.runtime.onLaunched.addListener(function() {
  chrome.app.window.create('window.html', {
    'bounds': {
      'width': Math.round(window.screen.availWidth),
      'height': Math.round(window.screen.availHeight)
    }
  });
});