# Decision record template for restful pattern
## Introduction
1. Prologue (Summary)
2. Discussion (Context)
3. Solution (Decision)
4. Consequences (Results)
## Specifics
1. Prologue (Summary):
In the context of sending api requests, we needed to select a architecture style between REST and GraphQL. We decided for using RESTful architecture as opposed to GraphQl to achieve simpler and more maintainable codebase. While this allows lesser control over our api requests, we believe it is justified as our requests are not complex.
2. Discussion (Context): 
Most of the team had little experience with graphQL and were much more comfortable with using REST. Due to the easier ease of implementation as well, it was decided that REST architecture will be much more conducive for smoother and faster development
3. Solution:
The decision will help us make API getways for our separate services in a simple and maintainable manner
4. Consequences: We found that the team found no issues while implementing API endpoints in the REST architecture. Our code is also performant and does not suffer from any latencies. 
The codebase is also much more cleaner than if we had implement GraphQL
