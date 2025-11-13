What did you learn from implementing a multi-agent workflow?

Because this application had a planner and a reviewer, the two agents had similar “skill sets” (making a good itinerary), but we wanted one to build on top of and revise the work of the other, so I had to ensure that they were focused on different tasks. I found that it was important to give each agent specific information that it should consider, verify, and include in its response. For example, the Reviewer should check reasonable travel distances, accurate cost estimates, and availability while the Planner should focus on the user’s constraints and interests.

Challenges faced and how you addressed them.


I was having a hard time getting the application to use the internet search tool and not just rely on its own “knowledge”, so in the system prompt, I was more direct in my request that it use the tool and repeated the request later in the prompt, asking that it always verified new information it’s giving with the tool.

Any creative ideas, variations, or design choices (e.g., persona roles, prompt design).

For early-stage prompts that just broadly stated the information I wanted included in the itineraries, the output structure of the model response varied differently with each call. For example, it would include estimated costs for some activities or transportation and not for others. I improved on this by providing a template with all the specific information that I wanted guaranteed in the itineraries, and this ensured that the model would include this information in its response.

