# Build-An-Agent
---

This is a repo of building a simple agent in Python without using a framework like langchain etc.


Pipeline of an Agent Run - the Thought Process:
* How many iterations?
* What conditions?
  * Am I evaluating the previous response?
  * Am I calling a tool?
* Termination?
  * Does my evaluation conclude nothing needs to change?
  * Have I executed the tool?
