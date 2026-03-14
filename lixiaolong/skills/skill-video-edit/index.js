/**
 * skill-video-edit
 * 视频混剪 Skill - 自动化视频制作
 * 
 * 功能：
 * - 素材匹配和拼接
 * - 转场效果
 * - 字幕合成
 * - BGM 混音
 * - 封面生成
 */

const { exec } = require('child_process');
const fs = require('fs').promises;
const path = require('path');

// FFmpeg 路径检测
const FFMPEG_PATH = process.env.FFMPEG_PATH || 'ffmpeg';

/**
 * 检查 FFmpeg 是否可用
 */
async function checkFFmpeg() {
  return new Promise((resolve) => {
    exec(`${FFMPEG_PATH} -version`, (error) => {
      resolve(!error);
    });
  });
}

/**
 * 视频拼接
 */
async function concatVideos(videoFiles, outputPath) {
  console.log('[视频编辑] 开始拼接视频...');
  
  // 创建文件列表
  const listFile = path.join(path.dirname(outputPath), 'video_list.txt');
  const listContent = videoFiles.map(f => `file '${f}'`).join('\n');
  await fs.writeFile(listFile, listContent);
  
  return new Promise((resolve, reject) => {
    const cmd = `${FFMPEG_PATH} -f concat -safe 0 -i "${listFile}" -c copy "${outputPath}"`;
    exec(cmd, async (error, stdout, stderr) => {
      if (error) {
        reject(error);
      } else {
        // 清理临时文件
        await fs.unlink(listFile);
        console.log('[视频编辑] 拼接完成:', outputPath);
        resolve(outputPath);
      }
    });
  });
}

/**
 * 添加转场效果
 */
async function addTransition(inputPath, outputPath, transition = 'fade', duration = 1) {
  console.log('[视频编辑] 添加转场效果...');
  
  return new Promise((resolve, reject) => {
    const cmd = `${FFMPEG_PATH} -i "${inputPath}" -vf "${transition},duration=${duration}" "${outputPath}"`;
    exec(cmd, (error) => {
      if (error) reject(error);
      else {
        console.log('[视频编辑] 转场完成:', outputPath);
        resolve(outputPath);
      }
    });
  });
}

/**
 * 添加字幕
 */
async function addSubtitle(inputPath, outputPath, subtitleText, options = {}) {
  console.log('[视频编辑] 添加字幕...');
  
  const {
    fontSize = 24,
    fontColor = 'white',
    position = 'bottom',
    backgroundColor = 'black@0.5'
  } = options;
  
  return new Promise((resolve, reject) => {
    // 简单的字幕添加（复杂字幕需要 .srt 文件）
    const cmd = `${FFMPEG_PATH} -i "${inputPath}" -vf "drawtext=text='${subtitleText}':fontsize=${fontSize}:fontcolor=${fontColor}:box=1:boxcolor=${backgroundColor}" "${outputPath}"`;
    exec(cmd, (error) => {
      if (error) reject(error);
      else {
        console.log('[视频编辑] 字幕完成:', outputPath);
        resolve(outputPath);
      }
    });
  });
}

/**
 * 添加背景音乐
 */
async function addBGM(videoPath, bgmPath, outputPath, volume = 0.3) {
  console.log('[视频编辑] 添加背景音乐...');
  
  return new Promise((resolve, reject) => {
    const cmd = `${FFMPEG_PATH} -i "${videoPath}" -i "${bgmPath}" -c:v copy -c:a aac -b:a 192k -filter_complex "[1:a]volume=${volume}[bgm];[0:a][bgm]amix=inputs=2:duration=first" "${outputPath}"`;
    exec(cmd, (error) => {
      if (error) reject(error);
      else {
        console.log('[视频编辑] BGM 完成:', outputPath);
        resolve(outputPath);
      }
    });
  });
}

/**
 * 生成封面
 */
async function generateCover(videoPath, outputPath, timestamp = '00:00:01') {
  console.log('[视频编辑] 生成封面...');
  
  return new Promise((resolve, reject) => {
    const cmd = `${FFMPEG_PATH} -i "${videoPath}" -ss ${timestamp} -vframes 1 "${outputPath}"`;
    exec(cmd, (error) => {
      if (error) reject(error);
      else {
        console.log('[视频编辑] 封面完成:', outputPath);
        resolve(outputPath);
      }
    });
  });
}

/**
 * 调整视频尺寸
 */
async function resizeVideo(inputPath, outputPath, width = 1080, height = 1920) {
  console.log('[视频编辑] 调整视频尺寸...');
  
  return new Promise((resolve, reject) => {
    const cmd = `${FFMPEG_PATH} -i "${inputPath}" -vf "scale=${width}:${height}" "${outputPath}"`;
    exec(cmd, (error) => {
      if (error) reject(error);
      else {
        console.log('[视频编辑] 尺寸调整完成:', outputPath);
        resolve(outputPath);
      }
    });
  });
}

