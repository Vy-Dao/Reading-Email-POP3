import email, getpass, poplib, sys

hostname,port,username = sys.argv[1:]
password = getpass.getpass()

MailConnect = poplib.POP3_SSL(hostname,port)

def allInbox(MailConnect):
    respone, listing, octets = MailConnect.list()
    for listing in listing:
        visit_listing(MailConnect,listing)

def visit_listing(pop,listing):
    number, size = listing.decode("utf-8").split()
    print("The message number", number,\
          "(The total size is",size,"bytes):")
    print()
    response, lines, octets = pop.top(number,0)
    document = "\n".join (line.decode("utf-8") for line in lines)
    message = email.message_from_string(document)
    for header in ['From','To','Subject','Date']:
        if header in message:
            print(header + ":",message[header])
    answer = input("\nRead this message [N\Y]")
    if answer.upper() == "Y":
        response, lines, octets = pop.retr(number)
        document = "\n".join(line.decode('utf-8') for line in lines)
        message = email.message_from_string(document)
        print("-" * 72)
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                print(part.get_payload())
                print('-' * 72)
                print()
        print("\nDelete this message [N\Y]? ")
        answer = input()
        if answer.upper() == "Y":
            pop.dele(number)
            print("Deleted.")

try:
    MailConnect.user(username)
    MailConnect.pass_(password)
except poplib.error_proto as e:
    print("Login failed:",e)
else:
    allInbox(MailConnect)
finally:
    MailConnect.quit()
