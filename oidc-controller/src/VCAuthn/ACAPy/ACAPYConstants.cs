namespace VCAuthn.ACAPY
{
    public static class ACAPYConstants
    {
        public const string ApiKeyHeader = "x-api-key";

        public const string WalletDidPublicUri = "/wallet/did/public";
        public const string PresentationExchangeCreateRequest = "/presentation_exchange/create_request";
        public const string GetPresentationRecord = "/presentation_exchange";

        public const string SuccessfulPresentationUpdate = "presentation_received";
        public const string PresentationsTopic = "presentations";
    }
}