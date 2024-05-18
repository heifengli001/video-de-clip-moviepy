import os
import random
from moviepy.editor import VideoFileClip,ImageClip, concatenate_videoclips,CompositeVideoClip, vfx, clips_array
from moviepy.audio.fx.all import audio_normalize
from moviepy.video.fx.all import resize, speedx,rotate,margin,crop
from PIL import Image
import math
import warnings
from datetime import datetime
import itertools
# 忽略警告
warnings.filterwarnings("ignore")


# ============================= 以下为用户自定义参数 =========================
ratio = 16/9 # 视频比例  高/宽
video_width = 720 # 视频宽度的像素 
video_duration = None # 0.15*60 # 视频长度，如果为None 则视频长度以main.video为准
mask_opacity = 0.08 # 遮罩四个角视频的透明度
mask_zoom = 1.3 # 遮罩视频的缩放
new_video_count = 1 # 你想生成几个新视频? !important ,如果设置为None 则生成所有根据mask_videos素材所有组合的视频
main_video_name ='main.mp4' # 主视频名称
#  =======================================================================



# ############################## 系统定义内容 #########################
# 获取随机4位数组
def combinations_to_four(n):
    numbers = list(range(0, n))
    combinations = list(itertools.combinations(numbers, 4))
    return combinations

main_path = "main_videos"  # Your video path
video_path = "mask_videos"  # Your video path
gif_path = "mask_gifs"  # Your video path
output_path = "output"  # Output path

def printTime(str):
    # 获取当前日期和时间
    now = datetime.now()
    # 打印当前的日期和时间
    print(now.strftime("%Y-%m-%d %H:%M:%S"),'--',str)


output_index = 0
# 生成视频
def genrate_video(video_arr,gif_arr):
    
    mask_video_files = []
    # 遍历video_arr 取出video_groups的文件名称
    for item in video_arr:
        mask_video_files.append(video_files[item])

   
    clips = []
    for video_file in mask_video_files:
        # print("正在添加遮盖视频：%s" % video_file)
        clip = VideoFileClip(os.path.join(video_path, video_file)).resize(height=video_height_half*mask_zoom, width=video_width_half*mask_zoom).set_opacity(mask_opacity).set_audio(None)  # Resize to half the final size
        # 获取视频长度
        if(clip.duration > video_duration):
            clip = clip.subclip(0, video_duration)
        else:
            # 修改 clip的速度为
            clip = clip.fx(speedx, clip.duration/video_duration)
        clips.append(clip)

    # Arrange clips
    clip1, clip2, clip3, clip4 = clips

    clip1 = clip1.rotate(45,expand=True)
    clip2 = clip2.rotate(360-45,expand=True)
    clip3 = clip3.rotate(360-45,expand=True)
    clip4 = clip4.rotate(45,expand=True)

    clip1 = clip1.set_position((-offset,-offset))  # Top left corner
    clip2 = clip2.set_position((video_width_half,-offset))  # Top right corner
    clip3 = clip3.set_position((-offset,video_height_half))  # Bottom left corner
    clip4 = clip4.set_position((video_width_half,video_height_half))  # Bottom right corner


    mask_gif_files = []
    # 遍历video_arr 取出video_groups的文件名称
    for item in gif_arr:
        mask_gif_files.append(gif_files[item])

    gif_clips =[]
    for gif_file in mask_gif_files:
        # 打印当前时间
        gif_clip = VideoFileClip(os.path.join(gif_path,gif_file), has_mask=True).resize(height=100,width=100).set_start(0)
        gif_clip=gif_clip.subclip(0, round(gif_clip.duration-0.1,2))
        # 设置帧率为24
        gif_clip = gif_clip.set_fps(24)
        
        # 计算需要循环的次数，这里是简单地用视频时长除以GIF时长
        # 注意：这里的做法假设你想让GIF贯穿整个视频，如果GIF太长，你可能需要调整逻辑
        # 设置GIF循环5次
        # 定义a = 精确到gif_clip.duration 的 小数后两位
        
        
        
        loop_times = (int(video_duration / gif_clip.duration)+1 )
        gif_clip = gif_clip.fx(vfx.loop,n=loop_times)
        
        gif_clip=gif_clip.set_duration(video_duration)
        
        gif_clips.append(gif_clip)
        
    gif_clip1, gif_clip2, gif_clip3, gif_clip4 = gif_clips
    

    gif_clip1 = gif_clip1.set_position((0,0))  # Top left corner
    gif_clip2 = gif_clip2.set_position((video_width-100,0))  # Top right corner
    gif_clip3 = gif_clip3.set_position((0,video_height-100))  # Bottom left corner
    gif_clip4 = gif_clip4.set_position((video_width-100,video_height-100))  # Bottom right corner


    clips = [main_clip,clip1, clip2, clip3, clip4,gif_clip1,gif_clip2, gif_clip3, gif_clip4]
    # clips = [main_clip,clip1, clip2, clip3, clip4]

    # 将四个视频合并，并将视频设置尺寸为 video_width vide_height
    # 合并的时候不用裁切掉其他视频，而是叠放
    final_clip = CompositeVideoClip(clips, size=(video_width, video_height))


    # Set audio volume to 0
    # final_clip = final_clip.set_audio(final_clip.audio.fx(audio_normalize, 0))
    # final_clip = final_clip.set_audio(None)


    output_index = output_index+1
    # 写入文件，并优化写入方式，提高写入速度
    final_clip.write_videofile(os.path.join(output_path, "output"+output_index+".mp4"), codec="libx264", fps=24, threads=4, logger=None,preset='ultrafast')
    
    
    from PIL import Image


# #######################################################





# 获取 videos、gifs 文件夹下的所有mp4文件 并输出成文件名称，保留后缀
video_files = [f for f in os.listdir(video_path) if f.endswith(".mp4")]
gif_files = [f for f in os.listdir(gif_path) if f.endswith(".gif")]

# 如果videos_files 和 gif_files 都为空，则退出
if len(video_files) < 4 or len(gif_files) < 4:
    printTime("资源不够哦，请在videos和gifs目录下至少添加4个以上视频和动图")
    exit(0)

video_groups = combinations_to_four(len(video_files))
gif_groups = combinations_to_four(len(gif_files))


if new_video_count is None:
    new_video_count = len(video_groups)
elif new_video_count > len(video_groups):
    printTime("资源不够哦,你想生成的视频数量大于视频素材的组合数量，我们只能生成 %d 个视频" % len(video_groups))
    exit(0)



# ---------- 下方为系统计算 ------------
video_height = int(video_width * ratio)
video_width_half = int(video_width/2)
video_height_half = int(video_height/2)

# Calculate the length of the legs of an isosceles right triangle using the Pythagorean theorem

offset = int(math.sqrt(video_width_half**2/2))

# ---------- 遍历数组生成视频 ------------
printTime("总共将生成 %d 个视频" % new_video_count)


main_clip = VideoFileClip(os.path.join(main_path,main_video_name))
main_clip=main_clip.resize(height=video_height, width=video_width)

if video_duration is None:
    video_duration = main_clip.duration
else:
    main_clip = main_clip.subclip(0, video_duration)



# 循环生成视频
for i in range(new_video_count):
    # 从video_groups数组中随机选择一个，并移除
    video_arr = random.choice(video_groups)
    video_groups.remove(video_arr)
    
    gif_arr = random.choice(gif_groups)
    # video_arr = video_groups[i]
    printTime("开始生成：第 %d 个视频" % int(i+1))
    genrate_video(video_arr,gif_arr)
    printTime("生成完成：第 %d 个视频" % int(i+1))
