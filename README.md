# translate video
generate translated audio to youtube video as file

1.give URL to youtube video

2.choose from what language translation needed

3.choose to what language translate

4.wait... about the same time as video length

5.get videofile(.mp4) with generated translated audio (original audio is taken away)
 - or audiofile(.mp3)

Why so slow? 
Well, in short, to not be banned by google text-to-speech api. It happens due to exceeding the limits of use (https://cloud.google.com/text-to-speech/quotas). 
However i can't determine any exact limits. So my tests guide me to this specific chunk size to avoid gtts api ban. it's intentionally sleep 1 min after every processed 2 min of video.

translate_video.py ->  def audiofile_from_transcript(...):
 
    [line 57] time.sleep(60)

 - It's usually safe to translate entire video that less than 40 min long in one chunk.
 - if banned, one usually need to wait till next day

