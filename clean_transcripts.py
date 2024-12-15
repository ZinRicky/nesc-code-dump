import os
import webvtt
import tqdm
import json

# Subtitles can be either proper VTT files or JSON objects.
# This script crunches both these file types and saves the
# results in plain-text files.

for transcript in tqdm.tqdm(os.listdir('./transcripts')):
    # First case: the transcript is a proper VTT.
    # The code should just loop over the lines and save them in a file.
    try:
        data = webvtt.read(os.path.join('transcripts', transcript))
        content: str = ' '.join(
            [line.text for line in data]).replace('  ', ' ')

        if not os.path.isfile(os.path.join('transcripts', transcript.split('.')[0] + '.txt')):
            with open(os.path.join('clean_transcripts', transcript.split('.')[0] + '.txt'), 'w', encoding='utf-8') as fp:
                fp.write(content)

    except webvtt.errors.MalformedFileError:
        with open(os.path.join('transcripts', transcript), encoding='utf-8') as fp:
            data = json.load(fp)
        alt_content: list[str] = []
        for line in data['utterances']:
            if 'text' in line:
                alt_content.append(line['text'])
            elif 'Text' in line:
                alt_content.append(line['Text'])
            else:
                raise ValueError(f"Something with the subtitles {transcript} is wrong")
        content = ' '.join(alt_content).replace('  ', ' ')

        if not os.path.isfile(os.path.join('transcripts', transcript.split('.')[0] + '.txt')):
            with open(os.path.join('clean_transcripts', transcript.split('.')[0] + '.txt'), 'w', encoding='utf-8') as fp:
                fp.write(content)
