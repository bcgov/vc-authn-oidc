from datetime import datetime, timedelta

from api.verificationConfigs.models import VerificationConfig, VerificationProofRequest
from api.authSessions.models import AuthSession

presentation = {
    "thread_id": "428ab5dc-185f-40ba-8714-498c79b822f3",
    "created_at": "2023-09-15T17:49:16.397954Z",
    "role": "verifier",
    "auto_present": False,
    "presentation_exchange_id": "ccaac3c5-1606-44fb-ade3-33937dfb6dca",
    "presentation_request": {
        "nonce": "633368193772519315256591",
        "name": "proof_requested",
        "version": "0.0.1",
        "requested_attributes": "invalid",  # Add test requested attributes
        "requested_predicates": {},
    },
    "presentation": {
        "proof": {
            "proofs": [
                {
                    "primary_proof": {
                        "eq_proof": {
                            "revealed_attrs": {
                                "email": "73814602767252868561268261832462872577293109184327908660400248444458427915643"
                            },
                            "a_prime": "40809417934849907123261471333411809633354074436405510819719547561843004255793023387498104889708571270607131703938696756407487467873368373775514806534499374680059274765067020721416649641170535056242622419292879011504372419414431627060123535951854477609020119038446707071877530649018798857842493513975477809431501443034563297114458359206476293934461316378865994820249592804467758433904174100097026785285885805688715928578812499534293751388422584754995155726212908115142236221995953756086868367889189436621196564054394071524712971126196703085030819194540892286515361206473918715176334283198231106756804249201321110676817",
                            "e": "132166309846004002298968329630750626534906193461199076364226183288855464715230907038994149984215600411276690314987056469395087923423376034",
                            "v": "389852336354596234620050863642411241608940316153319185423050526707483503655636070718528707360249027781424214465818771183857876571898645233712049550065615437328753383559647676180932006072233802815800996667626559757294734656704881893512658110558847026240354780006408044914149694965180223127754340423475416000940696265773581100989216553579233198807834530514088943560794612627439000580021272527304012796141460444099028132444095750454921031441117671745673457339631909515144154149520136598843334638440138229207476684776682052027672414220327439299122271829090948693982983191662066627130404544959976637513561609461174550463471636750546362339385232864872096796748538286120598703640917737216094473317639418313144992206875604615452306826430748790105881684965109026881701380306409317275248915954859998470708379642658766566479932465684746033865495941061980422316943701392367332573162799073428328950386460662125690364635698421614848860",
                            "m": {
                                "time": "11896542455624181868867605459032062290636202825612483735571300567506766112289589216989585608752835036405824270689163034684130257627062069669940002269643613585904726141499206139998",
                                "master_secret": "11978669714570126125906674715703732098298259897696576462078203241042378591463388624826815153862705227192729264588296043944542578244619153416802465506231069348686312732305137579470",
                            },
                            "m2": "5273201069177175286302918970464632772021241766353736934881903190951819578898991714048991692651562372414552361008106867369251847950990157935703897032904209115054769991615534757984",
                        },
                        "ge_proofs": [],
                    }
                }
            ],
            "aggregated_proof": {
                "c_hash": "8135055767072243139738404741550925116429855319200452769474586673630216912237",
                "c_list": [[1]],  # Not complete data
            },
        },
        "requested_proof": {
            "revealed_attrs": {},
            "revealed_attr_groups": "invalid",  # Add test revealed_attr_groups
            "self_attested_attrs": {},
            "unrevealed_attrs": {},
            "predicates": {},
        },
        "identifiers": [
            {
                "schema_id": "MTYqmTBoLT7KLP5RNfgK3b:2:verified-email:1.2.3",
                "cred_def_id": "MTYqmTBoLT7KLP5RNfgK3b:3:CL:160342:default",
            }
        ],
    },
    "verified": "true",
    "state": "verified",
    "presentation_request_dict": {
        "@type": "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/present-proof/1.0/request-presentation",
        "@id": "428ab5dc-185f-40ba-8714-498c79b822f3",
        "request_presentations~attach": [
            {
                "@id": "libindy-request-presentation-0",
                "mime-type": "application/json",
                "data": {
                    "base64": "eyJuYW1lIjogInByb29mX3JlcXVlc3RlZCIsICJ2ZXJzaW9uIjogIjAuMC4xIiwgInJlcXVlc3RlZF9hdHRyaWJ1dGVzIjogeyJyZXFfYXR0cl8wIjogeyJuYW1lcyI6IFsiZW1haWwiXSwgInJlc3RyaWN0aW9ucyI6IFt7InNjaGVtYV9uYW1lIjogInZlcmlmaWVkLWVtYWlsIiwgImlzc3Vlcl9kaWQiOiAiTVRZcW1UQm9MVDdLTFA1Uk5mZ0szYiJ9XSwgIm5vbl9yZXZva2VkIjogeyJmcm9tIjogMTY5NDgwMDE1NiwgInRvIjogMTY5NDgwMDE1Nn19fSwgInJlcXVlc3RlZF9wcmVkaWNhdGVzIjoge30sICJub25jZSI6ICI2MzMzNjgxOTM3NzI1MTkzMTUyNTY1OTEifQ=="
                },
            }
        ],
    },
    "initiator": "self",
    "updated_at": "2023-09-15T17:49:33.477755Z",
    "trace": False,
    "auto_verify": True,
    "verified_msgs": ["RMV_GLB_NRI", "RMV_RFNT_NRI::req_attr_0"],
}

auth_session = AuthSession(
    pres_exch_id="e444bc3e-346d-47d1-882d-39c014b8978c",
    expired_timestamp=datetime.now() + timedelta(seconds=3000),
    ver_config_id="verified-email",
    request_parameters={
        "scope": "openid vc_authn",
        "state": "oFLNfUyzDtWHmc61dNiQZkVZRsRUUXZ5KZIiQBeQuJQ.xfaKQBh1xfQ.T02DEr3QRTmMUfjegc9fQQ",
        "response_type": "code",
        "client_id": "keycloak",
        "redirect_uri": "http://localhost:8880/auth/realms/vc-authn/broker/vc-authn/endpoint",
        "pres_req_conf_id": "verified-email",
        "nonce": "J2o8dDBWAZyov0ipkMPZng",
    },
    pyop_auth_code="str",
    response_url="str",
    proof_status="pending",
)

ver_config = VerificationConfig(
    ver_config_id="verified-email",
    subject_identifier="email",
    proof_request=VerificationProofRequest(
        name="BCGov Verified Email",
        version="1.0",
        requested_attributes=[
            {
                "names": ["email"],
                "restrictions": [
                    {
                        "schema_name": "verified-email",
                        "issuer_did": "MTYqmTBoLT7KLP5RNfgK3b",
                    }
                ],
            }
        ],
        requested_predicates=[],
    ),
)
