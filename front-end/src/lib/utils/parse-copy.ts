export default function parseCopy(text: string) {
    const pattern: RegExp = /\[(.*?)\|(.*?)\]/g;
    const matches: RegExpMatchArray = text.match(pattern)!;
    
    if (matches) {
        matches.forEach((match) => {
            const [link, url]: string[] = match.slice(1, -1).split('|');
            text = text.replace(match, `<a class='link' href='${url}' target='_blank'>${link}</a>`);
        });
    }
    return text;
}