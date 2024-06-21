# Bella Trading Telegram Bot
Main ```@PrakarshKaBot``` <br>
Test ```@test_ptech_bot```



## Getting Started

### Prerequisites

- Python installed on your system.
- Git for cloning the repository.

### Installation Steps

1. Clone the repository to your local machine:
    ```sh
    git clone https://github.com/ptechofficial/PrakarshKaBot.git
    ```

2. Navigate to the project directory:
    ```sh
    cd PrakarshKaBot
    ```
3. Create and Activate Virtual Environment
    ```sh
    python -m venv venv
    venv/Scripts/activate
    ```
4. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage Instructions

To initiate the bot, you'll need to decide whether you're operating in a `test` environment or the `main` environment for live trading.

### Test Environment

For testing purposes, launch the bot with:
    ```
    python server.py test 
    ```

### Main Environment

For live trading, activate the main environment:
    ```
    python server.py main
    ```

