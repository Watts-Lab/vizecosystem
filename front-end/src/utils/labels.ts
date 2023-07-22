const labelMap : Map<string, string> = new Map([
    ['non-news', 'Non news'], 
    ['news', 'News'],
    ['other_news', 'Other news'], 
    ['facebook', 'Facebook'], 
    ['hard_news', 'Hard news'], 
    ['youtube', 'YouTube'], 
    ['twitter', 'Twitter'], 
    ['reddit', 'Reddit'], 
    ['fake_news', 'Fake News']
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