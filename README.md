
# com3014_profile

This is a service for handling user profiles.

## Overview
This service handles the following functions:
- Storage of information about user profile
- Update of the user's profile picture 
- Follows/unfollows

## Usage
Docker must be installed on the system. Run `docker-compose up -d --build` from the root of the repository. Once running, the service is accessible on the localhost:5051.

## Testing
Automatic testing is handled by pytest. To run the tests, build and start the container using the `docker-compose up -d --build` command and then `docker compose run profiler-app python3 -m pytest` from the root of the repository.

## Endpoints

### **/create_user** - [AUTHENTICATED] Params: None

Creates user with default params, call this during initialistation. 

### **/update_user_pfp** - [AUTHENTICATED ] Params: None

Updates user's profile picture to a new one. Form-data:

- pfp - id of the image to use as a new profile picture.

### **/get_followers** - Params: None

Return list of ids of user's followers. Form-data:

- user_id - id of the user the request corresponds to.

### **/get_follows** - Params: None

Return list of ids of user's follows. Form-data:

- user_id - id of the user the request corresponds to.

### **/follow_user** - [AUTHENTICATED ] Params: None

Follows supplied user. Form-data:

- user_to_follow - id of the user the needs to be followed.

### **/unfollow_user** - [AUTHENTICATED ] Params: None

Unfollows suplied user. Form-data:

- user_to_unfollow - id of the user the needs to be unfollowed.
