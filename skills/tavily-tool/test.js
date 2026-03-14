/**
 * Tavily Search Tool 测试脚本
 */

const { main } = require('./index');

async function test() {
  console.log('🧪 Tavily Search Tool 测试\n');
  console.log('=' .repeat(50));

  // 检查 API Key
  if (!process.env.TAVILY_API_KEY) {
    console.log('⚠️  TAVILY_API_KEY 未配置');
    console.log('\n配置方法:');
    console.log('1. 访问 https://app.tavily.com/ 获取 API Key');
    console.log('2. 在 .env 文件中添加:');
    console.log('   TAVILY_API_KEY=your_key\n');
    return;
  }

  // 测试搜索
  const result = await main({
    query: 'AI 最新进展 2026',
    max_results: 5,
    include_answer: true
  });

  console.log('\n' + '=' .repeat(50));
  if (result.success) {
    console.log('✅ 测试通过');
  } else {
    console.log('❌ 测试失败:', result.error);
  }
}

test().catch(console.error);
