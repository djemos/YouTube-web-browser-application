import os
import re
import base64
import glob
from typing import List, Optional
from fastapi import FastAPI, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from yt_dlp import YoutubeDL

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

download_progress = {}
# Temporary storage directory for completed files on the server
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads_temp")
os.makedirs(OUTPUT_DIR, exist_ok=True)

MAX_RESULTS = 200

# IN-MEMORY CACHE: Stores the last search result list per query string
search_cache = {}

# CLEANING UP ORPHANED FILES ON SERVER STARTUP
try:
    for old_file in glob.glob(os.path.join(OUTPUT_DIR, "*")):
        os.remove(old_file)
    print("🔥 The downloads_temp folder was successfully cleared on startup!")
except Exception as e:
    print(f"Cleanup error: {e}")

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h3>The index.html file was not found!</h3>"

def search_youtube_with_ytdlp(query: str, limit: int = MAX_RESULTS):
    ydl_opts = {
        'extract_flat': True,
        'skip_download': True,
        'quiet': True,
        'playlistend': limit
    }
    results = []
    s_prefix = base64.b64decode("eXRzZWFyY2g=").decode("utf-8")
    search_url = f"{s_prefix}{limit}:{query}"
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_url, download=False)
            if 'entries' in info:
                for entry in info['entries']:
                    if not entry: continue
                    video_id = entry.get('id')
                    if not video_id: continue
                    clean_match = re.match(r'^([a-zA-Z0-9_-]{11})', video_id)
                    if not clean_match: continue
                    video_id = clean_match.group(1)
                    
                    results.append({
                        "id": video_id,
                        "title": entry.get('title', 'Unknown Title'),
                        "channel": entry.get('uploader', 'Unknown Channel'),
                        "duration": f"{divmod(int(entry.get('duration', 0)), 60)[0]}:{divmod(int(entry.get('duration', 0)), 60)[1]:02d}" if entry.get('duration') else "N/A"
                    })
        return results
    except Exception as e:
        return []

def download_youtube_video(video_id: str, mode: str):
    v_prefix = base64.b64decode("aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g/dj0=").decode("utf-8")
    url = f"{v_prefix}{video_id}"
    
    download_progress[video_id] = {"status": "downloading", "percent": 0, "file": ""}

    def progress_hook(d):
        if d['status'] == 'downloading':
            percent_str = re.sub(r'\x1b\[[0-9;]*m', '', d.get('_percent_str', '0%')).strip().replace('%', '')
            try:
                download_progress[video_id]["percent"] = int(float(percent_str))
            except ValueError:
                pass
        elif d['status'] == 'finished':
            download_progress[video_id]["percent"] = 100

    ydl_opts = {
        'outtmpl': os.path.join(OUTPUT_DIR, f"{video_id}_%(title)s.%(ext)s"),
        'progress_hooks': [progress_hook],
        'quiet': True
    }
    
    if mode == 'mp3':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '0',
            }],
        })
    else:
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        })
        
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        search_pattern = os.path.join(OUTPUT_DIR, f"{video_id}_*")
        found = glob.glob(search_pattern)
        if found:
            download_progress[video_id] = {"status": "finished", "percent": 100, "file": os.path.basename(found[0])}
        else:
            download_progress[video_id] = {"status": "error", "percent": 0, "file": ""}
    except Exception as e:
        download_progress[video_id] = {"status": "error", "percent": 0, "file": ""}

@app.get("/search")
def search(q: str = Query(..., description="Search query string")):
    videos = search_youtube_with_ytdlp(q)
    if videos:
        search_cache[q] = videos  # Cache the latest search list in memory
    return {"status": "success" if videos else "error", "results": videos}

# UPDATED: Handles both Search list and Favorites continuous track transitions
@app.get("/next")
def play_next_video(
    current_id: str = Query(..., description="The ID of the video currently playing"),
    q: Optional[str] = Query(None, description="The original search query to find the list"),
    list_type: str = Query("search", description="Context list type: 'search' or 'favorites'"),
    fav_ids_string: Optional[str] = Query(None, description="Comma-separated string of favorite IDs")
):
    videos = []
    
    # 1. FETCH LIST BASED ON QUEUE TYPE
    if list_type == "favorites" and fav_ids_string:
        # Split the string by commas to extract clean IDs
        id_list = [vid_id.strip() for vid_id in fav_ids_string.split(",") if vid_id.strip()]
        for vid_id in id_list:
            videos.append({"id": vid_id, "title": "Favorite Track", "channel": "", "duration": ""})
    else:
        # Fallback to search memory cache
        if q:
            videos = search_cache.get(q)
            if not videos:
                videos = search_youtube_with_ytdlp(q)
                if videos:
                    search_cache[q] = videos

    if not videos:
        return {"status": "error", "message": f"No active queue playlist found for list type: {list_type}"}

    # 2. FIND POSITION OF THE CURRENT VIDEO
    current_idx = next((i for i, video in enumerate(videos) if video["id"] == current_id), -1)

    if current_idx == -1:
        return {"status": "error", "message": "Current video not found in active playlist view context"}
        
    if current_idx + 1 >= len(videos):
        return {"status": "end_of_playlist", "message": "You have reached the end of the tracking list"}

    # Return the next video
    return {"status": "success", "next_video": videos[current_idx + 1]}


@app.get("/download")
def download(video_id: str, mode: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(download_youtube_video, video_id, mode)
    return {"status": "started"}

@app.get("/progress")
def get_progress(video_id: str = Query(..., description="The ID of the video to check")):
    return download_progress.get(video_id, {"status": "idle", "percent": 0, "file": ""})

@app.get("/get-file")
def get_file(file_name: str, background_tasks: BackgroundTasks):
    file_path = os.path.join(OUTPUT_DIR, file_name)
    if os.path.exists(file_path):
        background_tasks.add_task(lambda path: os.remove(path) if os.path.exists(path) else None, file_path)
        clean_name = re.sub(r'^[a-zA-Z0-9_-]{11}_', '', file_name)
        return FileResponse(path=file_path, filename=clean_name, media_type='application/octet-stream')
    return {"status": "error", "message": "File expired or not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8090)
