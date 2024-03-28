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

const flowMap : Map<string, string> = new Map([
  ['Inflow', '#011f5b'],
  ['Outflow', '#990000'],
])

const colorMapByMedium : Map<string, { colorMap: Map<string,{color: string, order: number}> }> = new Map([
  ['tv', {
    colorMap: new Map([
      ['news', {color: '#011f5b', order: 1}],
      ['entertainment', {color: '#cab2d6', order: 2}],
      ['documentary', {color: 'steelblue', order: 3}],
      ['reality_variety', {color: '#ffa07a', order: 4}],
      ['sports', {color: 'lightgreen', order: 5}],
      ['other', {color: 'gainsboro', order: 6}],
    ]),
  }
  ],
  ['web', {
    colorMap: new Map([
      ['hard_news', {color: '#011f5b', order: 1}],
      ['fake_news', {color: '#990000', order: 2}],
      ['social_media', {color: '#fdbf6f', order: 3}],
      ['lifestyle', {color: 'lightblue', order: 4}],
      ['entertainment', {color: '#cab2d6', order: 5}],
      ['other', {color: 'gainsboro', order: 6}],  
    ]),
  }],
  ['mobile', {
    colorMap: new Map([
      ['news', {color: '#011f5b', order: 1}],
      ['social_media', {color: '#fdbf6f', order: 2}],
      ['lifestyle', {color: 'lightblue', order: 3}],
      ['entertainment', {color: '#cab2d6', order: 4}],
      ['other', {color: 'gainsboro', order: 5}],
    ]),
  }],
  ['tablet', {
    colorMap: new Map([
      ['news', {color: '#011f5b', order: 1}],
      ['social_media', {color: '#fdbf6f', order: 2}],
      ['lifestyle', {color: 'lightblue', order: 3}],
      ['entertainment', {color: '#cab2d6', order: 4}],
      ['other', {color: 'gainsboro', order: 5}],
    ]),
  }],
])

export default colorMap;
export { politicsMap, mediumMap, colorMapByMedium, flowMap };
  

