data_types = {
    "URL": "@@",
    "vCard":
        """BEGIN:VCARD
VERSION:4.0
FN:@@
N:@@
BDAY:@@
GENDER:@@
EMAIL;TYPE=@@
END:VCARD""",
    "vCalendar":
        """BEGIN:VCALENDAR
VERSION:1.0
BEGIN:VEVENT
CATEGORIES:@@
STATUS:@@
DTSTART:@@
DTEND:@@
SUMMARY:@@
DESCRIPTION:@@
CLASS:@@
END:VEVENT
END:VCALENDAR""",
    "e-mail": "mailto:@@",
    "Tel": "tel:@@",
    "SMS": "sms:@@?body=@@",
    "Geo Location": "geo:@@,@@,@@",
    "WiFi": "WIFI:S:@@;T:WPA;P:@@;;"}

qr_fields = {
    "URL": {"URL": "https://google.com"},
    "vCard": {"Full Name": "Simon Perreault",
              "Name": "Perreault;Simon;;;ing. jr,M.Sc.",
              "Birth Day": "--0203",
              "Gender": "M",
              "Email+Type": "work:simon.perreault@viagenie.ca"},
    "vCalendar": {"Categories": "MEETING",
                  "Status": "TENTATIVE",
                  "Start_Date": "19960401T033000Z",
                  "End_Date": "19960401T043000Z",
                  "Summary": "Your Proposal Review",
                  "Description": "Steve and John to review newest proposal material",
                  "Class": "PRIVATE"},
    "e-mail": {"email": "SomeOne@SomeWhere.org"},
    "Tel": {"Tel": "+1-212-555-1212"},
    "SMS": {"Phone": "+15105550101",
            "Message": "hello%20there"},
    "Geo Location": {"Lat": "123123",
                     "Long": "123123",
                     "Alt": "100"},
    "WiFi": {"SSID": "TestSSID",
             "Password": "12345"}
}
