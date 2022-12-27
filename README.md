README for Ubergeben

Ubergeben takes transcriptions from the Azure Speech SDK using the default microphone input and passes the transcribed text to a discord channel via a bot.

REQUIREMENTS

Install Azure Library
```
pip install azure-cognitiveservices-speech
```
See https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-speech-to-text?tabs=windows%2Cterminal&pivots=programming-language-python for further details on the Azure setup, including creating an Azure account and Speech resource.

Install Discord Library

```
pip install discord.py
```


SETTINGS

Set the following variables in the config.py

TOKEN - this is the token for the Discord bot

CHANNEL - this is the destination discord channel

speech_key - put your Azure speech key generated here

region - put your Azure speech region here - typically 'westus'


TODO

write a description on howto use an RTL-SDR via piping with the rtl_fm command.
