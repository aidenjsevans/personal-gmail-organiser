import re

class GmailHelper:
    
    def create_email_address_string_from_email_address_set(email_addresses: set[str]) -> str:
        
        values: list[str] = []
        inner_values: list[str] = []

        if len(email_addresses) == 0:
            raise Exception("At least 1 argument must be given")

        for email_address in email_addresses:
            if GmailHelper.is_valid_email_address(email_address):
                inner_values.append(email_address)
            else:
                raise Exception(f"'{email_address}' is not a valid email address format")
        
        inner_string: str = " OR ".join(inner_values)

        values.append("(")
        values.append(inner_string)
        values.append(")")

        result: str = "".join(values)

        return result

    def create_email_address_set_from_email_address_string(email_address_string: str) -> set[str]:

        email_addresses: set[str] = set()

        if len(email_address_string) == 0:
            raise Exception("At least 1 argument must be given")
        
        if (email_address_string[0] != '(' and email_address_string[-1] != ')'):
            
            if not GmailHelper.is_valid_email_address(email_address_string):
                raise Exception(f"'{email_address_string}' is not a valid email address format")
            
            email_addresses.add(email_address_string)

            return email_addresses
        
        start_index: int = 1
        end_index: int = len(email_address_string) - 1

        inner_string: str = email_address_string[start_index:end_index]
        result: list[str] = inner_string.split(" OR ")

        for element in result:

            if not GmailHelper.is_valid_email_address(element):
                raise Exception(f"'{element}' is not a valid email address format")

            email_addresses.add(element)
        
        return email_addresses

    @staticmethod
    def is_valid_email_address(email_address: str):
        pattern: str = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(pattern=pattern,string=email_address):
            return True
        else:
            return False

