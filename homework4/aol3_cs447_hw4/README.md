In the beginning, the translation probability for different Foreign word given an English word are almost all the same, while after some iterations for a certain English word, only the probability of a small portion of French word are larger than 0.01, and the rest are all zero. 

For common words in English(For example: Shit), after then first itetration we still assign some peobability incorrectly

E.g after the first iteration, the probability distribution is like:
Pr (f_y = Mierda | e_x = Shit) = 0.97 Pr (f_y = ! | e_x = Shit) = 0.03 

In the end the distribution is correct.
Pr (f_y = Mierda | e_x = Shit) = 1.0 

It is a usable translation system because the accuracy is enough (>0.95)

Sometimes the model incorrectly maps a word into a punctation. For example, the following:
Pr (f_y = . | e_x = You) = 0.24

This is probably because the model that depicts between the length of a English sentence and a foreign sentence is too
coarse. In this MP we use IBM Model 1, which assign different length of English sentences with same probability the same
length. We can modify this model, make it more complex and adaptive, then the problem might be solved.