function parseLink(text: string) {
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

function parseItalic(text: string) {
	const pattern: RegExp = /_i_(.*?)_i_/g;
	const matches: RegExpMatchArray = text.match(pattern)!;

	if (matches) {
		matches.forEach((match) => {
			text = text.replace(match, `<i>${match.slice(3, -3)}</i>`);
		});
	}
	return text;
}

function parseBold(text: string) {
	const pattern: RegExp = /_b_(.*?)_b_/g;
	const matches: RegExpMatchArray = text.match(pattern)!;

	if (matches) {
		matches.forEach((match) => {
			text = text.replace(match, `<b>${match.slice(3, -3)}</b>`);
		});
	}
	return text;
}

function parseCopy(text: string) {
	text = parseLink(text);
	text = parseItalic(text);
	text = parseBold(text);
	return text;
}

export default parseCopy;
