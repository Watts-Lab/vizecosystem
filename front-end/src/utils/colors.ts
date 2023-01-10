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
    ['L', 'blue'],
    ['R', 'red'],
])

const mediumMap : Map<string, {}> = new Map([
    ['tv', { line:'#588157', polygon: '#C5CEB6' }],
    ['online', { line:'#f7934c', polygon: '#f7c59f' }],
])

export default colorMap;
export { politicsMap, mediumMap };
  

