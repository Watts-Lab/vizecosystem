const colorMap : Map<string, string> = new Map([
    ['tv_not_news', '#005F73'], // dark blue
    ['mobile_not_news', '#0A9396'], // medium blue
    ['desktop_not_news', '#94D2BD'], // light blue
    ['tv_news', '#1B4332'], // dark green
    ['mobile_news', '#2D6A4F'], // medium green
    ['desktop_news', '#40916C'], // light green
    ['mobile_fake_news', '#BB3E03'], // dark orange
    ['desktop_fake_news', '#CA6702'], // medium orange
])

const politicsMap : Map<string, string> = new Map([
    ['L', '#011f5b'],
    ['R', '#990000'],
])

const mediumMap : Map<string, {}> = new Map([
    ['tv', { line:'#588157', polygon: '#C5CEB6' }],
    ['online', { line:'#f7934c', polygon: '#f7c59f' }],
])

const colorMapByMedium : Map<string, { colorMap: Map<string,string> }> = new Map([
		['tv', {
            colorMap: new Map([
                ['non-news', '#a6cee3'],
                // ['non-news', 'gainsboro'],
                ['news', '#fb9a99']
            ]),
		}
		],
		['web', {
            colorMap: new Map([
                ['non_news', '#a6cee3'],
                // ['non_news', 'gainsboro'],
                ['hard_news', '#fb9a99'],
                ['fake_news', '#e31a1c'],
                ['social_media', '#fdbf6f'],
            ]),
		}],
		['mobile', {
            colorMap: new Map([
                ['news', '#fb9a99'],
                // ['other', '#a6cee3'],
                ['other', '#a6cee3'],
                ['social_media', '#fdbf6f'],
                // ['lifestyle', 'navy'],
                // ['unlabeled_app', 'DarkMagenta'],
                // ['browser', 'teal'],
            ]),
		}],
	])

export default colorMap;
export { politicsMap, mediumMap, colorMapByMedium };
  

