from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from pytubefix import YouTube
from pytubefix.cli import on_progress
import requests
import json


def home(request):
    if request.method == "POST":
        url = request.POST.get("url")
        yt = YouTube(url, on_progress_callback = on_progress)
        streams = yt.streams.filter(progressive=True, file_extension="mp4")
        video_info = []
        for resolution in ['144p', '240p', '360p', '480p', '720p']:
            stream = streams.filter(res=resolution).first()
            if stream:
                video_info.append({
                    'resolution': resolution,
                    'size': f"{stream.filesize / 1024 / 1024:.2f} MB",
                    'download_url': stream.url
                })
        return render(request, 'video_info.html', {'video_info': video_info, 'title': yt.title})
    return render(request, 'index.html')


@csrf_exempt
def proxy(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data.get('url')
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', 'application/octet-stream')
            response_to_client = HttpResponse(response.content, content_type=content_type)
            response_to_client['Content-Disposition'] = f'attachment; filename="video.mp4"'
            return response_to_client
        else:
            return HttpResponse("Error: Could not retrieve video", status=response.status_code)
    return HttpResponse("")