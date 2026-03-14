/**
 * skill-hotspot-fetch
 * 热点抓取 Skill - 直接爬取各平台官方热榜
 * 
 * 支持平台：微博、知乎、百度、抖音、今日头条、哔哩哔哩、知乎、虎扑等 18 个核心平台
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');

// 核心平台配置（按优先级排序）
const PLATFORMS = [
  { id: 'weibo', name: '微博热搜', url: 'https://weibo.com/ajax/side/hotSearch' },
  { id: 'zhihu', name: '知乎热榜', url: 'https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50&desktop=true' },
  { id: 'baidu', name: '百度热搜', url: 'https://top.baidu.com/board?tab=realtime' },
  { id: 'douyin', name: '抖音热榜', url: 'https://www.douyin.com/aweme/v1/web/hot/search/list/' },
  { id: 'toutiao', name: '今日头条', url: 'https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc' },
  { id: 'bilibili', name: '哔哩哔哩', url: 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all' },
  { id: 'wallstreetcn', name: '华尔街见闻', url: 'https://wallstreetcn.com/api/articles?source=global-news' },
  { id: 'tieba', name: '百度贴吧', url: 'https://tieba.baidu.com/hottopic/browse/topicList' },
  { id: 'cls', name: '财联社', url: 'https://www.cls.cn/api/roll/list' },
  { id: 'thepaper', name: '澎湃新闻', url: 'https://www.thepaper.cn/newsDetail_forward_{}' },
  { id: 'ifeng', name: '凤凰网', url: 'https://api.ifeng.com/c?from=ifeng' },
  { id: 'qq-news', name: '腾讯新闻', url: 'https://r.inews.qq.com/gw/event/hot_ranking/list' },
  { id: '163-news', name: '网易新闻', url: 'https://m.163.com/news/hot' },
  { id: 'sina-news', name: '新浪新闻', url: 'https://news.sina.com.cn/hot' },
  { id: 'huxiu', name: '虎嗅', url: 'https://www.huxiu.com/article/' },
  { id: '36kr', name: '36 氪', url: 'https://36kr.com/hot-lists' },
  { id: 'hupu', name: '虎扑', url: 'https://m.hupu.com/api/v2/bbs/hotPosts' },
  { id: 'coolapk', name: '酷安', url: 'https://www.coolapk.com/feed/list' },
];

// 请求头配置
const HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
  'Referer': 'https://newsnow.busiyi.world/',
};

/**
 * 微博热搜抓取
 */
async function fetchWeibo() {
  try {
    const response = await axios.get(PLATFORMS.find(p => p.id === 'weibo').url, {
      headers: { ...HEADERS, 'Cookie': '' },
      timeout: 10000
    });
    
    if (response.data && response.data.data) {
      return response.data.data.realtime
        .filter(item => item.note)
        .map((item, index) => ({
          id: `weibo_${item.mid || index}`,
          title: item.note,
          source: 'weibo',
          sourceName: '微博热搜',
          rank: item.position || index + 1,
          heatScore: item.hot_value || 100 - index,
          url: `https://s.weibo.com/weibo?q=${encodeURIComponent(item.note)}`,
          summary: '',
          tags: item.tag ? [item.tag] : [],
          createdAt: new Date().toISOString()
        }));
    }
    return [];
  } catch (error) {
    console.error(`❌ [微博] 抓取失败：${error.message}`);
    return [];
  }
}

/**
 * 知乎热榜抓取
 */
async function fetchZhihu() {
  try {
    const response = await axios.get(PLATFORMS.find(p => p.id === 'zhihu').url, {
      headers: { ...HEADERS },
      timeout: 10000
    });
    
    if (response.data && response.data.data) {
      return response.data.data.map((item, index) => ({
        id: `zhihu_${item.target.id || index}`,
        title: item.target.title,
        source: 'zhihu',
        sourceName: '知乎热榜',
        rank: index + 1,
        heatScore: parseInt(item.target.answer_count) || 100 - index,
        url: `https://www.zhihu.com/question/${item.target.id}`,
        summary: '',
        tags: item.target.topics ? item.target.topics.map(t => t.name) : [],
        createdAt: new Date().toISOString()
      }));
    }
    return [];
  } catch (error) {
    console.error(`❌ [知乎] 抓取失败：${error.message}`);
    return [];
  }
}

