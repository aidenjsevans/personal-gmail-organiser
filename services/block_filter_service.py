from services.gmail_service_user import GmailServiceUser

from models.filters.block_filter import BlockFilter

from exceptions.format_exceptions.invalid_email_format_exception import InvalidEmailFormatException

from utilities.gmail_helper import GmailHelper

class BlockFilterService(GmailServiceUser):

    def __init__(self, gmail_service):
        super().__init__(gmail_service)
    
    def create_email_address_block_filter(
            self,
            name: str,
            blocked_email_addresses: set[str],
            suppress_print: bool) -> BlockFilter:
        
        filter_criteria_blocked_email_address_string: str = GmailHelper.create_email_address_string_from_email_address_set(email_addresses=blocked_email_addresses)

        criteria: dict = {"from": filter_criteria_blocked_email_address_string}

        block_filter = BlockFilter(
            criteria=criteria,
            name=name,
            blocked_email_addresses=blocked_email_addresses
            )
        
        result = self.gmail_service.service.users().settings().filters().create(
            userId="me",
            body=block_filter.config
            ).execute()
        
        block_filter.id = result["id"]

        if suppress_print:
            return block_filter

        print(f"\nBlock filter created:")
        print(f"\n{block_filter.__str__()}")

        return block_filter
    
    def add_email_address_to_block_filter(
            self,
            name: str, 
            blocked_email_addresses: set[str]) -> None:
        
        if len(blocked_email_addresses) == 0:
            raise Exception("At least 1 argument must be given")
        
        old_block_filter = BlockFilter.from_local_json_file_by_name(
            name=name,
            )
        
        old_id: str = old_block_filter.id
        old_blocked_email_addresses: set[str] = old_block_filter.blocked_email_addresses

        self.delete_filter(
            filter_id=old_id,
            suppress_print=True
            )
        
        new_blocked_email_addresses: set[str] = set()

        for email_address in old_blocked_email_addresses:

            if not GmailHelper.is_valid_email_address(email_address):
                raise InvalidEmailFormatException(email_address)
            
            new_blocked_email_addresses.add(email_address)

        for email_address in blocked_email_addresses:
            
            if not GmailHelper.is_valid_email_address(email_address):
                raise InvalidEmailFormatException(email_address)
            
            new_blocked_email_addresses.add(email_address)
        
        new_block_filter = self.create_email_address_block_filter(
            name=name,
            blocked_email_addresses=new_blocked_email_addresses,
            suppress_print=True
            )
        
        print(f"Added email address to block filter:")
        print(f"\n{new_block_filter.__str__()}")
