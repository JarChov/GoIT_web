from abc import abstractmethod, ABC
from classes import Record, Phone


class ShowedInfo(ABC):
    @abstractmethod
    def message(self, record: Record):
        pass


class ChangedAndShowedInfo(ABC):
    @abstractmethod
    def change_and_print(self, record: Record, phone: Phone):
        pass


class MessageUserAdding(ShowedInfo):
    def message(self, record: Record):
        return f'For user {record.name.value} added phone number {record.phones[-1]}'


class MessagePhoneChanging(ChangedAndShowedInfo):
    def change_and_print(self, record: Record, phone: Phone):
        return f'For user {record.name.value} number {phone} successfully changed to new number {record.phones[-1]}'


class MessageDeletePhone(ChangedAndShowedInfo):
    def change_and_print(self, record: Record, phone: Phone):
        return f'For user {record.name.value} phone number {phone} successfully deleted'


class MessageShowRecords(ShowedInfo):
    def message(self, record: Record):
        phones_num = ''

        if len(record.phones) == 1:
            return f"User {record.name.value} phone number: {record.phones[0]} birthday {record.birthday}\n"
        elif len(record.phones) == 0:
            return f"User {record.name.value} haven't phone number birthday {record.birthday}\n"
        else:
            for phone in record.phones:
                phones_num += str(phone) + '; '
            return f"User {record.name.value} phone number's: {phones_num.removesuffix('; ')}" \
                   f" birthday {record.birthday}\n"


class MessageAddBirthday(ShowedInfo):
    def message(self, record: Record):
        return f'For user {record.name.value} added birthday date {record.birthday}'


class MessageDaysToBirthday(ShowedInfo):
    pass
