bossjones-fabric
================

Just a github repo for my fabric tasks. Will continue to refactor over time

For my purposes, I always use a Jumpserver to access all of my remote servers.

because of this you need to add the following to your `.bash_profile`:

# For bossjone fabric tasks
export FABRIC_KEY_FILENAME='/path/to/.ssh/id_rsa'
export FABRIC_JUMPSERVER='127.0.0.1'
export FABRIC_USER='blacktonystarkoflife'

Yes I know I can use a user wide `~/.fabricrc` file as well.

# Known errors

If you get the following error `NetworkError: Error reading SSH protocol banner` make sure you note which servers this error was thrown on, and simply ssh into it. This will add it to your `known_hosts` file, and should prevent this issue from coming up.
