import outlook
mail = outlook.Outlook()
mail.login('Zestydragon1999@outlook.com','shashwat24#')
mail.inbox()
print mail.unread()

