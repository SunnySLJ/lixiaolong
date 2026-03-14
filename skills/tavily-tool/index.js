/**
 * Tavily Search Tool
 * 使用 Tavily AI 进行智能网络搜索
 */

const axios = require('axios');

const TAVILY_API_KEY = process.env.TAVILY_API_KEY;
const TAVILY_API_URL = 'https://api.tavily.com/search';

/**
 * Tavily 搜索
 */
async function tavilySearch(query, options = {}) {
  const {
    max_results = 5,
    include_answer = true,
    include_raw_content = false
  } = options;

  if (!TAVILY_API_KEY) {
    throw new Error('TAVILY_API_KEY 未配置。请在 .env 文件中配置 TAVILY_API_KEY');
  }

  try {
    const response = await axios.post(TAVILY_API_URL, {
      api_key: TAVILY_API_KEY,
      query: query,
      max_results: max_results,
      include_answer: include_answer,
      include_raw_content: include_raw_content,
      search_depth: 'basic' // 或 'advanced'
    }, {
      headers: {
        'Content-Type': 'application/json'
      },
      timeout: 30000
    });

    return response.data;
  } catch (error) {
    console.error('[Tavily 搜索] 失败:', error.message);
    if (error.response) {
      console.error('响应状态:', error.response.status);
      console.error('响应数据:', error.response.data);
    }
    throw error;
  }
}

/**
 * 主函数
 */
async function main(params = {}) {
  const {
    query,
    max_results = 5,
    include_answer = true,
    include_raw_content = false
  } = params;

  if (!query) {
    return {
      success: false,
      error: '缺少 query 参数'
    };
  }

  console.log('🔍 Tavily 搜索');
  console.log(`   查询：${query}`);
  console.log(`   数量：${max_results}`);
  console.log('=' .repeat(50));

  try {
    const result = await tavilySearch(query, {
      max_results,
      include_answer,
      include_raw_content
    });

    console.log('\n✅ 搜索完成');
    console.log(`   结果数：${result.results?.length || 0}`);
    
    if (result.answer) {
      console.log(`\n📝 AI 答案:\n   ${result.answer}`);
    }

    if (result.results && result.results.length > 0) {
      console.log('\n📊 搜索结果:');
      result.results.forEach((item, i) => {
        console.log(`\n   ${i + 1}. ${item.title}`);
        console.log(`      URL: ${item.url}`);
        console.log(`      相关度：${(item.score * 100).toFixed(1)}%`);
        console.log(`      摘要：${item.content?.substring(0, 100)}...`);
      });
    }

    return {
      success: true,
      answer: result.answer,
      results: result.results,
      query_time: result.query_time
    };

  } catch (error) {
    console.error('\n❌ 搜索失败:', error.message);
    return {
      success: false,
      error: error.message
    };
  }
}

module.exports = {
  main,
  tavilySearch
};
