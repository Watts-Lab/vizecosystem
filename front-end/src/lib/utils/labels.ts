const labelMap : Map<string, string> = new Map([
    ['non-news', 'Non-news'], 
    ['non_news', 'Non-news'],
    ['news', 'News'],
    ['hard_news', 'News'], 
    ['fake_news', 'Fake News'],
    ['social_media', 'Social Media'],
    ['entertainment', 'Entertainment'],
    ['utility+lifestyle', 'Utility+Life'],
    ['communication', 'Communication'],
    ['other', 'Other'],
    ['documentary', 'Documentary'],
    ['reality_variety', 'Reality/Variety'],
    ['sports', 'Sports'],
    ['lifestyle', 'Lifestyle'],
    ['unlabeled_app', 'Other'],
    ['browser', 'Browser'],
    ['utility', 'Utility'],
])

const mediumMap : Map<string, string> = new Map([
    ['tv','TV'],
    ['web', 'Online']
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

const flowMap : Map<string, string> = new Map([
    ['Inflow', 'Inflow'],
    ['Outflow', 'Outflow'],
])

export default labelMap;
export { politicsMap, orderMap, flowMap, mediumMap };