using System;

namespace VCAuthn.IdentityServer.SessionStorage
{
    public class AuthSession
    {
        public string Id { get; set; }
        public string PresentationRequestId { get; set; }
        public DateTime ExpiredTimestamp { get; set; }
        public bool PresentationRequestSatisfied { get; set; }
    }
}