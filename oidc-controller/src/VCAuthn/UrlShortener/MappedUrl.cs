using System.ComponentModel.DataAnnotations;

namespace VCAuthn.UrlShortener
{
    public class MappedUrl
    {
        [Key]
        public string Key { get; set; }

        public string Url { get; set; }
    }
}