from pytube import YouTube
from os import system, remove

# TODO: проверить работу get_audio_quality и download_audio_only: иногда не качаются некоторые битрейты


def get_video_resolutions(url: str):
    """
    Возвращает сортированный список строк, содержащий все имеющиеся у видео разрешения.
    Пример: ['360p', '480p', '720p', '1080p']
    url - ссылка на видео, строка.
    """
    yt = YouTube(url=url)
    all_resolutions = [str(i.resolution) for i in yt.streams]
    unique_resolutions = set(all_resolutions)
    unique_resolutions.remove('None')
    unique_resolutions = list(map(lambda x: int(x[:len(x) - 1]), unique_resolutions))
    unique_resolutions.sort()
    unique_resolutions = list(map(lambda x: (str(x) + 'p'), unique_resolutions))
    return unique_resolutions


def get_audio_quality(url: str):
    """
    Возвращает сортированный список строк, содержащий все имеющиеся у видео битрейты звука.
    Пример: ['70kbps', '96kbps', '128kbps', '160kbps']
    url - ссылка на видео, строка.
    """
    yt = YouTube(url=url)
    all_quality = [str(i.abr) for i in yt.streams]
    unique_quality = set(all_quality)
    unique_quality.remove('None')
    unique_quality = list(map(lambda x: int(x[:len(x) - 4]), unique_quality))
    unique_quality.sort()
    unique_quality = list(map(lambda x: (str(x) + 'kbps'), unique_quality))
    return unique_quality


def download_video_only(url: str, res):
    """
    Скачивает видео (без звука) заданного качества.
    Принимает url - ссылку на видео, res - разрешение картинки (строка вида "240p")
    """
    yt = YouTube(url=url)
    yt.streams.filter(adaptive=True, resolution=res, mime_type='video/mp4').first().download(filename='video.mp4')


def download_audio_only(url: str, abr: str):
    """
    Скачивает аудио (без видео) заданного качества.
    Принимает url - ссылку на видео (строка), abr - средний битрейт (строка вида "48kbps")
    """
    yt = YouTube(url=url)
    yt.streams.filter(only_audio=True, abr=abr).first().download(filename='audio.mp3')


def merge_audio_video(url, res, abr):
    download_audio_only(url, abr)
    download_video_only(url, res)
    cmd = f"ffmpeg -i video.mp4 -i audio.mp3 -c:v copy output.mp4"
    system(cmd)
    remove('video.mp4')
    remove('audio.mp3')
