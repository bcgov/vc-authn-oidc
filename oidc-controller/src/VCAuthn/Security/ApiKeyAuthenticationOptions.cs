using Microsoft.AspNetCore.Authentication;

namespace VCAuthn.Security
{
    public class ApiKeyAuthenticationOptions : AuthenticationSchemeOptions
    {
        public const string DefaultScheme = "API Key";
        public string Key;
        public string Scheme => DefaultScheme;
        public string AuthenticationType = DefaultScheme;
    }
}
