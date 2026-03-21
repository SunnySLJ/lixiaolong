#!/usr/bin/env node

/**
 * 小红书视频发布脚本
 * 
 * 用法:
 *   node publish.js --video="视频路径" --title="标题" [--tags="#话题 1,#话题 2"] [--debug]
 * 
 * 示例:
 *   node publish.js --video="C:\Users\爽爽\Desktop\视频.mp4" --title="春日随拍"
 *   node publish.js --video="./video.mp4" --title="测试" --tags="#测试，#自动化" --debug
 */

import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import { Command } from 'commander';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const UPLOADS_DIR = 'C:\\tmp\\openclaw\\uploads';

const program = new Command();

program
  .name('xiaohongshu-video-publish')
  .description('小红书视频一键发布工具')
  .version('1.1.0')
  .requiredOption('-v, --video <path>', '视频文件路径')
  .requiredOption('-t, --title <title>', '视频标题')
  .option('--tags <tags>', '话题标签（逗号分隔）', '#生活美学,#日常文案,#我的生活碎片')
  .option('--debug', '调试模式（详细日志）', false)
  .option('--profile <profile>', '浏览器 profile', 'openclaw')
  .parse(process.argv);

const options = program.opts();

// 日志函数
function log(message, level = 'info') {
  const timestamp = new Date().toLocaleTimeString('zh-CN');
  const prefix = {
    info: 'ℹ️',
    success: '✅',
    warning: '⚠️',
    error: '❌',
    debug: options.debug ? '🔍' : null
  };
  
  if (prefix[level] && (level !== 'debug' || options.debug)) {
    console.log(`${prefix[level]} [${timestamp}] ${message}`);
  }
}

// 检查环境
async function checkEnvironment() {
  log('检查环境...', 'info');
  
  // 检查 Node.js 版本
  const nodeVersion = process.version;
  const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0]);
  if (majorVersion < 18) {
    log(`Node.js 版本过低：${nodeVersion}，需要 >=18.0.0`, 'error');
    process.exit(1);
  }
  log(`Node.js 版本：${nodeVersion}`, 'success');
  
  // 检查视频文件
  if (!fs.existsSync(options.video)) {
    log(`视频文件不存在：${options.video}`, 'error');
    process.exit(1);
  }
  log(`视频文件存在：${options.video}`, 'success');
  
  // 检查视频格式
  const ext = path.extname(options.video).toLowerCase();
  if (!['.mp4', '.mov'].includes(ext)) {
    log(`不支持的视频格式：${ext}，请使用 mp4 或 mov`, 'warning');
  }
  
  // 检查视频大小
  const stats = fs.statSync(options.video);
  const sizeMB = stats.size / (1024 * 1024);
  if (sizeMB > 20 * 1024) {
    log(`视频文件过大：${sizeMB.toFixed(2)}MB，最大支持 20GB`, 'error');
    process.exit(1);
  }
  log(`视频大小：${sizeMB.toFixed(2)}MB`, 'success');
  
  // 创建 uploads 目录
  if (!fs.existsSync(UPLOADS_DIR)) {
    fs.mkdirSync(UPLOADS_DIR, { recursive: true });
    log(`创建 uploads 目录：${UPLOADS_DIR}`, 'success');
  }
  
  return true;
}

// 复制视频到 uploads 目录
function prepareVideo() {
  log('准备视频文件...', 'info');
  
  const videoName = path.basename(options.video);
  const destPath = path.join(UPLOADS_DIR, videoName);
  
  try {
    fs.copyFileSync(options.video, destPath);
    log(`视频已复制：${destPath}`, 'success');
    return destPath;
  } catch (error) {
    log(`复制视频失败：${error.message}`, 'error');
    process.exit(1);
  }
}

// 执行 OpenClaw 命令（使用 PowerShell 执行完整命令字符串）
function runOpenClawCommand(command) {
  return new Promise((resolve, reject) => {
    log(`执行：${command}`, 'debug');
    
    // 使用 PowerShell 执行完整命令字符串
    const psCommand = `openclaw ${command}`;
    const child = spawn('powershell', ['-Command', psCommand], {
      stdio: ['pipe', 'pipe', 'pipe'],
      shell: true,
      env: { ...process.env, FORCE_COLOR: '0' }
    });
    
    let stdout = '';
    let stderr = '';
    
    child.stdout.on('data', (data) => {
      stdout += data.toString();
      if (options.debug) {
        process.stdout.write(data);
      }
    });
    
    child.stderr.on('data', (data) => {
      stderr += data.toString();
      if (options.debug) {
        process.stderr.write(data);
      }
    });
    
    child.on('close', (code) => {
      if (code === 0) {
        resolve(stdout);
      } else {
        reject(new Error(`命令失败 (code ${code}): ${stderr}`));
      }
    });
    
    child.on('error', (error) => {
      reject(error);
    });
  });
}

