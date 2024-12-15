# It is possible that general influencer data was inspected at a later time.
# In this case, the provided link for subtitles may have already expired.
# This script deletes all failed transcripts.

import os

to_be_deleted: list[str] = []

i = 0

for transcript in os.listdir('./transcripts'):
    with open(os.path.join('transcripts', transcript), encoding='utf-8') as fp:
        # This is a bad hack, but it should work.
        if '<HTML><HEAD>' in fp.readlines()[0]:
            to_be_deleted.append(transcript)
            i += 1

for bad_transcript in to_be_deleted:
    os.remove(os.path.join('transcripts', bad_transcript))

print(f'{i} transcripts were faulty.')