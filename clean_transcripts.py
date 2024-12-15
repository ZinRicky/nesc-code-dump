import os
import webvtt
import tqdm
import json

# Subtitles can be either proper VTT files or JSON objects.
# This script crunches both these file types and saves the
# results in plain-text files.

for transcript in tqdm.tqdm(os.listdir('./transcripts')):
    if not os.path.isfile(os.path.join('transcripts', transcript.split('.')[0] + '.txt')):
        # First case: the transcript is a proper VTT.
        # The code should just loop over the lines and save them in a file.
        try:
            data = webvtt.read(os.path.join('transcripts', transcript))
            content: str = ' '.join(
                [line.text for line in data]).replace('  ', ' ')

        # Second case: the transcript is a weird JSON object.
        # Probably due to the on-screen version being styled.
        # We inspect such object and extract as much text as possible.
        except webvtt.errors.MalformedFileError:
            with open(os.path.join('transcripts', transcript), encoding='utf-8') as fp:
                data = json.load(fp)
            alt_content: list[str] = []

            # For some bizarre reason, there are two possible text keys.
            for line in data['utterances']:
                if 'text' in line:
                    alt_content.append(line['text'])
                elif 'Text' in line:
                    alt_content.append(line['Text'])
                else:
                    raise ValueError(f"Something with the subtitles {
                        transcript} is wrong")
            content = ' '.join(alt_content).replace('  ', ' ')

        finally:
            with open(os.path.join('clean_transcripts', transcript.split('.')[0] + '.txt'), 'w', encoding='utf-8') as fp:
                fp.write(content)
