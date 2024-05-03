from youtube_transcript_api import YouTubeTranscriptApi
import youtube_transcript_api
from gtts import gTTS
import time
from pydub import AudioSegment
from pytube import YouTube
import pytube.exceptions
from moviepy.editor import *
import moviepy.video.fx.all as vfx
import os


def get_transcript(url, language_from='en', language_to='uk'):
    video_id = url.split('/')[-1]
    while True:
        list_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        try:
            en_transcript = list_transcripts.find_transcript([language_from])
        except youtube_transcript_api._errors.NoTranscriptFound:
            return
        translated = en_transcript.translate(language_to).fetch()

        if translated:
            print(translated[0])
            return translated


def audiofile_from_transcript(transcript, language_to, title, length, dirname):
    start = transcript[0]['start']
    text = ['' for _ in range((length // 120)+1)]

    i = 0
    for fragment in transcript:
        if fragment['start'] > (i+1)*120:
            i += 1
        text[i] += ' ' + fragment['text']

    yield 'Making audio...'
    j = 0
    total_size = 0
    while j < len(text):
        total_size += len(text[j])
        print(f'making audio from chunk {j}, size={len(text[j])}')
        destination = os.path.join(dirname, f'{title}_{language_to}_{j}.mp3')
        try:
            tts = gTTS(text[j], lang=language_to)
            yield f'Saving audiofile from chunk {j}...'
            tts.save(destination)
        except Exception as e:
            print(*e.args)  # chunk 25, size=1743, total size=44097
            try:
                os.remove(destination)
            except FileNotFoundError:
                pass
            break
        j += 1
        time.sleep(60)

    print(f'total size={total_size}')
    assembly_audio(title, language_to, start, dirname)
    yield 'clear files...'
    clear_chunk_files(title, language_to, dirname)
    print('audio end')


def assembly_audio(title, lang_to, start, dirname):
    audio = AudioSegment.silent(start * 1000)

    for i in range(1000):
        try:
            path = os.path.join(dirname, f'{title}_{lang_to}_{i}.mp3')
            audio += AudioSegment.from_mp3(path)
        except FileNotFoundError:
            break

    destination = os.path.join(dirname, f'{title}_{lang_to}.mp3')
    audio.export(destination, format="mp3")


def clear_chunk_files(title, lang_to, dirname):
    for i in range(1000):
        try:
            file = os.path.join(dirname, f'{title}_{lang_to}_{i}.mp3')
            os.remove(file)
        except FileNotFoundError:
            break


def download_video(yt, title, lang_from, dirname):
    start_time = time.time()

    yd = yt.streams.get_highest_resolution()
    yd.download(dirname, filename=f'{title}_{lang_from}.mp4')

    t = time.time() - start_time
    print('Time to download video:', t)


def compose(title, lang_from, lang_to, dirname):
    yield 'editing audio/video...'
    start_time = time.time()

    path = os.path.join(dirname, f'{title}_{lang_from}.mp4')
    videoclip = VideoFileClip(path)

    path = os.path.join(dirname, f'{title}_{lang_to}.mp3')
    audioclip = AudioFileClip(path).fx(vfx.speedx, 1.2)

    rate = videoclip.duration / audioclip.duration
    print(f'\nspeed rate for video={rate}')

    yield 'remove audio from video...'
    videoclip = videoclip.without_audio().fx(vfx.speedx, rate)

    yield 'add new audio to video...'
    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip

    print('Time to edit video:', time.time() - start_time)

    yield 'saving new videofile...'
    start_time = time.time()

    destination = os.path.join(dirname, f"{title}_{lang_to}.mp4")
    videoclip.write_videofile(destination)

    print('Time to make videofile:', time.time() - start_time)


def translate(url, language_from, language_to, only_audio=False, dirname=os.getcwd()):
    start_time_total = time.time()
    print(f'from {language_from} to {language_to}, only audio={only_audio}')
    print(f'folder:{dirname}')

    try:
        yt = YouTube(url)
    except pytube.exceptions.RegexMatchError:
        return 'Wrong URL'

    yield f'{yt.title}, {yt.length}sec'

    good = '0123456789' + '().,- '
    title = ''.join(filter(lambda x: x.isalpha() or x in good, yt.title))
    print(f'title after:{title}')
    yield f'title after:{title}'

    filenames = [entry.name for entry in os.scandir(dirname)]

    if f"{title}_{language_to}.mp3" not in filenames:

        print('trying to get transcript...')
        yield 'trying to get transcript...'
        transcript = get_transcript(url, language_from, language_to)
        print('done!')

        if not transcript:
            print('no transcript')
            return f'No transcript was found for {language_from} language'

        gen = audiofile_from_transcript(transcript, language_to, title, yt.length, dirname)
        while True:
            try:
                yield next(gen)
            except StopIteration:
                break

    t = time.time() - start_time_total
    print('time to get audio:', t)

    if not only_audio:

        if f"{title}_{language_from}.mp4" not in filenames:

            yield 'start downloading video...'
            download_video(yt, title, language_from, dirname)

        if f"{title}_{language_to}.mp4" not in filenames:

            yield 'start composing new video...'
            gen = compose(title, language_from, language_to, dirname)
            while True:
                try:
                    yield next(gen)
                except StopIteration:
                    break

    yield ''
    print('Done!')
    print('total time:', time.time() - start_time_total)

    if only_audio:
        return f'Audio translated' \
               f' and saved as: {title}_{language_to}.mp3\n' \
               f'file at:{dirname}'
    else:
        return f'Video translated' \
               f' and saved as: {title}_{language_to}.mp4\n' \
               f'file at:{dirname}'
