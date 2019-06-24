def ward_newsletter_name(delivery_date):
    month = delivery_date.strftime("%B")
    year = str(delivery_date.year)
    return month + " " + year + " Ward Newsletter"
