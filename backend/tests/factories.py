import factory
from factory.django import DjangoModelFactory
from captives.models import Captive
from contacts.models import Contact
from policies.models import Policy
from claims.models import Claim

class CaptiveFactory(DjangoModelFactory):
    class Meta:
        model = Captive
    name = factory.Sequence(lambda n: f"TestCaptor-{n}")
    jurisdiction = "CYM"
    formation_date = "2023-01-01"
    status = "ACTIVE"

class ContactFactory(DjangoModelFactory):
    class Meta:
        model = Contact
    first_name = "Jane"
    last_name = factory.Sequence(lambda n: f"Doe{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.first_name.lower()}.{obj.last_name.lower()}@example.com")

class PolicyFactory(DjangoModelFactory):
    class Meta:
        model = Policy
    captive = factory.SubFactory(CaptiveFactory)
    policy_number = factory.Sequence(lambda n: f"P{n:03d}")
    inception_date = "2023-02-01"
    expiration_date = "2024-01-31"

class ClaimFactory(DjangoModelFactory):
    class Meta:
        model = Claim
    policy = factory.SubFactory(PolicyFactory)
    claim_number = factory.Sequence(lambda n: f"C{n:03d}")
    loss_date = "2023-03-01"
