# About

**[pg_grep_client](https://github.com/morrah/pg_grep_client)** parses postgres log files using regexp and pushes it's contents to redis channels, using ip as a channel name;

**[pg_grep_server](https://github.com/morrah/pg_grep_client)** subscribes web-clients to channels.


# Installation

```
sudo apt-get install virtualenv python3.5 python3.5-dev
virtualenv -p python3.5 pg_grep_client_env
source pg_grep_client_env/bin/activate
git clone https://github.com/morrah/pg_grep_client.git && cd pg_grep_client
pip install -r requirements.txt
python client.py
```

```pg_log_dir``` in ```pg_log.conf``` should be set to your postgres log directory; 
otherwise dummy log could be generated to ```./log``` for demo using ```python pg_log_generator.py```

**!!!: set the same log format in postgres config and client.py**

```PG_PATTERN = PgPattern().from_log_format('%m %u@%d %h %c ')```


# TODO

```pg_pattern.py``` – i18n for regexp (russian language only at this moment);

move log format to config file;
