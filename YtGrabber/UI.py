from tkinter import *
from tkinter import ttk
from Logic import *


def ui_constructor():
    def selectors():
        link = entry.get()
        audio_quality_selector['values'] = get_audio_quality(link)
        video_resolution_selector['values'] = get_video_resolutions(link)

        audio_label.pack(anchor=NW, padx=6, pady=6)
        audio_quality_selector.pack(anchor=NW, padx=6, pady=6)
        audio_download_btn.pack(anchor=NW, padx=6, pady=6)
        video_label.pack(anchor=NW, padx=6, pady=6)
        video_resolution_selector.pack(anchor=NW, padx=6, pady=6)
        video_download_btn.pack(anchor=NW, padx=6, pady=6)
        download_video_with_audio_btn.pack(anchor=NW, padx=6, pady=6)

    def download_audio_buttons():
        download_audio_only(entry.get(), audio_quality_selector.get())

    def download_video_buttons():
        download_video_only(entry.get(), video_resolution_selector.get())

    def download_video_with_audio():
        merge_audio_video(entry.get(), video_resolution_selector.get(), audio_quality_selector.get())

    root = Tk()
    root.title('YAYG - Yet Another Youtube Grabber')
    root.geometry("750x700")

    link_label = ttk.Label(text='Сюда вставить ссылку на Youtube:')
    link_label.pack(anchor=NW, padx=6, pady=6)
    entry = ttk.Entry(width=100)
    entry.pack(anchor=NW, padx=6, pady=6)

    btn = ttk.Button(text="Поехали", command=selectors)
    btn.pack(anchor=NW, padx=6, pady=6)

    audio_label = ttk.Label(text='Качество звука:')
    video_label = ttk.Label(text='Качество видео:')
    audio_quality_selector = ttk.Combobox(values=[])
    video_resolution_selector = ttk.Combobox(values=[])

    audio_download_btn = ttk.Button(text="Скачать только звук", command=download_audio_buttons)
    video_download_btn = ttk.Button(text="Скачать только видео", command=download_video_buttons)
    download_video_with_audio_btn = ttk.Button(text="Скачать видео со звуком", command=download_video_with_audio)

    root.mainloop()


ui_constructor()