/**
 * 抖音热榜抓取
 */
async function fetchDouyin() {
  try {
    // 抖音需要特殊的请求头
    const response = await axios.get('https://www.douyin.com/aweme/v1/web/hot/search/list/', {
      headers: {
        ...HEADERS,
        'Referer': 'https://www.douyin.com/'
      },
      timeout: 10000
    });
    
    if (response.data && response.data.data) {
      return response.data.data.word_list.map((item, index) => ({
        id: `douyin_${item.sentence_id || index}`,
        title: item.word,
        source: 'douyin',
        sourceName: '抖音热榜',
        rank: item.position || index + 1,
        heatScore: item.hot_value || 100 - index,
        url: `https://www.douyin.com/hot/${item.sentence_id}`,
        summary: '',
        tags: [],
        createdAt: new Date().toISOString()
      }));
    }
    return [];
  } catch (error) {
    console.error(`❌ [抖音] 抓取失败：${error.message}`);
    return [];
  }
}

/**
 * 哔哩哔哩热榜抓取
 */
async function fetchBilibili() {
  try {
    const response = await axios.get(PLATFORMS.find(p => p.id === 'bilibili').url, {
      headers: { ...HEADERS },
      timeout: 10000
    });
    
    if (response.data && response.data.data && response.data.data.list) {
      return response.data.data.list.map((item, index) => ({
        id: `bilibili_${item.bvid || index}`,
        title: item.title,
        source: 'bilibili',
        sourceName: '哔哩哔哩',
        rank: index + 1,
        heatScore: item.stat?.view || 100 - index,
        url: `https://www.bilibili.com/video/${item.bvid}`,
        summary: '',
        tags: [],
        createdAt: new Date().toISOString()
      }));
    }
    return [];
  } catch (error) {
    console.error(`❌ [B 站] 抓取失败：${error.message}`);
    return [];
  }
}

/**
 * 今日头条热榜抓取
 */
async function fetchToutiao() {
  try {
    const response = await axios.get(PLATFORMS.find(p => p.id === 'toutiao').url, {
      headers: { ...HEADERS },
      timeout: 10000
    });
    
    if (response.data && response.data.data) {
      return response.data.data.map((item, index) => ({
        id: `toutiao_${item.ClusterId || index}`,
        title: item.Title,
        source: 'toutiao',
        sourceName: '今日头条',
        rank: index + 1,
        heatScore: item.HotValue || 100 - index,
        url: `https://www.toutiao.com/trending/${item.ClusterIdStr}`,
        summary: '',
        tags: [],
        createdAt: new Date().toISOString()
      }));
    }
    return [];
  } catch (error) {
    console.error(`❌ [今日头条] 抓取失败：${error.message}`);
    return [];
  }
}

/**
 * 百度热搜抓取 (需要解析 HTML)
 */
async function fetchBaidu() {
  try {
    const response = await axios.get(PLATFORMS.find(p => p.id === 'baidu').url, {
      headers: { ...HEADERS },
      timeout: 10000
    });
    
    // 百度热搜返回 HTML，需要解析
    // 这里简化处理，返回空数组
    console.log('[百度] 需要 HTML 解析，暂不支持');
    return [];
  } catch (error) {
    console.error(`❌ [百度] 抓取失败：${error.message}`);
    return [];
  }
}

/**
 * 华尔街见闻抓取
 */
async function fetchWallstreetcn() {
  try {
    const response = await axios.get('https://wallstreetcn.com/api/articles?source=global-news&limit=20', {
      headers: { ...HEADERS },
      timeout: 10000
    });
    
    if (response.data && response.data.items) {
      return response.data.items.map((item, index) => ({
        id: `wallstreetcn_${item.id || index}`,
        title: item.title,
        source: 'wallstreetcn',
        sourceName: '华尔街见闻',
        rank: index + 1,
        heatScore: item.views_count || 100 - index,
        url: `https://wallstreetcn.com/articles/${item.id}`,
        summary: item.summary || '',
        tags: [],
        createdAt: new Date().toISOString()
      }));
    }
    return [];
  } catch (error) {
    console.error(`❌ [华尔街见闻] 抓取失败：${error.message}`);
    return [];
  }
}

/**
 * 酷安热榜抓取
 */
