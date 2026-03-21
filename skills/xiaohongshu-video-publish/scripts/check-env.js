#!/usr/bin/env node

/**
 * 环境检查脚本
 * 
 * 用法:
 *   node check-env.js
 */

import fs from 'node:fs';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const UPLOADS_DIR = 'C:\\tmp\\openclaw\\uploads';
const REQUIRED_DIRS = [
  UPLOADS_DIR,
  'C:\\Users\\爽爽\\.openclaw\\workspace'
];

console.log('🔍 检查小红书视频发布环境...\n');

let allPassed = true;

// 检查 Node.js
console.log('📦 Node.js 环境');
const nodeVersion = process.version;
const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0]);
if (majorVersion >= 18) {
  console.log(`   ✅ Node.js ${nodeVersion}`);
} else {
  console.log(`   ❌ Node.js ${nodeVersion} (需要 >=18.0.0)`);
  allPassed = false;
}

// 检查 OpenClaw
console.log('\n🦞 OpenClaw');
const openclawCheck = spawnSync('openclaw', ['status'], { 
  encoding: 'utf-8',
  timeout: 5000
});
if (openclawCheck.status === 0) {
  console.log('   ✅ OpenClaw 已安装并运行');
} else {
  console.log('   ❌ OpenClaw 未运行或无法访问');
  console.log('      解决：运行 openclaw gateway start');
  allPassed = false;
}

// 检查浏览器服务
console.log('\n🌐 浏览器服务');
const browserCheck = spawnSync('openclaw', ['browser', 'status'], {
  encoding: 'utf-8',
  timeout: 5000
});
if (browserCheck.stdout?.includes('enabled')) {
  console.log('   ✅ 浏览器服务可用');
} else {
  console.log('   ⚠️  浏览器服务未启动（首次使用会自动启动）');
}

// 检查目录
console.log('\n📁 目录结构');
REQUIRED_DIRS.forEach(dir => {
  if (fs.existsSync(dir)) {
    console.log(`   ✅ ${dir}`);
  } else {
    console.log(`   ❌ ${dir} (不存在)`);
    allPassed = false;
  }
});

// 检查 uploads 目录
if (!fs.existsSync(UPLOADS_DIR)) {
  console.log('\n📝 创建 uploads 目录...');
  try {
    fs.mkdirSync(UPLOADS_DIR, { recursive: true });
    console.log(`   ✅ 已创建：${UPLOADS_DIR}`);
  } catch (error) {
    console.log(`   ❌ 创建失败：${error.message}`);
    allPassed = false;
  }
}

// 检查技能文件
console.log('\n📄 技能文件');
const skillFiles = [
  'SKILL.md',
  'package.json',
  'scripts/publish.js'
];

const skillDir = path.join(__dirname, '..');
skillFiles.forEach(file => {
  const filePath = path.join(skillDir, file);
  if (fs.existsSync(filePath)) {
    console.log(`   ✅ ${file}`);
  } else {
    console.log(`   ❌ ${file} (缺失)`);
    allPassed = false;
  }
});

// 检查小红书登录状态
console.log('\n📕 小红书登录状态');
console.log('   ℹ️  请手动访问：https://creator.xiaohongshu.com/');
console.log('   ℹ️  确认已登录创作后台');

// 总结
console.log('\n' + '='.repeat(50));
if (allPassed) {
  console.log('✅ 环境检查通过！可以开始发布视频了。');
  console.log('\n📝 使用方法:');
  console.log('   node scripts/publish.js --video="视频路径" --title="标题"');
} else {
  console.log('❌ 环境检查失败，请先解决上述问题。');
  process.exit(1);
}

console.log('='.repeat(50));
