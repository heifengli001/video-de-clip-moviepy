# 使用moviepy对视频去重剪辑

> 去重原理，给原视频 四个角落分别增加可设透明度的其他视频和gif图层，类似一种遮罩
> 项目将mask_videos内的所有视频排列组合，取出所有的组合，组合内分别对应遮罩的四个角落，假设总共4个遮罩素材，则可以提供 4!=24个组合，那就能生成24个去重后的视频

## 技术栈
- `python`  `moviepy` `ffmpeg`

## 准备工作

使用前请先安装好环境

+ [python](https://www.python.org/)
+ [ffmpeg](https://ffmpeg.org/) 如果你是linux/MacOS 可以使用`brew install ffmpeg`进行安装
+ `moviepy` 安装命令 `pip install moviepy` 当然也可以选择 `aconada`安装

## 使用前素材准备

1. 将主视频放在 `/main_videos` 文件夹内
2. 遮罩层的视频素材放在 `/mask_videos` 文件夹内
3. 遮罩层的gif素材放在 `/mask_gifs` 文件夹内

> 需要注意的是遮罩素材 需要大于等于4个，以便于可以填充每个角落

## 运行

+ 运行命令 `python index.py`
+ 等待视频制作完成，去重后的视频将存放在 `output/` 文件夹内

## 代码内可配置项释义
> 你可在 `index.py` 文件的第15行找到这些配置内容


```
# ============================= 以下为用户自定义参数 =========================
ratio = 16/9 # 视频比例  高/宽
video_width = 720 # 视频宽度的像素 
video_duration = None # 0.15*60 # 视频长度，如果为None 则视频长度以main.video为准
mask_opacity = 0.08 # 遮罩视频的透明度
mask_zoom = 1.3 # 遮罩视频的缩放
new_video_count = 1 # 你想生成几个新视频? !important ,如果设置为None 则生成所有根据mask_videos素材所有组合的视频
main_video_name ='main.mp4' # 主视频名称
#  =======================================================================
```
