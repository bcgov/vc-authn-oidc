using Newtonsoft.Json;

namespace VCAuthn.ACAPY
{
    public class WalletDidPublicResponse
    {
        public WalletPublicDid Result { get; set; }
    }
    
    public class WalletPublicDid
    {
        [JsonProperty("did")]
        public string DID { get; set; }
            
        [JsonProperty("verkey")]
        public string Verkey { get; set; }
            
        [JsonProperty("public")]
        public bool Public { get; set; }
    }
}