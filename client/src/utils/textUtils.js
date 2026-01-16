/**
 * Simplify Arabic text for comparison
 * Normalizes alef variants, taa marbuta, and yaa
 * @param {string} text - Arabic text to simplify
 * @returns {string} Simplified text
 */
export function simplifyArabicText(text) {
  return text
    .replace(/[إأآ]/g, 'ا')
    .replace(/ة/g, 'ه')
    .replace(/ى/g, 'ي');
}
