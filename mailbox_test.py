import mailbox  ##I made an update


# CODE Reference: http://stackoverflow.com/questions/7166922/extracting-the-body-of-an-email-from-mbox-file-decoding-it-to-plain-text-regard

def getcharsets(msg):
    charsets = set({})
    for c in msg.get_charsets():
        if c is not None:
            charsets.update([c])
    return charsets

def handleerror(errmsg, emailmsg,cs):
    print()
    print(errmsg)
    print("This error occurred while decoding with ",cs," charset.")
    print("These charsets were found in the one email.",getcharsets(emailmsg))
    print("This is the subject:",emailmsg['subject'])
    print("This is the sender:",emailmsg['From'])

def getbodyfromemail(msg):
    body = None
    if msg.is_multipart():
        for part in msg.walk():
            if part.is_multipart():
                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        body = subpart.get_payload(decode=True)
            elif part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
    elif msg.get_content_type() == 'text/plain':
        body = msg.get_payload(decode=True)
    """for charset in getcharsets(msg):
        try:
            body = body.decode(charset)
        except UnicodeDecodeError:
            handleerror("UnicodeDecodeError: encountered.",msg,charset)
            pass
        except AttributeError:
            handleerror("AttributeError: encountered" ,msg,charset)
            pass"""
    return body


if __name__ == '__main__':
    for thisemail in mailbox.mbox('UMSI-Open.mbox'):
        body = getbodyfromemail(thisemail)
        print '******************************************'
        print thisemail['subject']
        print thisemail['Date']
        if thisemail['To']:
            print "TO: " + thisemail['To']
        if thisemail['From']:
            print "FROM: " + thisemail['From']
        print
        print body
