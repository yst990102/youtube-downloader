from flask import Flask, request, redirect, render_template, jsonify
from pytube import YouTube
from pathlib import Path
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/download", methods=["GET", "POST"])
def download_video():
    if request.method == 'POST' and 'video_url' in request.form:
        youtube_url = request.form["video_url"]
        if youtube_url:
            url = YouTube(youtube_url)
            
            selected_quality = request.form['selected_stream']
            selected_stream = None
            
            for stream in url.streams:
                value = f"{stream}"
                if value == selected_quality:
                    selected_stream = stream
                    break
            
            if selected_stream:
                # 构建直接下载链接
                direct_download_link = selected_stream.url
                return render_template('download.html', direct_download_link=direct_download_link)
            else:
                message = 'Selected stream is not available for download'
                return render_template('index.html', message=message)
        else:
            message = 'Please enter YouTube Video URL.'
            return render_template('index.html', message=message)
    return render_template('index.html')

@app.route("/redirect_download", methods=["GET"])
def redirect_download():
    direct_download_link = request.args.get('url', '')
    return redirect(direct_download_link)

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
    app.run(host="0.0.0.0", port=5000, debug=True)
