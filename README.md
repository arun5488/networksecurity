## networksecurity
My first e2e Machine learning project.
dataset is taken from https://www.kaggle.com/datasets/arnavs19/phishing-websites-dataset

These data consist of a collection of legitimate as well as phishing website instances. Each website is represented by the set of features which denote, whether website is legitimate or not. Data can serve as an input for machine learning process.

A subset of the above dataset, approx 10000 records were considered for this project.



## What all i learnt with this project ?
1. mirroring github repo and dagshub repo for logging experiments
2. The artifacts and the models generated are stored in AWS S3 bucket.
3. Set up continuous deployment to AWS EC2 using GitHub Actions and self-hosted runners.
4. Configured EC2 instance, installed prerequisites, and set up Docker for deployment.
5. Implemented and tested the full CI/CD pipeline, including image pull, container run, and security group configuration.
6. Verified successful deployment and API accessibility via browser.
