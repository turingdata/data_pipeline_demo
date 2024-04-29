# Jira Service Desk Tickets

## Jira Hygiene

Consistency in how we work in Jira will improve the quality of the data in the system and in turn result in better data driven decisions being made. Working a Jira ticket from start to finish will most probably be done by more than one person so it is important that we understand and follow some simple Jira hygiene guidelines so as to achieve consistent use of the system.

The following are general guidelines for how and when to interact with tickets and although it is primarily focused on the AMS (link to follow) ticket lifecycle there are many takeaways that will apply to working in Jira in general.

## Communication Outside Jira
If it didn’t happen in Jira, it didn’t happen. This applies to work and communication. We should encourage all communication to happen in Jira. If a customer contacts you directly regarding a ticket you are working on please attach or summarise the communication in the ticket. Finally, take the time to request that the customer replies to the ticket in future.

## Jira Status Should Reflect the Real World
This should be obvious but to target a couple of common offenders. _In Progress_ should mean actively being worked on, _Waiting on Customer_ likewise.

## Commenting on Tickets

### When to Comment
Comment on a ticket every time progress is made. That means commenting on a ticket when:
* A question needs to go to the customer.
* We need to set or manage expections around timelines. **If we are going to miss a ticket due date, a mention to the AMS and regional lead or product owner should be made or they should be added as participants on the ticket.**  
* For any reason we need to un assign ourselves from a ticket. **A mention to the AMS and regional lead or product owner should be made or they should be added as participants on the ticket.**  
* A ticket needs to be moved into a waiting status (_With Vendor_/_On Hold_/_UAT_ etc...).
* A ticket is blocked. **A mention to the AMS and regional lead or product owner should be made or they should be added as participants on the ticket.**  
* A ticket is _On Hold for Deployment_ and a deploy date is known. We should be informing our customer when they can expect to receive value. This date should align to the CCB deploy date.  
* We are wrapping up work for the date, regardless of whether the work is complete. An brief internal comment on progress made would be sufficient.

### Internal Note vs Reply to Customer

This really means “share internally” vs “share with participants”. An internal comment can generally be treated as IT only. Reply to customer will be visible to the reporter and any participants on the ticket. See image below.

![comments_and_mentions](./assets/jira_comments_and_mentions.png)

### @mentions

Where a comment on a ticket is directed at a given user(s) please mention said user with @username as per the example above. Mentions will get the attention of people not assigned to, watching or participating on a ticket through a notification.

## How Tickets Move Across Boards
The tickets move across the boards through Jira transitions and automations. That means that operators should not drag a ticket from one column to the next. Instead use the Jira actions available at every step to progress the ticket through the workflow.

## Work in Process (WIP)
We can only progress one ticket at a time but there will be times a ticket you're working on transitions into a waiting status (_With Vendor_/_On Hold_/_UAT_ etc...). Work in Process, not progress, is something that we need to be acutely aware of because if we pile up tickets in waiting statuses we run the risk of becoming a bottleneck if all of those tickets become available for work at the same time.

To mitigate this risk, AMS leads will set a WIP limit with their team and before you pick up a new ticket please do the following:
1. Check to see if any of your existing WIP is ready to be picked up again.
2. Provided you don't have too much WIP, check the _ToDo_ column for a new task.
3. If you're at your WIP limit escalate this to the AMS and regional lead so they can chase customers if required.
4. With the approval of your AMS lead pick up a ticket that can be paused i.e. a documentation ticket or other such ticket that has less impact to impact customers if we have to pause it in order to resume work on the higher priority WIP assigned to you. Please continue to monitor your WIP tickets for any change in status.

## Working a Ticket Part 1: Regional Leads (or Product Owners)
The first ticket operator is the regional lead / product owner, they categorise and prioritise the tickets before moving them to the board as outlined below. They are responsible for steps 1-5.  

### Step 1: Categorising a Ticket
On each ticket, the Portfolio Owner field should be populated with (1) a region (e.g. Asia, North America) and (2) at least one department (e.g. Claims, Insurance Operations). The region should reflect where the reporter sits, not where the ticket will be worked per se.

### Step 2: Do We Need a Label?
Labels give us an easy way of adding additional metadata to our tickets for use in our filters/queries. Examples of how labels can be useful. There are 4 labels in particular worth highlighting: prioritised, candidate_for_prioritisation, candidate_for_self_service, candidate_for_automation.

### Step 3: Due Dates?
If we have a known deadline, it will benefit all if it is visible. Note that a planned date communicated by the customer is not a hard deadline. If the user has a hard deadline or IT is commiting to a date, set it using the _Due Date_ field as that appears on the ticket and in reports.

### Step 4: Quality Inspection
The regional leads/product owners are the first line of defence for tickets that lack the detail required for the teams to work them. The regional leads/product owners are responsible for pushing back and demanding higher standards when it comes to the detail required for a ticket.

### Step 5: From Backlog to Todo
By default all tickets will hit the _Backlog_ before they hit the board. Once a ticket has been categorised the next step is to prioritise it in the _Backlog_. When a ticket is ready to be moved to the board we should right click on the ticket in the backlog and select the move to _ToDo_ option or simply drag the ticket from the backlog to the _ToDo_ section. This triggers a Jira automation to change the ticket status to _Selected for Development_. The regional lead or product owner ensures both _Backlog_ and _ToDo_ are kept in priority order.   

![jira_backlog_todo_workflow](./assets/jira_backlog_todo_workflow.png)

## Working a Ticket Part 2: AMS Team Member (or Developer)

The second ticket operator will be an AMS team member or developer who is tasked with delivering value to the customer. They are responsible for steps 6-9.

### Step 6: Pulling From the Top of the Pile
The tickets in a given swim lane are organised in priority order with the highest priority ticket at the top. This is the ticket you pick provided you can work it, i.e. that you have a document you can follow or the knowledge and skills required to see the ticket through to completion.

### Step 7: Quality Inspection
Although the regional lead has done a quality inspection it is highly unlikely that the regional lead will know every single detail required to work every ticket type. Therefor a second check should happen before deciding to work a ticket. Should you find information is missing please highlight the detail required to the regional lead with a mention so they can follow up with the customer and hopefully avoid this happening on similar requests in the future. It will also ensure the rest of the team is aware that the request for info has been made.

### Step 8: Assigning Ticket
Don’t drag a ticket into the _In Progress_ column. Instead assign it to yourself by opening the ticket, highlighting the assignee field and selecting _Assign to Me_. The Jira automation will transition the ticket to _In Progress_.

### Step 9: Transitioning the Ticket to Done
The ticket remains your responsibility until it is _Done_. Remember to ensure the status accurately reflects the current state of the ticket and to keep stakeholders updated with the relevant updates as the ticket transitions. Finally, please escalate to your AMS lead if upcoming time off means an urgent ticket is potentially left hanging until you return.
