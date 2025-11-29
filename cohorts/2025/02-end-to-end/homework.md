In the module, we build an end-to-end application: it was the snake game with front-end and back-end. 


We will implement the a plaform for online coding interviews. 

You should be able to create a link and share it with the candidate. Everyone who connects to the link should be able to edit the code in the code panel, and the rest should see updates in real time.

You can choose any technologies you want. For example:

- Frontend: React + Vite
- Backend: express.js

We recommend using JavaScript for frontend, because with other technologies, some of the homework requirements may be difficult to implement.

But you can experiment with alternatives, such as Streamlit.


## Q1

Ask AI to implement both frontend and backend - in one prompt.

Note: you can also follow the same path as in the videos and make it in 3 steps:

1. Frontend
2. OpenAPI specs
3. Backend

In the homework form, paste the initial prompt you gave to AI to start the implementation. 

## Commit your code

Commit your code to git. Don't forget to do it at every step. You can create AGENTS.md file with the instructions to do it.

## Q2

Maybe at this point your application will already function. Maybe not. But it's always a good idea to cover it with tests. 

I usually do it even before trying to run the application because it helps to resurface all the problems with implementation.

Ask AI to write integration tests that check that the interaction between client and server works.

Also it's a good idea to ask it to start creating a README.md file with all the commands for running and testing your application.

For the homework form, copy the terminal command you use for executing tests. 


## Q3 Running both client and server

make it possible to run both client and server at the same time
use concurrently for that

what's the command we have in package.json (npm dev run) for running both?

## Q4 multiple language 

Let's now add support for syntax highlight for JS and Python.  

Which library did AI use for it? 


## Q5 Execution

Now let's add code execution.

TODO explain why we don't want to execute ourside of sandbox 

But to make it save, let's use WASM - to execute the code only on the browser. 

Which libarry did aI use for comping python to WASM?



## Q6 Containerization


## Q7 Deployment

Now let's deploy it. which service do you want to use for it? 

Share your links or demos in slack and socials!

