# UBC Course Checker

Program to keep checking for free spots in your desired courses!
I used this to get into the courses I wanted to take :)

### How To Use

To use this, you'll need to create your own Twilio account for sending texts,
because I use the Free plan which only allows me to send texts to myself.

1.  Sign up for Twilio and get a free number, then export your Twilio information via `.bash_profile`:

    ```shell
    export TWILIO_ACCOUNT_SID='<YOUR_ACCOUNT_SID>'
    export TWILIO_AUTH_TOKEN='<YOUR_AUTH_TOKEN>'
    export TWILIO_FROM_NUMBER='<YOUR_TWILIO_NUMBER>'
    export TWILIO_TO_NUMBER='<YOUR_NUMBER>'
    ```

2.  Install dependencies with `pipenv`:

    ```shell
    pipenv shell && pipenv install
    ```

3.  Update the `COURSES_TO_CHECK` variable in `check.py` to the courses you want to check.
    e.g. `COMM 457 101` or `CPSC 221 101` or `CPSC 221 L1F`.

4.  Keep the script running (I use `tmux` to keep it alive)
    ```shell
    ./check.py
    ```
