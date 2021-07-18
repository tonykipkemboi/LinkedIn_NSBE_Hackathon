# LinkedIn_NSBE_Hackathon

![](https://img.shields.io/github/languages/code-size/tonykipkemboi/LinkedIn_NSBE_Hackathon?style=for-the-badge)
![](https://img.shields.io/github/last-commit/tonykipkemboi/LinkedIn_NSBE_Hackathon?color=blue&style=for-the-badge)

LinkedIn &amp; NSBE Hack Day team project

For an initial load, run `python3 dbload.py`.

There are 1000 profiles with random name and 4 skills in their skillset.

To analyze the skills of a profile, run:
`python3 analyze_skills.py --id [ID]`
where `[ID]` is an integer from 1 to 1000.

or
`python3 analyze_skills.py --name "[NAME]"`
where `[NAME]` can be a full or partial name, e.g. Hillary Velasquez
