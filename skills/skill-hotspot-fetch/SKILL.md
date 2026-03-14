# skill-hotspot-fetch

热点抓取 Skill - 从多平台获取热点话题数据

## 功能描述

从 TrendRadar、智小红、智小抖、巨量算数等平台抓取热点话题数据，并标准化存储。

## 触发词

- "抓取热点"
- "获取热点话题"
- "热点数据"
- "trend radar"
- "抖音热点"
- "小红书热点"

## 输入参数

```json
{
  "platform": "all",  // all, trendradar, xiaohongshu, douyin, giant
  "category": "",     // 分类，如"科技"、"娱乐"
  "limit": 20         // 获取数量限制
}
```

## 输出格式

```json
{
  "success": true,
  "data": [
    {
      "id": "hotspot_001",
      "title": "热点话题标题",
      "source": "trendradar",
      "category": "科技",
      "heatScore": 95,
      "trend": "rising",
      "keywords": ["关键词 1", "关键词 2"],
      "rawData": {},
      "createdAt": "2026-03-14T09:00:00Z"
    }
  ],
  "timestamp": "2026-03-14T09:00:00Z"
}
```

## 实现代码

```javascript
const axios = require('axios');
const fs = require('fs');
const path = require('path');

// TrendRadar API 对接
async function fetchTrendRadar(limit = 20) {
  try {
    // TODO: 实现 TrendRadar API 调用
    // GitHub: https://github.com/sansan0/TrendRadar
    const response = await axios.get('https://api.trendradar.com/hot', {
      params: { limit }
    });
    return response.data;
  } catch (error) {
    console.error('TrendRadar 抓取失败:', error.message);
    return [];
  }
}

// 智小红 API 对接
async function fetchXiaohongshu(category = '', limit = 20) {
  try {
    // TODO: 实现智小红 API 调用
    const apiKey = process.env.ZHIXIAOHONG_API_KEY;
    const response = await axios.get('https://api.zhixiaohong.com/hot', {
      headers: { 'Authorization': `Bearer ${apiKey}` },
      params: { category, limit }
    });
    return response.data;
  } catch (error) {
    console.error('智小红抓取失败:', error.message);
    return [];
  }
}

// 智小抖 API 对接
async function fetchXiaodouyin(category = '', limit = 20) {
  try {
    // TODO: 实现智小抖 API 调用
    const apiKey = process.env.ZHIXIAODOU_API_KEY;
    const response = await axios.get('https://api.zhixiaodou.com/hot', {
      headers: { 'Authorization': `Bearer ${apiKey}` },
      params: { category, limit }
    });
    return response.data;
  } catch (error) {
    console.error('智小抖抓取失败:', error.message);
    return [];
  }
}

// 巨量算数爬取
async function fetchGiantArithmetic() {
  try {
    // TODO: 实现巨量算数爬取
    // URL: https://creator.douyin.com/creator-micro/creator-count/arithmetic-index
    console.log('巨量算数爬取功能待实现');
    return [];
  } catch (error) {
    console.error('巨量算数抓取失败:', error.message);
    return [];
  }
}

// 主函数
async function main(params = {}) {
  const { platform = 'all', category = '', limit = 20 } = params;
  
  console.log(`开始抓取热点数据 - 平台：${platform}, 分类：${category}, 数量：${limit}`);
  
  let allHotspots = [];
  
  if (platform === 'all' || platform === 'trendradar') {
    const data = await fetchTrendRadar(limit);
    allHotspots = [...allHotspots, ...data];
  }
  
  if (platform === 'all' || platform === 'xiaohongshu') {
    const data = await fetchXiaohongshu(category, limit);
    allHotspots = [...allHotspots, ...data];
  }
  
  if (platform === 'all' || platform === 'douyin') {
    const data = await fetchXiaodouyin(category, limit);
    allHotspots = [...allHotspots, ...data];
  }
  
  if (platform === 'all' || platform === 'giant') {
    const data = await fetchGiantArithmetic();
    allHotspots = [...allHotspots, ...data];
  }
  
  // 去重和排序
  const uniqueHotspots = Array.from(
    new Map(allHotspots.map(item => [item.id, item])).values()
  ).sort((a, b) => b.heatScore - a.heatScore);
  
  console.log(`抓取完成，共获取 ${uniqueHotspots.length} 条热点数据`);
  
  return {
    success: true,
    data: uniqueHotspots.slice(0, limit),
    timestamp: new Date().toISOString()
  };
}

module.exports = { main };
```

## 使用示例

### OpenClaw 调用

```bash
openclaw skill run skill-hotspot-fetch --params '{"platform":"all","limit":20}'
```

### 程序化调用

```javascript
const hotspotFetch = require('./skills/skill-hotspot-fetch');

const result = await hotspotFetch.main({
  platform: 'all',
  category: '科技',
  limit: 20
});

console.log(result.data);
```

## 待办事项

- [ ] 实现 TrendRadar API 对接
- [ ] 实现智小红 API 对接
- [ ] 实现智小抖 API 对接
- [ ] 实现巨量算数爬取
- [ ] 添加热点去重逻辑
- [ ] 添加数据持久化存储
- [ ] 添加错误重试机制
- [ ] 添加速率限制

## 相关文件

- `config/hotspot-sources.json` - 数据源配置
- `scripts/test-hotspot.js` - 测试脚本