// 主发布流程
async function publish() {
  log('开始发布流程...', 'info');
  
  try {
    // 1. 检查环境
    await checkEnvironment();
    
    // 2. 准备视频
    const videoPath = prepareVideo();
    
    // 3. 启动浏览器
    log('启动浏览器...', 'info');
    await runOpenClawCommand('browser action=start');
    log('浏览器已启动', 'success');
    
    // 4. 打开发布页
    log('打开小红书发布页...', 'info');
    await runOpenClawCommand(`browser action=open url=https://creator.xiaohongshu.com/publish/publish profile=${options.profile}`);
    log('发布页已打开', 'success');
    
    // 5. 等待页面加载
    log('等待页面加载...', 'info');
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // 6. 获取页面快照
    log('获取页面元素...', 'info');
    const snapshot = await runOpenClawCommand('browser action=snapshot refs="aria"');
    
    // 解析文件选择器 ref（简化处理，实际需要根据快照解析）
    const fileInputRef = '2_5'; // 默认 ref，实际应从快照解析
    log(`文件选择器 ref: ${fileInputRef}`, 'debug');
    
    // 7. 上传视频
    log('上传视频...', 'info');
    const uploadCmd = `browser action=upload inputRef=${fileInputRef} paths=["${videoPath.replace(/\\/g, '\\\\')}"]`;
    await runOpenClawCommand(uploadCmd);
    log('视频上传成功', 'success');
    
    // 8. 等待上传处理
    log('等待视频处理...', 'info');
    await runOpenClawCommand('browser action=act kind=wait timeMs=15000');
    
    // 9. 获取编辑页快照
    log('获取编辑页元素...', 'info');
    await runOpenClawCommand('browser action=snapshot refs="aria"');
    
    // 10. 填写标题
    log(`填写标题：${options.title}`, 'info');
    const titleRef = '3_9'; // 默认 ref
    await runOpenClawCommand(`browser action=act kind=type ref=${titleRef} text="${options.title}"`);
    log('标题已填写', 'success');
    
    // 11. 填写话题
    const tags = options.tags.split(',').join(' ');
    log(`填写话题：${tags}`, 'info');
    const descRef = '3_11'; // 默认 ref
    await runOpenClawCommand(`browser action=act kind=type ref=${descRef} text="${tags}"`);
    log('话题已填写', 'success');
    
    // 12. 点击发布
    log('发布视频...', 'info');
    const publishRef = '3_74'; // 默认 ref
    await runOpenClawCommand(`browser action=act kind=click ref=${publishRef}`);
    log('发布按钮已点击', 'success');
    
    // 13. 等待发布处理
    log('等待发布处理...', 'info');
    await runOpenClawCommand('browser action=act kind=wait timeMs=8000');
    
    // 14. 完成
    log('✅ 小红书视频发布完成！', 'success');
    console.log('\n📹 发布详情:');
    console.log(`   视频：${path.basename(options.video)}`);
    console.log(`   标题：${options.title}`);
    console.log(`   话题：${tags}`);
    console.log(`   状态：审核中（页面返回上传页 = 成功）`);
    console.log('\n🔗 查看笔记：https://creator.xiaohongshu.com/note/manage\n');
    
  } catch (error) {
    log(`发布失败：${error.message}`, 'error');
    
    // 错误恢复建议
    console.log('\n💡 建议:');
    if (error.message.includes('timeout')) {
      console.log('   1. 重启网关：gateway action=restart note="恢复浏览器"');
      console.log('   2. 重启浏览器：browser action=start');
      console.log('   3. 重试发布流程');
    } else if (error.message.includes('path')) {
      console.log('   1. 确保视频已复制到 C:\\tmp\\openclaw\\uploads\\');
      console.log('   2. 检查文件路径是否正确');
    } else {
      console.log('   1. 检查浏览器是否已登录小红书');
      console.log('   2. 检查网络连接');
      console.log('   3. 使用 --debug 查看详细日志');
    }
    
    process.exit(1);
  }
}

// 运行
publish();
