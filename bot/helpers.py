def get_attachments(attachments):
    urls = ''
    for attachment in attachments:
        urls = urls + '\n' + attachment.url
    return urls