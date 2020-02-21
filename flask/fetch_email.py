import outlook
mail=outlook.Outlook()
mail.login("Zestydragon@outlook.com","shashwat24#")
mail.inbox()
print mail.unread()
