import cv2
import os
from tqdm import tqdm
import numpy as np
import modules.scripts as scripts
import gradio as gr

def ui_frame2video(image_folder,ouput_dir,fps,mode):
    print("\n IS-NET_pro:frame2video generating...")
    if mode =='.mp4':
        return frame2video(image_folder,ouput_dir,fps)
    elif mode == '.avi':
        return frame2video_alpga(image_folder,ouput_dir,fps)



def video2frame(video_path,output_folder,aim_fps_checkbox,aim_fps,time_range_checkbox,start_time,end_time):
    print("\n v2f:video2frame generating...")

    # 读取视频文件
    # video_path = 'path/to/video.mp4'
    cap = cv2.VideoCapture(video_path)

    # 检查视频是否成功打开
    if not cap.isOpened():
        print("Error opening video file")

    # 创建输出文件夹
    # output_folder = 'path/to/output'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    fps = cap.get(cv2.CAP_PROP_FPS)
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    ## 两种情况运行和不允许
    if aim_fps_checkbox:
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        # 这个问题是关于视频转图片的方法。首先，我们需要知道视频的帧率（fps），
        # 即每秒钟播放的帧数。然后，我们可以计算每个输出图片之间的时间间隔，即 
        # 1/fps。接着，我们需要确定每个输出图片所在的时间点。为了做到这一点，我
        # 们可以将输出图片的序号乘以时间间隔，然后将结果乘以视频的帧率，再向下取整
        # ，就可以得到输出图片所对应的视频帧。最后，我们只需要将这些视频帧保存为图片即可。
        total_output_frames = int( total_frames * aim_fps / video_fps)

    # 生成需要输出的帧的索引
        if time_range_checkbox:
            frame_indexes = np.linspace(max(start_frame,0), total_frames - 1, min(int( (end_time-start_time) * aim_fps),end_frame), dtype=np.int)
        else :
            frame_indexes = np.linspace(0, total_frames - 1, total_output_frames, dtype=np.int)
        frame_count = 1
        for i in tqdm(frame_indexes):
        # 设置读取帧的位置
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            # 读取帧并保存为图片
            ret, frame = cap.read()
            if ret:
                # 指定输出文件名
                output_file = os.path.join(output_folder, f'{frame_count:04d}.png')
                # print('\r geneframe:',output_file,end='')

                # 保存帧到输出文件
                cv2.imwrite(output_file, frame)
                frame_count += 1
    else:
        # 逐帧读取视频并保存到输出文件夹
        frame_count = 1
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        for i in tqdm(range(num_frames)):
            # 读取一帧
            ret, frame = cap.read()

            # 检查是否成功读取帧
            if not ret:
                break
            if (i >= start_frame and i <= end_frame) or (not time_range_checkbox):
            # 指定输出文件名
                output_file = os.path.join(output_folder, f'{frame_count:04d}.png')
                # print('\r geneframe:',output_file,end='')

                # 保存帧到输出文件
                cv2.imwrite(output_file, frame)

                # 更新帧计数器
                frame_count += 1

    # 释放视频对象
    cap.release()
    print('\n:) done!')

    return ":) done"
    
def frame2video(image_folder,ouput_dir,fps):
    # 读取图像文件列表
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.png') or f.endswith('.jpg')]
    image_files.sort()

    # 获取图像的宽度和高度
    img = cv2.imread(os.path.join(image_folder, image_files[0]),cv2.IMREAD_UNCHANGED)
    height, width, _ = img.shape

    # 创建输出视频对象
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(ouput_dir+'/output.mp4', fourcc, fps, (width, height), isColor=True)
    num_images = len(image_files)
    frame_num = 0
    # 逐帧写入视频帧
    for image_file in tqdm(image_files):
        image_path = os.path.join(image_folder, image_file)
        frame = cv2.imread(image_path)
        out.write(frame)
        frame_num +=1
        # print('\r generating video:',f'{100*frame_num/num_images:5.2f}%',end='')

    # 释放视频对象
    out.release()
    print('\n:) done!')
    return ":) done"


