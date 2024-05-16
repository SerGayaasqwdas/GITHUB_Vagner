git clone https://github.com/Garret47/PT_Telegram_Bot.git -b ansible

Edit .env, db_hosts, db_master, db_slave (PORT, DB_NAME, USER_NAME, PASSWORD_USER should match .env)

Then execute the command:

ansible-playbook ansible-playbook.yml
