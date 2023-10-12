import mock
import pytest
from api.authSessions.models import AuthSession
from api.core.oidc.issue_token_service import Token
from api.core.oidc.tests.__mocks__ import auth_session, presentation, ver_config

basic_valid_requested_attributes = {
    "req_attr_0": {
        "names": ["email"],
        "restrictions": [
            {
                "schema_name": "verified-email",
                "issuer_did": "MTYqmTBoLT7KLP5RNfgK3b",
            }
        ],
    }
}

basic_valid_revealed_attr_groups = {
    "req_attr_0": {
        "sub_proof_index": 0,
        "values": {
            "email": {
                "raw": "test@email.com",
                "encoded": "73814602767252868561268261832462872577293109184327908660400248444458427915643",
            }
        },
    }
}

multiple_valid_requested_attributes = {
    "req_attr_0": {
        "names": ["email_1", "age_1"],
        "restrictions": [
            {
                "schema_name": "verified-email",
                "issuer_did": "MTYqmTBoLT7KLP5RNfgK3b",
            }
        ],
    },
}

multiple_valid_revealed_attr_groups = {
    "req_attr_0": {
        "sub_proof_index": 0,
        "values": {
            "email_1": {
                "raw": "test@email.com",
                "encoded": "73814602767252868561268261832462872577293109184327908660400248444458427915643",
            },
            "age_1": {
                "raw": "30",
                "encoded": "73814602767252868561268261832462872577293109184327908660400248444458427915644",
            },
        },
    }
}


@pytest.mark.asyncio
async def test_valid_proof_presentation_with_one_attribute_returns_claims():
    presentation["presentation_request"][
        "requested_attributes"
    ] = basic_valid_requested_attributes
    presentation["presentation"]["requested_proof"][
        "revealed_attr_groups"
    ] = basic_valid_revealed_attr_groups
    with mock.patch.object(AuthSession, "presentation_exchange", presentation):
        claims = Token.get_claims(auth_session, ver_config)
        assert claims is not None


@pytest.mark.asyncio
async def test_valid_proof_presentation_with_multiple_attributes_returns_claims():
    presentation["presentation_request"]["requested_attributes"] = {
        "req_attr_0": {
            "names": ["email"],
            "restrictions": [
                {
                    "schema_name": "verified-email",
                    "issuer_did": "MTYqmTBoLT7KLP5RNfgK3b",
                }
            ],
        },
        "req_attr_1": {
            "names": ["age"],
            "restrictions": [
                {
                    "schema_name": "verified-age",
                    "issuer_did": "MTYqmTBoLT7KLP5RNfgK3c",
                }
            ],
        },
    }
    presentation["presentation"]["requested_proof"]["revealed_attr_groups"] = {
        "req_attr_0": {
            "sub_proof_index": 0,
            "values": {
                "email": {
                    "raw": "test@email.com",
                    "encoded": "73814602767252868561268261832462872577293109184327908660400248444458427915643",
                }
            },
        },
        "req_attr_1": {
            "sub_proof_index": 0,
            "values": {
                "age": {
                    "raw": "30",
                    "encoded": "73814602767252868561268261832462872577293109184327908660400248444458427915644",
                }
            },
        },
    }
    with mock.patch.object(AuthSession, "presentation_exchange", presentation):
        claims = Token.get_claims(auth_session, ver_config)
        assert claims is not None


@pytest.mark.asyncio
async def test_include_v1_attributes_false_does_not_add_the_named_attributes():
    presentation["presentation_request"][
        "requested_attributes"
    ] = multiple_valid_requested_attributes
    presentation["presentation"]["requested_proof"][
        "revealed_attr_groups"
    ] = multiple_valid_revealed_attr_groups
    with mock.patch.object(AuthSession, "presentation_exchange", presentation):
        ver_config.include_v1_attributes = False
        claims = Token.get_claims(auth_session, ver_config)
        vc_presented_attributes_obj = eval(claims["vc_presented_attributes"])
        assert claims is not None
        assert vc_presented_attributes_obj["email_1"] == "test@email.com"
        assert vc_presented_attributes_obj["age_1"] == "30"
        assert "email_1" not in claims
        assert "age_1" not in claims


