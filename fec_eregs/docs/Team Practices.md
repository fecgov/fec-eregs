# Team Practices

This page is meant to describe the team practices that the FEC Legal Resources team operate under.  

It is a living document that will be amended as the team learns what works sprint by sprint.

Many of these practices come from Agile development processes; with no specific framework being adopted.

# Team Members 
(once in GitHub link it to 18F .yml)
* Aaron Borden - Front End Developer
* Annalee Flower Horne - Back End Developer
* Anthony Garvan - Back End Developer
* Ed Mullen - UX and Design
* Leah Bannon - Engagement Manager
* Porta Antiporta - Product Steward
* Tadgh O'Higgins - Back End Developer

# Tools & Repositories
WIP - integration between tools is still under investigation.  Tools were selected to give different views of our project

## Story Map - [Storiesonboard](https://18f.storiesonboard.com/m/fec)
Story maps will serve as the vision/roadmap for our product.  It will describe the different users and activities/goals they want to achieve as they interact with beta.fec.gov
## Sprint Taskboard - [Trello](https://trello.com/b/1NNW09CL/fec-eregs-discovery)
Trello will be our used as our taskboard.  All work the team is doing should be reflected on the taskboard.  Backlog grooming/planning/estimation/demos will be driven by the task board.  

Owners of each card should comment frequently to provide visibility to progress (or lack thereof).  

While the product steward will likely be creating the bulk of the cards (in collaboration with the FEC product owner), any team member can create cards that will be prioritized into grooming sessions.

TBD - Creating / Syncing cards from whatever forum will be used for user feedback, reported defects etc.

## GitHub
Our code repositories.  
The following are GH repositories of note:
* [fec-eregs](https://github.com/18F/fec-eregs)
* [regulations-core](https://github.com/18F/regulations-core)
* [regulations-site](https://github.com/18F/regulations-site)
* [regulations-parser](https://github.com/18F/regulations-parser)
* [openFEC-web-app](https://github.com/18F/openFEC-web-app)
* [fec-styles](https://github.com/18F/fec-styles)
* [fec-cms](https://github.com/18F/fec-cms)

TBD - GH Issues syncing wih Trello

## Slack
Given our distributed model, slack will be used for async comms.  The following are channels of note:
* #fec-eregs
* #fec-general
* #fec-partners
* #eregs

# Sprint Cadence
Sprints will be used to time box our development cycles.  
Sprints will be two weeks long.  
It will start with Backog grooming and planning, and end with Demos and Retrospectives.

## Backlog Grooming/Planning
At the beginning of a sprint a prioritized list of activities will be present on the team taskboard.
This meeting will be used to review those stories where we will:
* Gain a common understanding of what the stories entail
* Ensure the team is in a position to execute the story (any dependencies)
* Commit to which stories the team will complete for that given Sprint

### Estimation
Storypointing in Agile is used in conjunction with velocity to project how much a team can commit to.  However, given our team is nascent in nature, establishing the velocity is a second priority.
Estimation is going to be used to ensure that as we discuss stories, there is a common understanding as to what it entails.  
One of the best sources to find disconnects and align on them is by each member of the team pointing.
Further, pointing gives a common baseline which can drive whether a story should be broken down further into smaller chunks.

There are at least 2 trains of thought in terms of units of measure for storypoint: complexity vs. effort (time).  
The difference between the two is described through the example of tasks that are great candidates for automation.  Those tasks often carry high effort estimates, but very low complexity estimates.
Given the forming nature of the team, effort estimates will be used.  
Aligning on a baseline of complexity may come at a later time.

*Units of Measure*

|Points| Measure|
|------|--------|
|0.5| Under 1 hour of work|
|1| Half day|
|2| Full day|
|3| 2-3 days|
|5| Full week|
|8| Full sprint|

In general, stories that initially get a 5 or 8 estimate should be considered to be broken down further.

During grooming, discussion on a particular story can extend for quite a bit of time leading to the bulk of the time spent on one story.
The moderator will be tasked on preventing this from occurring.  Some techniques are (but are not limiteed to):
* Opt to timebox the card
* Focus on getting a consistent estimate amongst the team, impleentation detail can be discussed in a kick-off
* Decide that too many dependencies/unknowns are present and move the story to the next grooming

## Daily Standups
On days without planning or demos, the team will have a standup.  This meeting will be at most 15 minutes in length via a video call.
Each member will provide an update on what they completed yesterday, plan for today, and highlight any blockers.
Being a remote team, we also will update tasks with comments; however, a daily real-time meeting will help with getting team updates faster.

The meeting will be from 4:30 - 4:45 EST.

## Sprint Demos
Sprint demos will be an opportunity for the team to showcase the hard work that has been completed during the sprint.
This will be held via a video conference where members of the team can screen share the work they completed.
Sprint demos will be open to folks outside team; particularly the FEC, our partner agency.  Sprint demos will be also open to anyone within 18F.

## Retrospectives
Retros are a forum private to the team where we will review what went well, and what did not.
This will be a 30 minute meeting, and will be private to our team.  On request it can also be facilitated with the product steward not in attendance.
Will be split up into the following:

5 minutes : team will post in mural.ly stickies that represent:
* What went well
* What did not go well
* Vote from 1-5 on how the sprint went (1 --> Poor, 5--> Excellent)

5 min : moderator will group stickies together prior to team discussion

10 - 15 min : open discussion on stickies

5-10 min : team votes *on up to two* items to focus on for the next iteration.  There will be a lot of improvement opportunities we will not get to; but if they continue to be important to the team they will come up again in subsequent retros and get voted in.

# Additional Principles

## Continuous Integration
Multiple 18F product teams will be working on a shared set of software assets.
From Notice and Comment working out of the shared eRegs repos to FEC-data working out of beta.fec.gov.  There is likely more overlap on the former, but the latter is an asset that is also live in prod (as a beta).

Therefore it is necessary to ensure that code changes preserve current functionality available to the public.  The team will invest in strengthening our automation and continous integration as we develop this product.

### Smoke Tests
Smoke tests are run on every pull request.  They are intended to validate that critical functionality is kept intact after the pull request is merged.  Smoke tests should be part of the build process and by design should complete within 5 minutes (at the very latest).  If a PR results in a failed smoke test, then the responsible dev should either address failing test or revert their code **before leaving their workstation**.  This ensures that any pull / sync from master into a branch will contain stable code.

### Daily Dev Builds
Daily builds to a development environment will allow us to kick off a more extensive set of tests.  For example, a smoke test (due to the need to execute quickly) may just validate that the output of the most extensive regulation is working.  However, we want to ensure all 53 regulations are valid.  So a daily build to a development environment will allow a nightly regression test to be run.

Both Smoke Tests and Daily Builds require effort to create, maintain and adhere to.  When discussing stories, this effort should be assumed as implicit acceptance criteria.

## Continuous Learning
We have spent a considerable amount of time analyzing fec.gov.  As we build out beta.fec.gov to support legal resources, we will ensure that the appropriate analytics and feedback loops are present to ensure that we continually measure the impact of the changes being made and take corrective action.  

Again when estimating a story; we should assume these as implicit acceptance criteria.

