
using Microsoft.IdentityModel.Tokens;
using Newtonsoft.Json;
using System.Text;
using System;

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
            byte[] stringBytes = Encoding.UTF8.GetBytes(value);
            return Convert.ToBase64String(stringBytes);
        }

        public static string FromBase64(this string value)
        {
            byte[] stringBytes = Convert.FromBase64String(value);
            return Encoding.UTF8.GetString(stringBytes);
        }

        public static string ToBase64Url(this string value)
        {
            return Base64UrlEncoder.Encode(value);
        }

        public static string FromBase64Url(this string value)
        {
            return Base64UrlEncoder.Decode(value);

        }
    }
}