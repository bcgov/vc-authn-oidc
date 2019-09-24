using Microsoft.IdentityModel.Tokens;
using Newtonsoft.Json;

namespace VCAuthn.Utils
{
    public static class Formatting
    {
        public static string ToJson(this object obj)
        {
            return JsonConvert.SerializeObject(obj, Newtonsoft.Json.Formatting.None);
        }

        public static string ToBase64(this string value)
        {
            return Base64UrlEncoder.Encode(value);
        }
    }
}