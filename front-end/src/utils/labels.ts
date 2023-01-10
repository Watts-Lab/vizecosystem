const labelMap : Map<string, string> = new Map([
    ['tv_not_news', '#005F73'],
    ['mobile_not_news', '#0A9396'],
    ['desktop_not_news', '#94D2BD'], 
    ['tv_news', '#1B4332'],
    ['mobile_news', '#2D6A4F'], 
    ['desktop_news', '#40916C'], 
    ['mobile_fake_news', '#BB3E03'],
    ['desktop_fake_news', '#CA6702'], 
])

const orderMap : Map<string, number> = new Map([
    ['tv_R', 0],
    ['tv_L', 3],
    ['online_R', 1],
    ['online_L', 2]
])

const politicsMap : Map<string, string> = new Map([
    ['L', 'Left'],
    ['R', 'Right'],
])

export default labelMap;
export { politicsMap, orderMap };