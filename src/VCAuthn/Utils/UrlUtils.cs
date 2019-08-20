namespace VCAuthn.Utils
{
    public static class UrlUtils
    {
        public static string EnsureLeadingSlash(this string url)
        {
            if (url.StartsWith("/"))
            {
                return url;
            }

            return $"/{url}";
        }
    }
}