/**
 * Finds unique values in an array of values
 * @param {array} arr - sequence of strings, numbers, booleans
 * @returns {array} array of unique values
 *
 * @example
 * import findUnique from './utils/unique';
 * const unique = findUnique([1,2,2,3]);
 * // [1,2,3]
 */

const from = 'àáäâèéëêìíïîòóöôùúüûñç·/_,:;';
const to = 'aaaaeeeeiiiioooouuuunc------';

export default function slugify(text) {
  let t = text.replace(/^\s+|\s+$/g, ''); // trim
  t = t.toLowerCase(); // convert to lower case

  // remove accents, swap ñ for n, etc
  // eslint-disable-next-line no-plusplus
  for (let i = 0, l = from.length; i < l; i++) {
    t = t.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
  }

  return String(t)
    .replace(/[^a-z0-9 -]/g, '') // remove invalid chars
    .replace(/\s+/g, '-') // collapse whitespace and replace by -
    .replace(/-+/g, '-'); // collapse dashes
}
