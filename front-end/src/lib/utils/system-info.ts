//----------------------------------------------------------------------------//
//                             Svelte System Info                             //
//----------------------------------------------------------------------------//
/**** DeviceBrowserName ****/
// based on: https://github.com/keithws/browser-report

function getBrowserInfo() {

    const UserAgent = {
        Value:    window.navigator.userAgent,
        contains: function contains (ValueToSearchFor:string):boolean {
          return (this.Value.indexOf(ValueToSearchFor) >= 0)
        },
        lacks:    function lacks (ValueToSearchFor:string):boolean {
          return (this.Value.indexOf(ValueToSearchFor) < 0)
        },
        match:    function match (Pattern:RegExp):any {
          return this.Value.match(Pattern)
        },
        matches:  function matches (Pattern:RegExp):boolean {
          return (this.Value.match(Pattern) != null)
        },
      }

    let DeviceBrowserName:string = '(n/a)'

    if (UserAgent.contains('Trident') || UserAgent.contains('MSIE')) {
      DeviceBrowserName = (UserAgent.contains('Mobile') ? 'IE Mobile' : 'Internet Explorer')
    }

    if (UserAgent.contains('Firefox') && UserAgent.lacks('Seamonkey')) {
      DeviceBrowserName = (UserAgent.contains('Android') ? 'Firefox for Android' : 'Firefox')
    }

    if (
      UserAgent.contains('Safari') && UserAgent.lacks('Chrome') &&
      UserAgent.lacks('Chromium')  && UserAgent.lacks('Android')
    ) {
      DeviceBrowserName = (
        UserAgent.contains('CriOS')
        ? 'Chrome for iOS'
        : (UserAgent.contains('FxiOS') ? 'Firefox for iOS' : 'Safari')
      )
    }

    if (UserAgent.contains('Chrome')) {
      if (UserAgent.matches(/\bChrome\/[.0-9]* Mobile\b/)) {
        DeviceBrowserName = (UserAgent.matches(/\bVersion\/\d+\.\d+\b/) || UserAgent.matches(/\bwv\b/)
          ? 'WebView on Android'
          : 'Chrome for Android'
        )
      } else {
        DeviceBrowserName = 'Chrome'
      }
    }

    if (
      UserAgent.contains('Android') && UserAgent.lacks('Chrome')  &&
      UserAgent.lacks('Chromium')   && UserAgent.lacks('Trident') &&
      UserAgent.lacks('Firefox')
    ) {
      DeviceBrowserName = 'Android Browser'
    }

    if (UserAgent.contains('Edge')) {
      DeviceBrowserName = 'Edge'
    }

    if (UserAgent.contains('UCBrowser')) {
      DeviceBrowserName = 'UC Browser for Android'
    }

    if (UserAgent.contains('SamsungBrowser')) {
      DeviceBrowserName = 'Samsung Internet'
    }

    if (UserAgent.contains('OPR') || UserAgent.contains('Opera')) {
      DeviceBrowserName = (
        UserAgent.contains('Opera Mini')
        ? 'Opera Mini'
        : (
          UserAgent.contains('Opera Mobi') ||
          UserAgent.contains('Opera Tablet') ||
          UserAgent.contains('Mobile')
          ? 'Opera Mobile'
          : 'Opera'
        )
      )
    }

    if (UserAgent.contains('BB10') || UserAgent.contains('PlayBook') || UserAgent.contains('BlackBerry')) {
      DeviceBrowserName = 'Blackberry'
    }

    return DeviceBrowserName
}

export default getBrowserInfo