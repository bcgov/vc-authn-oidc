using System;
using System.Collections.Generic;
using Newtonsoft.Json;
using VCAuthn.Models;

namespace VCAuthn.Utils
{
    public static class ProofRequestUtils
    {
        public static string GenerateProofRequest(PresentationRequestConfiguration configuration)
        {
            string proofRequest;

            if (configuration.ProtocolVersion == null || configuration.ProtocolVersion.Equals("0.1"))
            {
                PresentationRequestConfiguration localConfig = configuration;
                localConfig.ProtocolVersion = null;
                proofRequest = JsonConvert.SerializeObject(localConfig, new JsonSerializerSettings { NullValueHandling = NullValueHandling.Ignore });
            }
            else
            {
                ProofRequest_v_1_0 proofRequest_1_0 = new ProofRequest_v_1_0();
                proofRequest_1_0.Version = configuration.Version;

                foreach (RequestedAttribute reqAttribute in configuration.RequestedAttributes) {
                    proofRequest_1_0.RequestedAttributes.Add(Guid.NewGuid().ToString(), reqAttribute);
                }
                foreach (RequestedPredicate reqPredicate in configuration.RequestedPredicates) {
                    proofRequest_1_0.RequestedPredicates.Add(Guid.NewGuid().ToString(), reqPredicate);
                }

                Dictionary<string, ProofRequest_v_1_0> requestBody = new Dictionary<string, ProofRequest_v_1_0>();
                requestBody.Add("proof_request", proofRequest_1_0);
                proofRequest = JsonConvert.SerializeObject(requestBody);
            }
            return proofRequest;
        }
    }

    class ProofRequest_v_1_0
    {
        [JsonProperty("version")]
        public string Version { get; set; }

        [JsonProperty("requested_attributes")]
        public Dictionary<string, RequestedAttribute> RequestedAttributes { get; set; } = new Dictionary<string, RequestedAttribute>();

        [JsonProperty("requested_predicates")]
        public Dictionary<string, RequestedPredicate> RequestedPredicates { get; set; } = new Dictionary<string, RequestedPredicate>();
    }
}