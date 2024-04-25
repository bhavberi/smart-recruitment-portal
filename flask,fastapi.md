# Decision record template for flask pattern
## Introduction
1. Prologue (Summary)
2. Discussion (Context)
3. Solution (Decision)
## Specifics
1. Prologue (Summary):
For sending API calls to our backend which is return in python, we needed to find a routing framework to handle the incoming requests. We have used FASTAPI for handling most of the calls but have used Flask for the AI models. 
2. Discussion (Context): 
We used FASTAPI for most of the endpoints as it is very performant for handling large amounts of data. Moreover, we had experience using FASTAPI. Flask was used for calling the AI models as the data transfer over network between them is not that much. Thus FLask was ideal as it has a very easy to use interface and is easier to maintain and extend
3. Solution:
Our choices for using the appropriate framework at the proper position ensure that the codebase is easier to maintain and extend in the future while still not compromising on performance.