# More Is Less LectureEditor
![](/images/demo.PNG)

## Info and credits: 

Made by: Maximo Perasso

Credit to the following modules and programmers for their code:

https://gist.github.com/vivekhaldar (concatenate video code)

https://zulko.github.io/moviepy/ (video editing module)


### Description
This software was meant to make the lecture videos from professors a lot easier to learn from if the instructor likes to wait or perhaps talks a bit too slow or too fast.
This is done by detecting the 'quiet points in the lecture (sections of the video which fall below a user controlled decibel level) and removes it from the final processed lecture.
It has been capable of reducing class lectures down from **1 hr 15 minutes** down to **23 minutes** with 0% information loss! 

The software is also capable of reading from an instructor.txt plain text file in which you can save your presets in the following manner:
```
PRESET_NAME , VOLUME_LEVEL , SPEED , AUDIO_CLIPPING_LEVEL
example:
DEFAULT,100,1,0.01
```
There is also a resolutions file, but this should not be modified as the available options are only present based on compatibility with the moviepy module

### Disclaimer

*For professors:
No malice is intended, this software is purely
to enhance the content from the instructor
for students who prefer different learning styles.*


*For students:
This software is not magic, it cannot help if you
simply do not understand the content.
Asking a teacher for help is always the best way to
understand the topic.*

## Download:
(By downloading you agree to the above disclaimers)

### Full list of releases:
### [1.0.0 (original release) , created on 1/23/2022 (Windows exe standalone) ](https://github.com/MaxCorpIndustries/MoreIsLess_LectureEditor/releases/tag/main)