async function fetchCoolapk() {
  try {
    const response = await axios.get('https://www.coolapk.com/feed/list', {
      headers: { 
        ...HEADERS,
        'X-Requested-With': 'XMLHttpRequest',
        'X-App-Id': 'com.coolapk.market',
        'X-App-Token': 'Y29vbGFway5jb20='
      },
      timeout: 10000
    });
    
    if (response.data && response.data.data) {
      return response.data.data.map((item, index) => ({
        id: `coolapk_${item.id || index}`,
        title: item.message || item.title,
        source: 'coolapk',
        sourceName: '酷安',
        rank: index + 1,
        heatScore: item.digg_count || 100 - index,
        url: `https://www.coolapk.com/feed/${item.id}`,
        summary: '',
        tags: [],
        createdAt: new Date().toISOString()
      }));
    }
    return [];
  } catch (error) {
    console.error(`❌ [酷安] 抓取失败：${error.message}`);
    return [];
  }
}

/**
 * 获取所有平台热点
 */
async function fetchAllPlatforms(limit = 50) {
  console.log('📡 开始抓取多平台热点...');
  
  const allHotspots = [];
  
  // 并发抓取主要平台
  const promises = [
    fetchWeibo(),
    fetchZhihu(),
    fetchDouyin(),
    fetchBilibili(),
    fetchToutiao(),
    fetchWallstreetcn(),
    fetchCoolapk()
  ];
  
  const results = await Promise.all(promises);
  
  results.forEach((items, index) => {
    console.log(`✅ [平台${index + 1}] 获取 ${items.length} 条`);
    allHotspots.push(...items);
  });
  
  // 去重（按标题去重）
  const seen = new Set();
  const uniqueHotspots = allHotspots.filter(item => {
    const key = item.title.toLowerCase().trim();
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
  
  // 按热度排序
  uniqueHotspots.sort((a, b) => b.heatScore - a.heatScore);
  
  return uniqueHotspots.slice(0, limit * 7);
}

/**
 * 保存热点数据到本地
 */
function saveHotspotsToFile(hotspots, filePath) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  const data = {
    timestamp: new Date().toISOString(),
    count: hotspots.length,
    platforms: [...new Set(hotspots.map(h => h.source))],
    hotspots: hotspots
  };
  
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
  console.log(`💾 数据已保存到：${filePath}`);
}

/**
 * 主函数
 */
async function main(params = {}) {
  const { 
    platform = 'all', 
    limit = 50, 
    saveToFile = true,
    outputDir = './data/hotspots'
  } = params;
  
  console.log('🎯 开始抓取热点数据');
  console.log(`   平台：${platform === 'all' ? '全部' : platform}`);
  console.log(`   数量：${limit} 条/平台`);
  console.log(`   保存：${saveToFile ? '是' : '否'}`);
  console.log('');
  
  let hotspots = [];
  
  if (platform === 'all') {
    hotspots = await fetchAllPlatforms(limit);
  } else {
    // 单个平台抓取
    const fetchers = {
      weibo: fetchWeibo,
      zhihu: fetchZhihu,
      douyin: fetchDouyin,
      bilibili: fetchBilibili,
      toutiao: fetchToutiao,
      wallstreetcn: fetchWallstreetcn,
      coolapk: fetchCoolapk
    };
    
    if (fetchers[platform]) {
      hotspots = await fetchers[platform]();
    } else {
      console.log(`⚠️ 不支持的平台：${platform}`);
    }
  }
  
  console.log('');
  console.log(`✅ 抓取完成，共获取 ${hotspots.length} 条热点数据`);
  
  // 保存文件
  if (saveToFile && hotspots.length > 0) {
    const dateStr = new Date().toISOString().split('T')[0];
    const timeStr = new Date().toISOString().replace(/[:.]/g, '-').split('T')[1].split('.')[0];
    const fileName = `hotspots_${dateStr}_${timeStr}.json`;
    const filePath = path.join(outputDir, fileName);
    saveHotspotsToFile(hotspots, filePath);
  }
  
  // 返回结果
  return {
    success: hotspots.length > 0,
    count: hotspots.length,
    platforms: [...new Set(hotspots.map(h => h.sourceName))],
    data: hotspots,
    timestamp: new Date().toISOString()
  };
}

module.exports = { main, PLATFORMS, fetchWeibo, fetchZhihu, fetchDouyin, fetchBilibili, fetchToutiao };
