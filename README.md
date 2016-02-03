# StreamLighter - HackRice 2016

### StreamLighter captures automatic highlights of any live stream during the stream based on the density of chat comments per second

We saw that during streams, many people want to see instant highlights right after a moment happens. Or they would like to just view the highlights of a stream but sometimes that isn't always available. This hack solves that problem.

We focused on twitch chat for this hack. Our metric for a highlight was seeing the density of chat comments per second. We maintained a moving average of the density of comments and if the chat exploded in comments, we would start recording. Once the chat died down, we would end the recording, add 8-7 seconds of footage before the highlight started and about 5 seconds of footage after the highlight ended and that would be a highlight.

We made a small web app to compliment this. The user can type in the address of a channel they are interested in, it will start looking at the stream to see if there is a highlight. If there is one, it will record it, and then make it available as a download.

We tried this for Twitch, but it can be extended to be used for any live stream.

