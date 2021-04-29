# Semasia - utilities for analyzing a list of journal entries

If you want to use this, take a look at the code at [the examples notebook](https://github.com/sarmentow/semasia/blob/master/src/examples.ipynb)

## Using NLP to see what emotions I felt while I was journalling 

![Graph of emotions over time](./assets/cover.png)

While writing one day, I realized that by being consistent with my writing I was creating a lot of data that I could use to play around. At first I just wanted some basic information about the words I was using and the length of my journal entries, so I wrote a small script with lots of utility functions to process my text files.

![List of functions I created](./assets/snippet.png)

Above is a snippet of what I was able to accomplish with these utility functions. Things like searching for the amount of times a certain query appeared throughout all documents, listing all periods I was able to sustain daily writing, listing all periods I spent without writing, the total amount of words written so far... The list goes on. 

It was pretty fun to get some info on everything I had written.

After doing all that I started thinking about what other information could I extract from what I wrote. I wanted to see whether I could establish some sort of relation between the emotions behind what I was writing and the stuff that happened in my life. I thought that if I found a way of plotting emotions over time I would be able to see how the things that happened in my life affected my emotions or even how ideas I had affected how I perceived the world.

I already had some experience with machine learning, so I knew what I was looking for. At first I thought I would need to train my own language model to be able to calculate the emotions in a text, so I searched around for datasets that correlated text to emotions. I found [GoEmotions](https://arxiv.org/abs/2005.00547), which is a dataset containing lots of reddit comments which were labeled by assigning 1's (which means yes) and 0's (which means no) to a list of 27 emotions + a neutral category.

I didn't know how long it would take to train a model such as this and ended up deciding to use a pre-trained model on the GoEmotions dataset instead of training my own. So I found a model on HuggingFace and right away I was able to write a sentence in a little input box and get back some data about the emotions in the written text. Progress boyz.

![Text classification on HuggingFace](./assets/text_classification.png)

So the next step was I had to setup a way to send an entry and get back a list of emotions. 

I knew that there would be some sort of limit as to how much text I was able to send at once for the language model to make its predictions given how bad language models are at keeping up with long texts containing lots of contextual relationships. 

So I had to find out a way of classifying long journal entries, and the solution I found was to break it up into individual sentences and then calculate the average of all emotions in an entry. There are probably more intelligent ways of solving this problem, but this was simple and easy to write.

Another thing I did was running the language model locally for privacy reasons - and also because I was going to get rate limited for sending a request for each sentence in each of my entries. It isn't a particularly fast approach, but at least I can do the predictions as many times as I want.

After creating some more utility functions in order to have a function that returned the predictions organized just like the HuggingFace API did, I was finally able to piece together a complete program that was able to tell me what emotions I felt while I was writing. 

I still had to filter out all journal entries which weren't completely in english in order to avoid the model spitting nonsense about the emotions in portuguese text, write a python notebook to put together everything necessary from my utility functions and the language model in order to be able to plot my emotions over time, and then, voila.

![Graph of my emotions over time, extracted from my journal entries](./assets/cover.png)

So how good were the predictions above? Kind of. For individual sentences I've found that the language model does a good enough job of telling what emotions are involved in a sentence. Also, the guy who trained the model I'm using [actually wrote](https://huggingface.co/joeddav/distilbert-base-uncased-go-emotions-student) that the performance of the model isn't as good as models trained with full supervision. I went with his model anyway because I felt like it was good enough. Despite that being the case, the data looks a bit messy when visualized.

I think a big problem that's responsible for how chaotic the data looks has to do with my filtering of the entries that weren't written in english. 

See, I used to write a lot in english but overtime I found that portuguese comes a bit more natural for accurately depicting what feelings I'm trying to convey, though sometimes I switch back to english at times when I want to be more objective and concise. This frequent switch between languages made the available english entries for classifying emotions take place in periods distant from one another, making it look like there's no relation between what I felt in the previous entry and the next couple of ones.

I believe that if I had data that was more continuous and uniform, the score for each feeling would look less random and more in line with what one would expect of data points that are close to one another.

Also, there's way too much going on at once in the graph above, sometimes it's even hard to tell the difference between what emotion does a color represent. 

So, by using some of the utility functions I wrote, I was able to find a period of 9 days where I wrote daily in english. Also, this is a sample of what the graph looks like for single emotions.

![Graph of realization emotion scores over time](./assets/realization.png)

![Graph of love emotion scores over time](./assets/love.png)

![Graph of admiration emotion scores over time](./assets/admiration.png)

![Graph of neutral emotion scores over time](./assets/neutral.png)

It looks a lot less chaotic. Also, I can take a look at my entries and see whether these spikes in each emotion make any sense. They're a bit iffy. Because the graphs are not to scale (you can see that the values on the y axis for love are very small while the ones for realization are much bigger) it's easy to misrepresent the emotions that were actually felt. I've noticed that when an emotional statement is processed by the language model, it increases its predictions in pretty much all emotions, but the emotions that were actually surrounding the text gets a bigger increase than the other ones.

This was fun, and has a lot of potential. I didn't want to get distracted by stuff that had nothing to do with the initial aim of this project - to get info about the data I created on my journal - so I didn't create a GUI or anything like that. It's all a couple of scripts and a notebook with not so great code that spits out these graphs.
