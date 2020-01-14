namespace VCAuthn.IdentityServer
{
    public class IdentityConstants
    {
        public const string AuthenticationContextReferenceIdentityTokenKey = "acr";
        public const string SubjectIdentityTokenKey = "sub";

        public const string ClientId = "client_id";
        public const string ScopeParamName = "scope";
        public const string VCAuthnScopeName = "vc_authn";
        public const string MissingVCAuthnScopeError = "missing_vc_authn_scope";
        public static readonly string MissingVCAuthnScopeDesc = $"Missing {VCAuthnScopeName} scope"; 
        
        public const string PresentationRequestConfigIDParamName = "pres_req_conf_id";
        public const string InvalidPresentationRequestConfigIDError = "invalid_pres_req_conf_id";
        public static readonly string InvalidPresentationRequestConfigIDDesc = $"Missing {PresentationRequestConfigIDParamName} param";

        public const string RedirectUriParameterName = "redirect_uri";
        public const string InvalidRedirectUriError = "invalid_redirect_uri";
        
        public const string GrantTypeParameterName = "grant_type";
        public const string InvalidGrantTypeError = "invalid_grant_type";
        
        public const string UnknownPresentationRecordId = "unknown_presentation_record_id";
        public const string PresentationUrlBuildFailed = "presentation_url_build_failed";
        public const string SessionStartFailed = "session_start_failed";
        public const string AcapyCallFailed = "acapy_call_failed";
        
        public const string ResponseTypeUriParameterName = "response_type";
        public const string DefaultResponseType = "form_post";
        
        public const string ResponseModeUriParameterName = "response_mode";
        public const string DefaultResponseMode = "authorization_code";

        public const string StateParameterName = "state";
        public const string NonceParameterName = "nonce";
        public const string AuthorizationCodeParameterName = "code";
        public const string InvalidAuthorizationCodeError = "invalid_authorization_code";

        public const string SessionIdCookieName = "sessionid";
        public const string InvalidSessionError = "invalid_session";
        
        public const string GeneralError = "error";

        public const string AuthorizationViewName = "/Views/Authorize/Authorize.cshtml";
        
        public const string ChallengeIdQueryParameterName = "pid";
        public const string ChallengePollUri = "vc/connect/poll";
        public const string AuthorizeCallbackUri = "vc/connect/callback";
        public const string VerifiedCredentialAuthorizeUri = "vc/connect/authorize";
        public const string VerifiedCredentialTokenUri = "vc/connect/token";

        // Standard OIDC claim names
        public const string OIDCTokenIssuedAt = "iat";
    }
}