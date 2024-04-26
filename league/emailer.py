import yagmail
import keyring


class Emailer:
    sender_address = None

    _pass = None
    _sole_instance = None

    @classmethod
    def configure(cls, sender_address):
        cls.sender_address = sender_address
        cls._pass = keyring.get_password("MicrosoftAccount:user=christianpolka@gmail.com", cls.sender_address)

    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    def send_plain_email(self, recipients, subject, message):
        if not self.sender_address:
            raise ValueError("Sender address is not configured. Please use configure() method.")

        yag = yagmail.SMTP(self.sender_address, self._pass)
        yag.send(to=recipients, subject=subject, contents=message)

        for recipient in recipients:
            print(f"Sent email to {recipient}")


if __name__ == '__main__':
    emailer = Emailer.instance()
    emailer.configure("christianpolka@gmail.com")
    emailer.send_plain_email("cpolka7@gmail.com", "Test", "Hello World")