def frame2video_alpga(image_folder,ouput_dir,fps):
    # 读取图像文件列表
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.png') or f.endswith('.jpg')]
    image_files.sort()

    # 获取图像的宽度和高度
    img = cv2.imread(os.path.join(image_folder, image_files[0]),cv2.IMREAD_UNCHANGED)
    height, width, _ = img.shape

    # 创建输出视频对象
    # 格式表在这里：自己查一下对照表
    # https://learn.microsoft.com/en-us/windows/win32/medfound/video-fourccs
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(ouput_dir+'/output.avi', fourcc, fps, (width, height), isColor=True)
    num_images = len(image_files)
    frame_num = 0
    # 逐帧写入视频帧
    for image_file in tqdm(image_files):
        image_path = os.path.join(image_folder, image_file)
        frame = cv2.imread(image_path)
        out.write(frame)
        frame_num +=1
        # print('\r generating video:',f'{100*frame_num/num_images:5.2f}%',end='')

    # 释放视频对象
    out.release()
    print('\n:) done!')
    return ":) done"






class Script(scripts.Script):
    def title(self):
        return "(Gamma) frame_generator & video_generator"

    def show(self, is_img2img):
        return is_img2img

    def ui(self, is_img2img):
        with gr.Column(variant='panel'):
            gr.Markdown(""" 
            ## 视频生成'帧'\\video2frame
            在下面上传你的视频吧\\upload your video  
            注意！安装路径中有中文或者视频路径中有中文都容易报错！
            """)
            video_input_dir = gr.Video(lable='上传视频\\upload video',source='upload',interactive=True)
            video_input_dir.style(width=300)
            with gr.Row(variant='panel'):
                aim_fps_checkbox = gr.Checkbox(label="启用输出帧率控制\\enable the ouput fps control")
                aim_fps = gr.Slider(
                    minimum=1,
                    maximum=60,
                    step=1,
                    label='输出帧率\\output fps',
                    value=30,interactive=True)
            with gr.Row(variant='panel'):
                time_range_checkbox = gr.Checkbox(label="启用时间段裁剪\\enable video cut")
                aim_start_time = gr.Number(value=0,label="裁剪起始时间(s)\\start_time",)
                aim_end_time = gr.Number(value=0,label="裁剪停止时间(s)\\end_time")
            frame_output_dir = gr.Textbox(label='图片输出地址\\Frame Output directory', lines=1,placeholder='output\\folder')
            btn = gr.Button(value="gene_frame")
            out = gr.Textbox(label="log info",interactive=False,visible=True,placeholder="output log")
            btn.click(video2frame, inputs=[video_input_dir, frame_output_dir,aim_fps_checkbox,aim_fps,time_range_checkbox,aim_start_time,aim_end_time],outputs=out)
# with gr.TabItem(label='video2frame'):
#     with gr.Row(variant='panel'):
        with gr.Column(variant='panel'):
            gr.Markdown(""" 
            ## 帧生成'视频'\\frame2video
            由图片转化为视频，注意这里只需要给出生成视频的地址即可，不要文件名！！！！  
            本拓展由 [_星瞳毒唯](https://space.bilibili.com/113557956)编写  
            本拓展GitHub项目在 [_github_sd-webui-IS-NET-pro](https://github.com/ClockZinc/sd-webui-IS-NET-pro)  
            本拓展使用的算法有使用的DIS的开源项目 [_github_DIS](https://github.com/xuebinqin/DIS)  
            有任何问题均可b站私信我,我看心情回答,本项目不收取任何费用！！  
            
            """)
            fps = gr.Slider(
                minimum=1,
                maximum=60,
                step=1,
                label='FPS',
                value=30)
            frame_input_dir = gr.Textbox(label='图片输入地址\\Frame Input directory', lines=1,placeholder='input\\folder')
            video_output_dir = gr.Textbox(label='视频输出地址\\Video Output directory', lines=1,placeholder='output\\folder')
            f2v_mode = gr.Dropdown(
                label="video out",
                choices=[
                    '.mp4',
                    '.avi',
                    ],
                value='.mp4')
            btn1 = gr.Button(value="gene_video")
            out1 = gr.Textbox(label="log info",interactive=False,visible=True,placeholder="output log")

            btn1.click(ui_frame2video, inputs=[frame_input_dir, video_output_dir,fps,f2v_mode],outputs=out1)



if __name__ == '__main__':
    # image_folder = r"D:\Doctoral_Career\Little_interest\novelAI\SD_img2img_Video\test\course2\output4"
    # ouput_dir = r"D:\Doctoral_Career\Little_interest\novelAI\SD_img2img_Video\test\course2\output4"
    # fps = 30
    video2frame(r'D:\Doctoral_Career\Little_interest\novelAI\SD_img2img_Video\test\course1\luming.mp4',r'D:\Doctoral_Career\Little_interest\novelAI\SD_img2img_Video\test\course1\output2',True,15,True ,0,1)