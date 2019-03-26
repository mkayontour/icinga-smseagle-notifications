# icinga-smseagle-notifications

This is a notification script for the SMSEagle Gateway. 

It's using the API, so in order to use this script a user is needed which has access to the API.

### Setup API User

The API user only need two endpoint querys, one to send sms and a second to query sms to contacts.

![API User create](/img/create-user.png)


### Installation

Put the script into the Icinga 2 scripts folder.

`/etc/icinga2/scripts`

Make sure all perl dependencies are installed.

* urllib2

* argparse

Copy the notification command configuration into your Icinga 2 configuration folder.
Check the configuration with `icinga2 daemon -C` and reload Icinga 2.

### Using the notification

To send notifications to SMSEagle contacts you need to add a contact to the addressbook.

![create contact](/img/create-contact.png)

Then create a user object in Icinga 2.

```
object User "jdoe" {
  import "generic-user"

  email = "jondoe@domain.com"

  smseagle_notify_contactname = "jdoe"
}
```
