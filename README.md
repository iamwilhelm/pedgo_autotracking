# Pedagogical Autotracking

A pedagogical implementation of [autotracking](https://www.pzuraq.com/blog/how-autotracking-works)
in Python. It was mostly for me to understand how it worked. 

The advantage of autotracking over hybrid push-pull signals is that in the 
state setting phase, you don't need to propagate a dirty bit all the way 
down the entire computational graph. That's because you have a global clock 
to compare against. 

The curious thing about it was how it seemed like it didn't cut off traversal 
all the way back to the state source, unlike the pull phase of push-pull 
hybrid of signal systems like Solid. 

But I think it's because it doesn't need to. At every node, you can compare the
node's clock to the global clock and see if it needs to be updated. 

The other thing not mentioned is it leaves the potential for a version vector,
so all nodes establish a poset. That way you can determine if two nodes are 
siblings or not and potentially execute them concurrently.


