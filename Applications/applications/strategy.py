from models.applications import Report, Listing
from models.applications_otypes import (
    Applications,
)
from utils import (
    get_all_applications,
    get_all_user_applications,
)

from validation import (
    CandidateValidator,
    ExistingListingValidator,
    RecruiterValidator,
)


class Context:
    def __init__(self, strategy):
        self._strategy = strategy

    def set_strategy(self, strategy):
        self._strategy = strategy

    def execute_strategy(self):
        return self._strategy.execute()


class Strategy:
    def execute(self):
        pass


class Recruiter_listing(Strategy):
    def __init__(self, listing: Listing,
                 user) -> None:
        super().__init__()
        self.listing = listing
        self.user = user

    def execute(self):
        handler = RecruiterValidator()
        handler.escalate_request(ExistingListingValidator())
        request = {"listing": self.listing.name, "role": self.user["role"]}
        handler.handle_request(request)
        return Applications(applications=get_all_applications(self.listing.name))


class Candidate_listing(Strategy):
    def __init__(self, listing: Listing,
                 user) -> None:
        super().__init__()
        self.listing = listing
        self.user = user

    def execute(self):
        handler = CandidateValidator()
        handler.escalate_request(ExistingListingValidator())
        request = {"listing": self.listing.name, "role": self.user["role"]}
        handler.handle_request(request)
        return Applications(applications=get_all_user_applications(self.listing.name, self.user["username"]))
