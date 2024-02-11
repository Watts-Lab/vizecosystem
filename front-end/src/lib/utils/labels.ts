const labelMap : Map<string, string> = new Map([
    ['non-news', 'Non-news'], 
    ['non_news', 'Non-news'],
    ['news', 'News'],
    ['hard_news', 'Hard news'], 
    ['fake_news', 'Fake News'],
    ['social_media', 'Social Media'],
    ['music', 'Music'],
    ['other', 'Other'],
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