/**
 * 裁剪视频
 */
async function trimVideo(inputPath, outputPath, startTime, duration) {
  console.log('[视频编辑] 裁剪视频...');
  
  return new Promise((resolve, reject) => {
    const cmd = `${FFMPEG_PATH} -i "${inputPath}" -ss ${startTime} -t ${duration} -c copy "${outputPath}"`;
    exec(cmd, (error) => {
      if (error) reject(error);
      else {
        console.log('[视频编辑] 裁剪完成:', outputPath);
        resolve(outputPath);
      }
    });
  });
}

/**
 * 完整的视频制作流程
 */
async function createVideo(params) {
  const {
    clips = [],        // 视频片段 [{path, startTime, duration}]
    bgm,              // 背景音乐路径
    subtitles = [],   // 字幕 [{text, startTime, duration}]
    outputPath,       // 输出路径
    options = {}      // 其他选项
  } = params;
  
  console.log('🎬 开始制作视频...');
  console.log(`   片段数：${clips.length}`);
  console.log(`   BGM: ${bgm ? '是' : '否'}`);
  console.log(`   字幕数：${subtitles.length}`);
  console.log(`   输出：${outputPath}`);
  
  const tempDir = path.join(path.dirname(outputPath), 'temp');
  await fs.mkdir(tempDir, { recursive: true });
  
  try {
    // 1. 裁剪视频片段
    console.log('\n[步骤 1] 裁剪视频片段...');
    const trimmedClips = [];
    for (let i = 0; i < clips.length; i++) {
      const clip = clips[i];
      const trimmedPath = path.join(tempDir, `clip_${i}.mp4`);
      await trimVideo(clip.path, trimmedPath, clip.startTime || '0', clip.duration || 10);
      trimmedClips.push(trimmedPath);
    }
    
    // 2. 拼接视频
    console.log('\n[步骤 2] 拼接视频...');
    const mergedPath = path.join(tempDir, 'merged.mp4');
    await concatVideos(trimmedClips, mergedPath);
    
    // 3. 添加字幕（简化：只添加第一个字幕）
    let finalPath = mergedPath;
    if (subtitles.length > 0) {
      console.log('\n[步骤 3] 添加字幕...');
      finalPath = path.join(tempDir, 'with_subtitles.mp4');
      await addSubtitle(mergedPath, finalPath, subtitles[0].text);
    }
    
    // 4. 添加 BGM
    if (bgm) {
      console.log('\n[步骤 4] 添加背景音乐...');
      const withBgmPath = path.join(tempDir, 'with_bgm.mp4');
      await addBGM(finalPath, bgm, withBgmPath);
      finalPath = withBgmPath;
    }
    
    // 5. 生成封面
    console.log('\n[步骤 5] 生成封面...');
    const coverPath = outputPath.replace('.mp4', '_cover.jpg');
    await generateCover(finalPath, coverPath);
    
    // 6. 移动到最终位置
    console.log('\n[步骤 6] 保存最终视频...');
    await fs.rename(finalPath, outputPath);
    
    // 清理临时文件
    await fs.rm(tempDir, { recursive: true, force: true });
    
    console.log('\n✅ 视频制作完成！');
    console.log(`   输出：${outputPath}`);
    console.log(`   封面：${coverPath}`);
    
    return {
      success: true,
      videoPath: outputPath,
      coverPath: coverPath,
      duration: clips.reduce((sum, c) => sum + (c.duration || 10), 0)
    };
    
  } catch (error) {
    console.error('❌ 视频制作失败:', error.message);
    
    // 清理临时文件
    try {
      await fs.rm(tempDir, { recursive: true, force: true });
    } catch (e) {}
    
    return {
      success: false,
      error: error.message
    };
  }
}

/**
 * 主函数
 */
async function main(params = {}) {
  console.log('🎬 视频编辑 Skill');
  console.log('=' .repeat(50));
  
  // 检查 FFmpeg
  const hasFFmpeg = await checkFFmpeg();
  if (!hasFFmpeg) {
    return {
      success: false,
      error: 'FFmpeg 未安装或未找到。请安装 FFmpeg 或设置 FFMPEG_PATH 环境变量。'
    };
  }
  
  console.log('✅ FFmpeg 检查通过');
  
  // 执行视频制作
  const result = await createVideo(params);
  
  return result;
}

module.exports = {
  main,
  createVideo,
  concatVideos,
  addTransition,
  addSubtitle,
  addBGM,
  generateCover,
  resizeVideo,
  trimVideo,
  checkFFmpeg
};
