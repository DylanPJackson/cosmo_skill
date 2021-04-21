# cosmo
Cosmo is an [Alexa](https://developer.amazon.com/en-US/alexa) skill that 
increases your productivity by essentially answering : What should I do with 
my free time? 

Cosmo listens to your Goals, Interests, and Reminders, then prioritizes them so 
you have enough time in each day for all of them. This skill ensures that you
consistently work towards your goals, always make time for your interests, and
never forget to complete tasks you'd otherwise forget. 

## Functionality
The technical part of this project can be broken up into three distinct parts 
 : the skill itself, the logic that drives the skill, and the database that 
supports the logic. The following provides an overview of all of those pieces as 
well as how they interact with each other. 

### Alexa Skill

#### Interaction Model
The main interaction with cosmo starts by initializing your Goals, Interests,
and Reminders. From there, general usage of cosmo becomes fluid back 
and forth where you ask cosmo what to do, cosmo keeps track of what you've 
accomplished, and cosmo adjusts your priorities in response. You can of course
create more Goals, Interests, and Reminders as you continue to use cosmo. 

##### Example Intents
*InitializationIntent* : Introduces the user to cosmo, and sets up a dialogue
to pull in Goals, Interests, and Reminders.  

*CreateGoalIntent* : Gathers a description about the goal from the user, 
creates the goal in the database.

*GeneratePrioritiesIntent* : Pulls Goals, Interests, Reminders, time available,
and informs the user what tasks they should work on, and how much time it will
take. 

##### Example Dialogue
###### Breakdown of Goals, Interests, and Reminders
*User* : Hey Alexa, ask Cosmo what I need to do today?  
*Alexa* : You need to practice French, play the piano, and go swing dancing
(These are the user's goals)

*User* : Ok, what can I look forward to afterwards?  
*Alexa* : You have a number of interests to enjoy. Feel free to watch Cowboy
Bebop, make smores with your cousins, or play Spikeball. (These are some of the
user's interests)

*User* : Great. What should I work on first?  
*Alexa* : I suggest you pay your credit card bill before doing anything else.
Remember by the end of the day you need to take the car back to your 
grandfather and schedule a dental appointment. (These are the user's current
Reminders)

###### Creation of an Interest
*User* : Hey Alexa, tell Cosmo to add a new interest of mine.  
*Alexa* : Sure, tell me a bit about your interest.

*User* : I really want to explore the city some more. I live nearby but don't
ever make time to really explore it.
*Alexa* : That sounds great. Could you give me a one or two word name for this
interest?

*User* : Explore downtown  
*Alexa* : Got it. I'll make sure to include Explore Downtown when you have time
for it.

#### Hosting the Skill
This skill is hosted on an [OKD4](https://www.okd.io/) server cluster in the 
[Computer Science House](https://github.com/ComputerScienceHouse) server room. 
This cluster services the application code necessary to handle receiving and 
sending responses from and to Alexa. Rather than pointing to an [AWS Lambda](
https://aws.amazon.com/lambda/) endpoint as per the default configuration, this 
skill points to the endpoint exposed by OKD. That way, the endpoint can be fully 
customized while the performance of the skill remains the same.

### The Logic 
Cosmo prioritizes your life by taking two things about you into consideration.
Collectively, your Goals, Interests, and Reminders, and secondly how much time
you have in a day. The 'Alexa Skill' section describes how Cosmo learns that 
first piece, and the 'Database' section describes how that data is stored, so
that won't be covered here. What this section focuses on is how Cosmo obtains
the second piece : your availability, and how it ties into prioritizing your 
life.

#### Getting your Availability
Cosmo relies on the user to have a well populated, updated Google Calendar in 
order to determine their free time. Cosmo uses the [freebusy query](
https://developers.google.com/calendar/v3/reference/freebusy/query?apix_params=%7B%22resource%22%3A%7B%22timeMin%22%3A%2200%3A00%22%2C%22timeMax%22%3A%2223%3A59%22%7D%7D)
from the [Google Calendar API](https://developers.google.com/calendar/v3/reference)
to pull the amount of free time they have in a given day. In the following
hypothetical day, cosmo would identify that the user has free time between 09:00
and 10:00, as well as 18:00 and 22:00, providing Cosmo with 5 hours to work with.  
![hypothetical day](https://github.com/DylanPJackson/cosmo_skill/blob/master/imgs/hypothetical_day.png)  

#### Prioritization 
Cosmo wants to ensure that you work towards your Goals every day, that you
have time for your Interests, and that you don't forget about your Reminders.
Consider a scenario where the user has the following goals and the given free
time :
![prioritization\_1](https://github.com/DylanPJackson/cosmo_skill/blob/master/imgs/prioritization_1.png)
Cosmo wants to ensure that you complete your Reminders, so it slots them into
your free time first. Cosmo has a custom prioritization function for Reminders
which weights each Reminder by its expiration date and creation time. The 
sooner the Reminder will expire, and the longer you've had it around, the more
important it will be.
![prioritization-2](https://github.com/DylanPJackson/cosmo_skill/blob/master/imgs/prioritization_2.png)
From there, Cosmo slots in your Goals. All goals are included by default, which
makes the time you spend on each a bit interesting. A balance is struck here so
that you spend at least some minimum amount of time on each goal, but not so 
long that you'd become unproductive. This amount is based off of how much time 
you have left over after including your Reminders.
![prioritization\_3](https://github.com/DylanPJackson/cosmo_skill/blob/master/imgs/prioritization_3.png)
Finally, with whatever time is left over, the Interests are included. These are
prioritized by how long they've existed for and how long it's been since you
interacted with it. So if an interest was created a month ago but just
interacted with yesterday, it would have a lower priority than an interest that
was created last week and you haven't interacted with it yet.
![prioritization\_4](https://github.com/DylanPJackson/cosmo_skill/blob/master/imgs/prioritization_4.png)
For more in depth explanation of how the Goals, Interests, and Reminders are 
prioritized, check out the relevant code. 

### Database
All of the Goal, Interest, and Reminder data is hosted in a PostgreSQL database
on the [Computer Science House](https://github.com/ComputerScienceHouse) 
servers. This allows for security of user data and a standardized structure to
reference it. 

#### Goal Tables 
##### goal\_registry (Standalone data about each Goal)
|g\_id|description|creation\_date|status|termination\_date|
|---|---|---|---|---|
|1|Fluent in French|20200301|alive|-|
|2|Swing Dancing Instructor|20200401|alive|-|
|3|Graduate Highschool|20130801|dead|20170513|

##### goal\_milestones (Big accomplishments towards Goal)
|g\_id|milestone|date|
|---|---|---|
|1|Had an hour long conversation in French|20200814|
|1|Listened to an episode of RFM and understood almost everything|202001020|
|2|Taught my first lesson|20210424|

##### goal\_log (Daily tracking) 
|g\_id|explanation|time\_spent|date|
|---|---|---|---|
|1|Watched some Comme Une Francaise videos|45 minutes|20200509|
|2|Went to swing lesson|3 hours|20201118|
|...|...|...|

#### Interest Tables
##### interest\_registry (Standalone data about each Interest)
|i\_id|description|creation\_date|last\_interaction|status|termination\_date|
|---|---|---|---|---|---|
|1|Watch Hellzapoppin|20201006|-|alive|-|
|2|Read The Last Lecture|20210301|20210328|dead|20210401| 
|3|Play Spikeball|20210318|20210324|alive|-|

##### interest\_log (Keeps track of interest activity)
|i\_id|explanation|time\_spent|date|
|---|---|---|---|
|2|Read a couple chapters|20 minutes|20210318|
|3|Played with friends at the park|90 minutes|20210419|

#### Reminder Tables
##### remindter\_registry (Standalone data for each Reminder)
|r\_id|description|expiration\_date|expected\_time|creation\_date|status|completion\_date|
|---|---|---|---|---|---|---|
|1|Graduation cords for CSH|20210424 18:00|20 minutes|20210421|active|-|
|2|Book flights for Seattle|20210428 17:30|30 minutes|20210418|active|-|
|3|Meal prep|20210320 12:00|35 minutes|20210320|completed|20210320 11:30|

#### Integration with Skill
The backend uses [psycopg2](https://pypi.org/project/psycopg2/) to authenticate 
to and make queries to the database.
Since they are on the same secure network, no other authentication is needed to
first get onto the network. An issue that occurred when the skill was hosted
externally at AWS Lambda. 

## Philosophy
The whole idea for this project more or less culminated over the past two years
out of conversations about productivity I've had with friends and family. The 
conversations have ranged from pondering what you'd do if you made the 'best' 
decision in any situation and what that would even mean, to discussing why some
people tend to get less done when they have a ton of time to do it, and why 
they get more done with less. All of these conversations spawned a desire to
create something to solve what seemed to be a central problem : How can you
use your free time more effectively? The answer might surprise you. Just figure
out what makes people feel fulfilled, what the important things are in their
life, what they want to accomplish, all those things. Once you have that, just
make sure they consistently work towards those things and leave nothing behind.

### The Division of Life into : Goals, Interests, and Reminders 
While considering how best to prioritize the various things you could do to 
work towards a more fulfilling day, I came up with the following 
classifications. These distinctions encapsulate, more or less, anything that
anyone would need to or want to do, thereby making the overall prioritization
process much more straightforward.

#### Goals
Goals can be long term, or short term. Either way, these are normally critical
to career success, crucial to lifestyle, or things that you have much more than
a passing interest in. These normally will have dire life hindering 
consequences if not completed and / or will cause a feeling of sincere regret
so as to feel necessary. (Apologies for the pessimistic definition but it makes
sense) These things are necessary for happiness / fulfillment and thus should
be worked on each day.

#### Interests
These are people, places, activities which serve to enrich life and provide
supplementary happiness, comfort, or fulfillment. These are not of dire
importance and as such don't necessarily need to be pursued each day. These
things are the spice of life. They don't necessarily ever get completed, as you
could perpetually be interested in something. 

#### Reminders
These are normally momentary, isolated actions which only require a small
amount of attention, yet which may be crucial for daily operation / fulfillment.
Often these will need to be done by a certain time as well, and so may have
expiration date / times. They may also just be Interests that you're not
necessarily interested in, and therefore would procrastinate. Therefore, would
need a reminding nudge for it. 
