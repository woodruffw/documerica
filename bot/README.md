documerica-bot
==============

A small Twitter bot for posting DOCUMERICA photos.

See it in action [here](https://twitter.com/dailydocumerica).

## Setup

1. Create a `twitter.env` file that looks roughly like this:

    ```bash
    export API_KEY=your-api-key
    export API_KEY_SECRET=your-api-key-secret
    export ACCESS_TOKEN=your-access-token
    export ACCESS_TOKEN_SECRET=your-access-token-secret
    ```

2. Run `make_db.py` (see the parent directory) and move the resultant
`documerica.db` into this directory

3. Run `bot.sh` (or put it in your job scheduler)
