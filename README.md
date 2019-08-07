# TwitterNetwork
This program generates a Twitter follower network starting from a single user. For that first user, it will retrieve all of their followers, then all of their follower's followers, and so on until the program is stopped. It works by continously adding retrieved followers to a queue and de-queuing them once their followers have been retrieved (and in turn added to the queue). If a user has already been looked up they will be skipped. Because some users can have many followers, a maximum of 200 followers will be retrieved for a given user and added to the queue. Error handling is built in - if a user returns an API error they will be skipped. 

## Output files
| File | Contents |
| --- | --- |
| user_details.csv | More detailed information about a user (friend count, followers count)|
| followers.csv | The follower network as Twitter ids | 
| skip.csv | A master record of which ids have had their followers retrieved |

## To use
To use this program you will need to add your Twitter API details, change the output paths of the above files, and select a user to start building the network from. 

## Restarting network.py
If at some point you stop network.py and want to re-start building the network, use network_pickup.py. This will identify the last user that was looked up and re-start the queue from there. 
