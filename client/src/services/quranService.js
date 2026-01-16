import { apiClient } from './api';

export const quranService = {
  /**
   * Fetch all chapters (surahs)
   * @returns {Promise<Array>} List of chapters
   */
  async getChapters() {
    return apiClient.get('/surahs');
  },
  
  /**
   * Fetch verses based on range parameters
   * @param {Object} params - Range parameters
   * @param {string} params.rangeType - 'juz', 'page', or 'key'
   * @param {string} params.rangeValue - Range value string
   * @returns {Promise<Array>} List of verses
   */
  async getVerses({ rangeType, rangeValue }) {
    return apiClient.get('/verses', {
      range_type: rangeType,
      range_value: rangeValue,
    });
  },
  
  /**
   * Build range value string from config
   * @param {string} rangeType - 'juz', 'page', or 'key'
   * @param {Object} config - Range configuration object
   * @returns {string} Formatted range value string
   */
  buildRangeValue(rangeType, config) {
    if (rangeType === 'key') {
      const { startChapter, startVerse, endChapter, endVerse } = config;
      return `${startChapter}:${startVerse}-${endChapter}:${endVerse}`;
    }
    return `${config.start}:${config.end}`;
  },
};
