# Decision record template for flask and Fastapi
## Introduction
1. Prologue (Summary)
2. Discussion (Context)
3. Solution (Decision)
4. Consequences (Results)

## Specifics
1. Prologue (Summary):
For sending API calls to our backend which is rwritten in python, we needed to find a routing framework to handle the incoming requests. We have used FASTAPI for handling most of the calls but have used Flask for the AI models. 
2. Discussion (Context): 
We used FastAPI for most of the endpoints as it is very performant for handling large amounts of data. Moreover, we had experience using FastAPI.
Flask was used for calling the AI models as the data transfer over network between them is not that much. Thus FLask was ideal as it has a very easy to use interface and is easier to maintain and extend.
3. Solution:
Our choices for using the appropriate framework at the proper position ensure that the codebase is easier to maintain and extend in the future while still not compromising on performance.
4. Consequences(Results): 
We found that the api endpoints defined using FastAPI are very performant and reduce latency while api endpoints in Flask are not a bottleneck for our code as majority of the time is taken in generating the response.
The code base is also easier to maintain for the AI module
