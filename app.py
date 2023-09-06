from flask import Flask, request, render_template, jsonify
from pytube import YouTube
from pathlib import Path
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/download", methods=["GET", "POST"])
def downloadVideo():
    message = ''
    errorType = 0
    
    if request.method == 'POST' and 'video_url' in request.form:
        youtubeUrl = request.form["video_url"]
        if youtubeUrl:
            url = YouTube(youtubeUrl)
            
            # 获取用户选择的清晰度和格式
            selected_quality = request.form['selected_stream']
            selected_stream = None
            
            # 根据用户选择的清晰度和格式筛选视频流
            for stream in url.streams:
                value = f"{stream}"
                if value == selected_quality:
                    selected_stream = stream
                    break
            
            if selected_stream:
                downloadFolder = str(os.path.join(Path.home(), "Downloads"))
                if selected_stream.resolution:
                    selected_stream.download(output_path=downloadFolder, filename_prefix=f"{selected_stream.resolution}_")
                else:
                    selected_stream.download(output_path=downloadFolder, filename_prefix=f"{selected_stream.abr}_")
                message = f'Video Downloaded Successfully in {downloadFolder}!'
                errorType = 0
            else:
                message = 'Selected stream is not available for download'
                errorType = 1
        else:
            message = 'Please enter YouTube Video URL.'
            errorType = 2
    return render_template('index.html', message=message, errorType=errorType)

@app.route("/get_quality", methods=["GET"])
def get_quality():
    video_url = request.args.get("url")
    if not video_url:
        return jsonify({"options": {"video": [], "audio": []}})
    
    url = YouTube(video_url)
    
    # 获取所有可用的视频流和音频流，将视频清晰度和格式对应起来
    available_streams = url.streams
    
    # 初始化 video 和 audio 的选项列表
    video_options = []
    audio_options = []
    
    # 将流按类型分类
    for stream in available_streams:
        if stream.type == "video":
            video_options.append({
            "value": f"{stream}",
            "res": f"{stream.resolution}",
            "subtype": f"{stream.subtype}",
            "label": f"{stream.resolution} - {stream.subtype}"
        })
        elif stream.type == "audio":
            audio_options.append({
            "value": f"{stream}",
            "abr": f"{stream.abr}",
            "subtype": f"{stream.subtype}",
            "label": f"{stream.abr} - {stream.subtype}"
        })
    
    # label去重
    def remove_duplicates(options, type):
        unique_options = []
        seen = set()
        for option in options:
            if option['label'] not in seen:
                unique_options.append(option)
                seen.add(option['label'])
        return unique_options

    video_options = sorted(remove_duplicates(video_options, type="video"), key=lambda x: (int(x["res"].replace('p', '')), x["subtype"]))
    
    audio_options = sorted(remove_duplicates(audio_options, type="audio"), key=lambda x: (int(x["abr"].replace('kbps', '')), x["subtype"]))

    return jsonify({"video": video_options, "audio": audio_options})

if __name__ == "__main__":
    app.run()
