title: Do Not Redeem #5
value: 500
description: Can you determine the https GET endpoint where the scammer logs their victims' sms messages? The scammer took a lot of steps in hiding the endpoint, maybe they're afraid of getting caught... Wrap your answer within `KashiCTF{` and `}`.

## Footnotes

1. The flag format:
  Let's say the scammer logs their victim's sms messages to the url https://example.site.com/logScamResults?sender=lmao&message=ded&id=victimId
  Then the answer shall be `KashiCTF{https://example.site.com/logScamResults}`. Omit the query string (i.e. the part after (including) `?`).

2. As with other challenges in this series, solving previous challenges, although not required, will be of great help.


Download `kitler's-phone.tar.gz` : Use the same file as in the challenge description of [forensics/Do Not Redeem #1](https://kashictf.iitbhucybersec.in/challenges#Do%20Not%20Redeem%20#1-28)