@pytest.mark.asyncio
async def test_include_v1_attributes_true_adds_the_named_attributes():
    presentation["presentation_request"][
        "requested_attributes"
    ] = multiple_valid_requested_attributes
    presentation["presentation"]["requested_proof"][
        "revealed_attr_groups"
    ] = multiple_valid_revealed_attr_groups
    with mock.patch.object(AuthSession, "presentation_exchange", presentation):
        ver_config.include_v1_attributes = True
        claims = Token.get_claims(auth_session, ver_config)
        vc_presented_attributes_obj = eval(claims["vc_presented_attributes"])
        assert claims is not None
        assert vc_presented_attributes_obj["email_1"] == "test@email.com"
        assert vc_presented_attributes_obj["age_1"] == "30"
        assert claims["email_1"] == "test@email.com"
        assert claims["age_1"] == "30"


@pytest.mark.asyncio
async def test_include_v1_attributes_none_does_not_add_the_named_attributes():
    presentation["presentation_request"][
        "requested_attributes"
    ] = multiple_valid_requested_attributes
    presentation["presentation"]["requested_proof"][
        "revealed_attr_groups"
    ] = multiple_valid_revealed_attr_groups
    with mock.patch.object(AuthSession, "presentation_exchange", presentation):
        ver_config.include_v1_attributes = None
        print(ver_config.include_v1_attributes)
        claims = Token.get_claims(auth_session, ver_config)
        vc_presented_attributes_obj = eval(claims["vc_presented_attributes"])
        assert claims is not None
        assert vc_presented_attributes_obj["email_1"] == "test@email.com"
        assert vc_presented_attributes_obj["age_1"] == "30"
        assert "email_1" not in claims
        assert "age_1" not in claims


@pytest.mark.asyncio
async def test_revealed_attrs_dont_match_requested_attributes_throws_exception():
    presentation["presentation_request"]["requested_attributes"] = {
        "req_attr_0": {
            "names": ["email"],
            "restrictions": [
                {
                    "schema_name": "verified-email",
                    "issuer_did": "MTYqmTBoLT7KLP5RNfgK3b",
                }
            ],
        }
    }
    presentation["presentation"]["requested_proof"]["revealed_attr_groups"] = {
        "req_attr_0": {
            "sub_proof_index": 0,
            "values": {
                "email-wrong": {
                    "raw": "test@email.com",
                    "encoded": "73814602767252868561268261832462872577293109184327908660400248444458427915643",
                }
            },
        }
    }
    with mock.patch.object(AuthSession, "presentation_exchange", presentation):
        with pytest.raises(Exception):
            Token.get_claims(auth_session, ver_config)


@pytest.mark.asyncio
async def test_valid_presentation_with_matching_subject_identifier_has_identifier_in_claims_sub():
    presentation["presentation_request"][
        "requested_attributes"
    ] = basic_valid_requested_attributes
    presentation["presentation"]["requested_proof"][
        "revealed_attr_groups"
    ] = basic_valid_revealed_attr_groups
    with mock.patch.object(AuthSession, "presentation_exchange", presentation):
        claims = Token.get_claims(auth_session, ver_config)
        print(claims)
        assert claims["sub"] == "test@email.com"


@pytest.mark.asyncio
async def test_valid_presentation_with_non_matching_subject_identifier_and_has_no_sub():
    presentation["presentation_request"][
        "requested_attributes"
    ] = basic_valid_requested_attributes
    presentation["presentation"]["requested_proof"][
        "revealed_attr_groups"
    ] = basic_valid_revealed_attr_groups
    with mock.patch.object(AuthSession, "presentation_exchange", presentation):
        ver_config.subject_identifier = "not-email"
        claims = Token.get_claims(auth_session, ver_config)
        assert "sub" not in claims
