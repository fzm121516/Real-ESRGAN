import argparse
import glob
import os
import subprocess

# --------------- Arguments ---------------
parser = argparse.ArgumentParser(description='Test Images')
parser.add_argument('--videos-dir', type=str, required=True)
parser.add_argument('--images-dir', type=str, required=True)
parser.add_argument('--result-dir', type=str, required=True)

args = parser.parse_args()

# Load Videos
video_list = sorted(glob.glob(os.path.join(args.videos_dir, '**', '*.avi'), recursive=True))

num_video = len(video_list)
print("Find ", num_video, " images")

# Process
for i in range(num_video):
    video_path = video_list[i]
    video_name = os.path.basename(video_path)  # 获取文件名（包含扩展名）
    print(i, '/', num_video, video_name)

    images_dir = os.path.join(
        args.images_dir,
        os.path.relpath(video_path, args.videos_dir).rsplit(os.sep, 1)[0]
    )
    # Save results
    output_dir = os.path.join(
        args.result_dir,
        os.path.relpath(video_path, args.videos_dir).rsplit(os.sep, 1)[0]
    )
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 拼接保存路径并创建
    # save_path = os.path.join(output_dir, video_name)
    save_path = output_dir

    # 确保保存路径存在
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # 调用 RealESRGAN 推理
    subprocess.run(['python', 'inference_realesrgan.py', '-n', 'RealESRGAN_x4plus', '-i', images_dir, '-o', save_path])
