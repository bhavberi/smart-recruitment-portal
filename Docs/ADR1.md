# Decision record template for Microservices architecture
## Introduction
1. Prologue (Summary)
2. Discussion (Context)
3. Solution (Decision)
4. Consequences (Results)
## Specifics
1. Prologue:
In the context of the system architecture, we face the issue of large load on servers, so, we decided for MicroServices to achive maintanability and scalability accepting higher complexity.
2. Discussion:
We face the issue of large load on a single monolithic server due to large AI models for the report generation. Moreover, the failure in one server should not bring down the entire system. We also need to cater with the user need to add more features to the report. 
Since the users come from diiferent companies and thus the requirements can be different which will need us to extend the services in the future. So, we need easier scalability. Also, failure of one server should not affect the entire system.
3. Solution:
We decided to use Microservices Architecture to achieve:
    1. Scalability: Microservices allows individual components of an application to scale independently based on demand.
    2. Flexibility: Each microservice operates independently, enabling us to choose the best technology stack for each component of the AI.
    3. Resilience: Failure in one microservice typically won't bring down the entire system.
    4. Continuous Delivery and Deployment: Microservices promote continuous integration and delivery practices. We can add further festures in the report if the user needs the same.
    5. Easier Maintenance: With smaller, focused services, it's easier to understand, maintain, and debug the system.
4. Consequences:
We accept the downsides which come along whith this decision which are:
    1. Complexity: Managing a distributed system with numerous interconnected microservices can be complex.
    2. Data Management Challenges: Microservices often have their own databases or data stores, leading to data duplication and consistency challenges.