
## Create files and folders

This service is responsible for managing user profiles for meowstagram. All paths start with a **/profile** prefix. 

**/create_user** - [AUTHENTICATED] POST

Creates user with default params, call this during initialistation. 

**/update_user_pfp** - [AUTHENTICATED ] POST

Takes pfp id and updates it 

**/get_followers** - GET

Return list of ids of user's followers

**/get_follows** - GET

Return list of ids of user's follows

**/follow_user** - [AUTHENTICATED ] POST

Follows supplied user

**/unfollow_user** - [AUTHENTICATED ] POST

Unfollows suplied user
